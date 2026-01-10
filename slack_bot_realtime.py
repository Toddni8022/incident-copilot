"""Real-time Slack bot for IT Incident Copilot.

This bot listens to a specific Slack channel and automatically generates
incident reports when triggered by a keyword or reaction.

Setup:
1. Create a Slack App at https://api.slack.com/apps
2. Enable Socket Mode and get an App Token (xapp-...)
3. Add Bot Token Scopes: channels:history, channels:read, chat:write, reactions:read
4. Install app to workspace
5. Add these to .env:
   - SLACK_BOT_TOKEN=xoxb-...
   - SLACK_APP_TOKEN=xapp-...
   - INCIDENT_CHANNEL_ID=C01234ABCDE
"""

from slack_sdk import WebClient
from slack_sdk.socket_mode import SocketModeClient
from slack_sdk.socket_mode.response import SocketModeResponse
from slack_sdk.socket_mode.request import SocketModeRequest
from incident_parser import IncidentCopilot
from config import Config, setup_logging, DEFAULT_MESSAGE_LIMIT
import logging
import re

# Setup logging
logger = setup_logging(__name__)


class IncidentSlackBot:
    """Real-time Slack bot that monitors channels for incident reports."""

    def __init__(self, config: Config):
        """Initialize the Slack bot.

        Args:
            config: Application configuration.

        Raises:
            ValueError: If required configuration is missing.
        """
        config.validate_anthropic()
        config.validate_slack()

        self.config = config
        self.copilot = IncidentCopilot(config)

        # Get app token for Socket Mode
        import os
        self.app_token = os.getenv("SLACK_APP_TOKEN")
        if not self.app_token:
            raise ValueError(
                "SLACK_APP_TOKEN environment variable is required for Socket Mode. "
                "Get it from: https://api.slack.com/apps → Your App → Basic Information → App-Level Tokens"
            )

        self.web_client = WebClient(token=config.slack_bot_token)

        # Initialize Socket Mode client
        self.socket_client = SocketModeClient(
            app_token=self.app_token,
            web_client=self.web_client
        )

        # Trigger keywords
        self.trigger_keywords = ['@incident-report', '/incident', '!incident']

        logger.info("Slack bot initialized")

    def process_message(self, message_text: str, channel_id: str, thread_ts: str = None):
        """Process a message and generate incident report.

        Args:
            message_text: The message text to analyze.
            channel_id: Slack channel ID.
            thread_ts: Thread timestamp (optional).
        """
        try:
            logger.info("Processing incident request in channel %s", channel_id)

            # Generate report
            report = self.copilot.parse_incident(message_text)
            markdown = self.copilot.format_markdown(report)

            # Post report to Slack
            response_text = f"📊 **Incident Report Generated**\n\n```\n{markdown}\n```"

            self.web_client.chat_postMessage(
                channel=channel_id,
                text=response_text,
                thread_ts=thread_ts  # Reply in thread if applicable
            )

            logger.info("Successfully posted incident report")

        except Exception as e:
            logger.error("Error processing incident: %s", e)
            self.web_client.chat_postMessage(
                channel=channel_id,
                text=f"❌ Error generating report: {e}",
                thread_ts=thread_ts
            )

    def handle_message(self, client: SocketModeClient, req: SocketModeRequest):
        """Handle incoming Slack messages.

        Args:
            client: Socket Mode client.
            req: Incoming request.
        """
        # Acknowledge the request
        response = SocketModeResponse(envelope_id=req.envelope_id)
        client.send_socket_mode_response(response)

        # Check if it's a message event
        if req.type == "events_api":
            event = req.payload.get("event", {})

            if event.get("type") == "message" and "subtype" not in event:
                text = event.get("text", "")
                channel = event.get("channel")
                thread_ts = event.get("thread_ts", event.get("ts"))

                # Check for trigger keywords
                should_process = any(keyword in text.lower() for keyword in self.trigger_keywords)

                if should_process:
                    logger.info("Trigger detected in message: %s", text[:50])

                    # Fetch recent messages from the channel
                    try:
                        result = self.web_client.conversations_history(
                            channel=channel,
                            limit=DEFAULT_MESSAGE_LIMIT
                        )
                        messages = result.get("messages", [])

                        # Combine messages
                        combined_text = "\n".join([
                            msg.get("text", "") for msg in messages
                            if "text" in msg
                        ])

                        # Process the incident
                        self.process_message(combined_text, channel, thread_ts)

                    except Exception as e:
                        logger.error("Error fetching channel history: %s", e)

    def handle_reaction(self, client: SocketModeClient, req: SocketModeRequest):
        """Handle emoji reactions (alternative trigger method).

        Args:
            client: Socket Mode client.
            req: Incoming request.
        """
        # Acknowledge the request
        response = SocketModeResponse(envelope_id=req.envelope_id)
        client.send_socket_mode_response(response)

        if req.type == "events_api":
            event = req.payload.get("event", {})

            # Check for specific emoji reaction (e.g., 🚨 or :incident:)
            if event.get("type") == "reaction_added":
                reaction = event.get("reaction")
                if reaction in ["rotating_light", "fire", "incident"]:
                    channel = event.get("item", {}).get("channel")
                    message_ts = event.get("item", {}).get("ts")

                    logger.info("Incident reaction detected: %s", reaction)

                    # Fetch the thread or recent messages
                    try:
                        result = self.web_client.conversations_history(
                            channel=channel,
                            limit=DEFAULT_MESSAGE_LIMIT
                        )
                        messages = result.get("messages", [])

                        combined_text = "\n".join([
                            msg.get("text", "") for msg in messages
                            if "text" in msg
                        ])

                        self.process_message(combined_text, channel, message_ts)

                    except Exception as e:
                        logger.error("Error processing reaction: %s", e)

    def start(self):
        """Start the Slack bot."""
        logger.info("Starting Slack bot...")

        # Register event handlers
        self.socket_client.socket_mode_request_listeners.append(self.handle_message)
        self.socket_client.socket_mode_request_listeners.append(self.handle_reaction)

        # Start listening
        logger.info("🤖 Slack bot is running! Listening for triggers...")
        print("🤖 Incident Copilot Slack Bot is running!")
        print("   Triggers:")
        print("   - Type: @incident-report, /incident, or !incident")
        print("   - React with: 🚨 :rotating_light: :fire: :incident:")
        print("\nPress Ctrl+C to stop...")

        self.socket_client.connect()

        # Keep the bot running
        from threading import Event
        Event().wait()


def main():
    """Main entry point for the Slack bot."""
    try:
        config = Config()

        # Check if app token is set
        import os
        app_token = os.getenv("SLACK_APP_TOKEN")
        if not app_token:
            raise ValueError(
                "SLACK_APP_TOKEN environment variable is required. "
                "Get it from: https://api.slack.com/apps → Your App → Basic Information → App-Level Tokens"
            )

        bot = IncidentSlackBot(config)
        bot.start()

    except KeyboardInterrupt:
        logger.info("Bot stopped by user")
        print("\n\n⏹️  Bot stopped.")
    except Exception as e:
        logger.exception("Fatal error: %s", e)
        print(f"\n❌ Error: {e}")
        print("\nMake sure you have:")
        print("1. ANTHROPIC_API_KEY set in .env")
        print("2. SLACK_BOT_TOKEN set in .env")
        print("3. SLACK_APP_TOKEN set in .env")
        print("4. Socket Mode enabled in your Slack app")
        return 1

    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())
