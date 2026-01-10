"""Manual Slack channel analysis script for IT Incident Copilot."""

from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from incident_parser import IncidentCopilot
from typing import List, Dict
from anthropic import APIError, APIConnectionError, RateLimitError
from pydantic import ValidationError
from config import Config, setup_logging, DEFAULT_MESSAGE_LIMIT

# Setup logging
logger = setup_logging(__name__)


def fetch_slack_messages(
    client: WebClient, channel_id: str, limit: int = DEFAULT_MESSAGE_LIMIT
) -> List[Dict]:
    """Fetch messages from a Slack channel.

    Args:
        client: Slack WebClient instance.
        channel_id: Slack channel ID to fetch from.
        limit: Maximum number of messages to fetch.

    Returns:
        List[Dict]: List of message dictionaries.

    Raises:
        SlackApiError: If Slack API request fails.
    """
    logger.info("Fetching %d messages from channel %s", limit, channel_id)
    print(f"Fetching messages from channel {channel_id}...")

    result = client.conversations_history(channel=channel_id, limit=limit)
    messages = result.get("messages", [])

    logger.info("Retrieved %d messages", len(messages))
    print(f"Found {len(messages)} messages. Analyzing...")

    return messages


def combine_messages(messages: List[Dict]) -> str:
    """Combine Slack messages into a single text string.

    Args:
        messages: List of Slack message dictionaries.

    Returns:
        str: Combined message text.
    """
    return "\n".join([msg.get("text", "") for msg in messages if "text" in msg])


def process_channel_history(
    copilot: IncidentCopilot, client: WebClient, channel_id: str, limit: int = DEFAULT_MESSAGE_LIMIT
) -> None:
    """Fetch, analyze, and post incident report for a Slack channel.

    Args:
        copilot: IncidentCopilot instance for parsing.
        client: Slack WebClient instance.
        channel_id: Slack channel ID to analyze.
        limit: Maximum number of messages to fetch.

    Raises:
        SlackApiError: If Slack API request fails.
        APIError: If OpenAI API request fails.
        ValueError: If no messages found or input is empty.
    """
    # Fetch messages
    messages = fetch_slack_messages(client, channel_id, limit)

    if not messages:
        raise ValueError("No messages found in channel")

    # Combine into text
    raw_text = combine_messages(messages)

    if not raw_text.strip():
        raise ValueError("No text content found in messages")

    # Generate report
    logger.info("Generating incident report")
    report = copilot.parse_incident(raw_text)
    markdown = copilot.format_markdown(report)

    print("\n" + markdown + "\n")

    # Post back to channel
    logger.info("Posting report to Slack channel %s", channel_id)
    client.chat_postMessage(channel=channel_id, text=f"`{markdown}`")

    print("✅ Report posted to Slack!")
    logger.info("Report successfully posted to Slack")


def main() -> int:
    """Main entry point for manual Slack analysis.

    Returns:
        int: Exit code (0 for success, 1 for error).
    """
    print("Slack Incident Copilot - Manual Mode")
    print("=====================================\n")

    try:
        # Initialize configuration
        config = Config()
        config.validate_slack()
        config.validate_openai()

        # Initialize clients
        client = WebClient(token=config.slack_bot_token)
        copilot = IncidentCopilot(config)

        # Get channel ID from user
        channel_id = input(
            "Enter Slack channel ID (right-click channel > View channel details): "
        ).strip()

        if not channel_id:
            print("Error: Channel ID is required")
            return 1

        # Process channel
        process_channel_history(copilot, client, channel_id)

        return 0

    except ValueError as e:
        logger.error("Configuration error: %s", e)
        print(f"\nError: {e}")
        print("Please check your .env file and ensure all required variables are set.")
        return 1

    except SlackApiError as e:
        logger.error("Slack API error: %s", e.response["error"])
        print(f"\nSlack API Error: {e.response['error']}")
        print("Please check your Slack bot token and channel ID.")
        return 1

    except APIConnectionError as e:
        logger.error("API connection failed: %s", e)
        print("\nError: Unable to connect to Claude API. Please check your internet connection.")
        return 1

    except RateLimitError as e:
        logger.error("Rate limit exceeded: %s", e)
        print("\nError: Claude API rate limit exceeded. Please try again later.")
        return 1

    except APIError as e:
        logger.error("Claude API error: %s", e)
        print(f"\nClaude API Error: {e}")
        return 1

    except KeyboardInterrupt:
        logger.info("Operation cancelled by user")
        print("\n\nOperation cancelled.")
        return 1

    except Exception as e:
        logger.exception("Unexpected error: %s", e)
        print(f"\nUnexpected error: {e}")
        return 1


if __name__ == "__main__":
    import sys

    sys.exit(main())
