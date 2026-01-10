"""Streamlit web interface for IT Incident Copilot."""

import streamlit as st
from incident_parser import IncidentCopilot, IncidentReport
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from datetime import datetime
from pathlib import Path
from typing import Optional, List, Dict
import logging
from anthropic import APIError, APIConnectionError, RateLimitError
from pydantic import ValidationError
from config import Config, setup_logging, TIMESTAMP_FORMAT, DEFAULT_MESSAGE_LIMIT

# Setup logging
logger = setup_logging(__name__)

# Page configuration
st.set_page_config(page_title="IT Incident Copilot", page_icon="🚨", layout="wide")


def get_config() -> Config:
    """Get or initialize configuration.

    Returns:
        Config: Application configuration instance.
    """
    if "config" not in st.session_state:
        st.session_state.config = Config()
    return st.session_state.config


def get_copilot(config: Config) -> Optional[IncidentCopilot]:
    """Get or initialize incident copilot.

    Args:
        config: Application configuration.

    Returns:
        Optional[IncidentCopilot]: Copilot instance or None if API key not configured.
    """
    if not config.has_anthropic():
        return None

    if "copilot" not in st.session_state:
        try:
            st.session_state.copilot = IncidentCopilot(config)
        except ValueError as e:
            logger.error("Failed to initialize copilot: %s", e)
            return None

    return st.session_state.copilot


def get_slack_client(config: Config) -> Optional[WebClient]:
    """Get or initialize Slack client.

    Args:
        config: Application configuration.

    Returns:
        Optional[WebClient]: Slack client or None if token not configured.
    """
    if not config.has_slack():
        return None

    if "slack_client" not in st.session_state:
        st.session_state.slack_client = WebClient(token=config.slack_bot_token)

    return st.session_state.slack_client


def save_report(markdown: str, output_dir: str) -> str:
    """Save incident report to a timestamped file.

    Args:
        markdown: Markdown-formatted report content.
        output_dir: Directory to save the report in.

    Returns:
        str: Path to the saved file.

    Raises:
        OSError: If unable to write to the file.
    """
    timestamp = datetime.now().strftime(TIMESTAMP_FORMAT)
    output_path = Path(output_dir) / f"incident_report_{timestamp}.md"
    output_path.write_text(markdown, encoding="utf-8")
    logger.info("Report saved to: %s", output_path)
    return str(output_path)


def display_report_with_download(markdown: str, config: Config) -> None:
    """Display report and provide download/save options.

    Args:
        markdown: Markdown-formatted report to display.
        config: Application configuration.
    """
    st.markdown("---")
    st.markdown(markdown)

    # Download button
    timestamp = datetime.now().strftime(TIMESTAMP_FORMAT)
    st.download_button(
        label="📥 Download Report",
        data=markdown,
        file_name=f"incident_report_{timestamp}.md",
        mime="text/markdown",
    )

    # Save to file
    try:
        output_file = save_report(markdown, config.output_dir)
        st.info(f"Report saved to: {output_file}")
    except OSError as e:
        logger.error("Failed to save report: %s", e)
        st.warning(f"Could not save to file: {e}")


def fetch_slack_messages(
    slack_client: WebClient, channel_id: str, limit: int
) -> List[Dict]:
    """Fetch messages from a Slack channel.

    Args:
        slack_client: Slack WebClient instance.
        channel_id: Slack channel ID to fetch from.
        limit: Maximum number of messages to fetch.

    Returns:
        List[Dict]: List of message dictionaries.

    Raises:
        SlackApiError: If Slack API request fails.
    """
    logger.info("Fetching %d messages from channel %s", limit, channel_id)
    result = slack_client.conversations_history(channel=channel_id, limit=limit)
    messages = result.get("messages", [])
    logger.info("Retrieved %d messages", len(messages))
    return messages


def combine_slack_messages(messages: List[Dict]) -> str:
    """Combine Slack messages into a single text string.

    Args:
        messages: List of Slack message dictionaries.

    Returns:
        str: Combined message text.
    """
    return "\n".join([msg.get("text", "") for msg in messages if "text" in msg])


def handle_error(error: Exception) -> None:
    """Display appropriate error message based on exception type.

    Args:
        error: Exception that occurred.
    """
    if isinstance(error, ValueError):
        st.error(f"❌ Invalid input: {error}")
    elif isinstance(error, APIConnectionError):
        st.error("❌ Unable to connect to Claude API. Please check your internet connection.")
    elif isinstance(error, RateLimitError):
        st.error("❌ Claude API rate limit exceeded. Please try again later.")
    elif isinstance(error, APIError):
        st.error(f"❌ Claude API error: {error}")
    elif isinstance(error, ValidationError):
        st.error("❌ Received invalid response from Claude. Please try again.")
    elif isinstance(error, SlackApiError):
        st.error(f"❌ Slack API error: {error.response['error']}")
    else:
        st.error(f"❌ Error: {error}")
        logger.exception("Unexpected error: %s", error)


# Initialize configuration
config = get_config()

# Header
st.title("🚨 IT Incident Copilot")
st.markdown("Transform messy incident notes into professional reports")

# Initialize services
copilot = get_copilot(config)
slack_client = get_slack_client(config)

# Tabs
tab1, tab2, tab3 = st.tabs(["📝 Text Input", "💬 Slack Channel", "📊 View Reports"])

# Tab 1: Direct Text Input
with tab1:
    st.subheader("Paste Incident Notes")

    incident_text = st.text_area(
        "Enter messy ticket notes, chat logs, or outage descriptions:",
        height=300,
        placeholder="""Example:
prod db slow, users reporting 500 errors starting around 2:45pm
checked logs - connection pool maxed out
dave restarted db at 3:10
errors stopped at 3:15
need to fix cron schedule and add monitoring""",
    )

    col1, col2 = st.columns([1, 4])
    with col1:
        analyze_btn = st.button("Generate Report", type="primary", use_container_width=True)

    if analyze_btn:
        if not copilot:
            st.error("❌ Claude API key not configured. Please set ANTHROPIC_API_KEY in your .env file.")
        elif not incident_text or not incident_text.strip():
            st.warning("⚠️ Please enter incident notes to analyze.")
        else:
            with st.spinner("🔄 Analyzing incident with Claude AI..."):
                try:
                    report = copilot.parse_incident(incident_text)
                    markdown = copilot.format_markdown(report)

                    st.success("✅ Report generated!")
                    display_report_with_download(markdown, config)

                except Exception as e:
                    handle_error(e)

# Tab 2: Slack Integration
with tab2:
    st.subheader("Analyze Slack Channel")

    channel_id = st.text_input(
        "Slack Channel ID",
        placeholder="C01234ABCDE",
        help="Right-click channel in Slack > View channel details > Copy Channel ID",
    )

    message_limit = st.slider(
        "Number of messages to analyze", 10, 100, DEFAULT_MESSAGE_LIMIT
    )

    col1, col2 = st.columns([1, 4])
    with col1:
        fetch_btn = st.button("Fetch & Analyze", type="primary", use_container_width=True)

    if fetch_btn:
        if not copilot:
            st.error("❌ Claude API key not configured. Please set ANTHROPIC_API_KEY in your .env file.")
        elif not slack_client:
            st.error("❌ Slack not configured. Please set SLACK_BOT_TOKEN in your .env file.")
        elif not channel_id or not channel_id.strip():
            st.warning("⚠️ Please enter a Slack channel ID.")
        else:
            with st.spinner(f"🔄 Fetching {message_limit} messages from Slack..."):
                try:
                    # Fetch messages
                    messages = fetch_slack_messages(slack_client, channel_id, message_limit)

                    if not messages:
                        st.warning("⚠️ No messages found in channel.")
                    else:
                        st.info(f"Found {len(messages)} messages")

                        # Combine and analyze
                        raw_text = combine_slack_messages(messages)

                        with st.spinner("🤖 Generating incident report..."):
                            report = copilot.parse_incident(raw_text)
                            markdown = copilot.format_markdown(report)

                            st.success("✅ Report generated!")

                            # Display report
                            st.markdown("---")
                            st.markdown(markdown)

                            # Options
                            col_a, col_b = st.columns(2)

                            with col_a:
                                timestamp = datetime.now().strftime(TIMESTAMP_FORMAT)
                                st.download_button(
                                    label="📥 Download Report",
                                    data=markdown,
                                    file_name=f"incident_report_{timestamp}.md",
                                    mime="text/markdown",
                                )

                            with col_b:
                                if st.button("📤 Post Back to Slack"):
                                    try:
                                        slack_client.chat_postMessage(
                                            channel=channel_id, text=f"`{markdown}`"
                                        )
                                        st.success("✅ Posted to Slack!")
                                    except SlackApiError as e:
                                        st.error(f"❌ Failed to post to Slack: {e.response['error']}")

                            # Save to file
                            try:
                                output_file = save_report(markdown, config.output_dir)
                                st.info(f"Report saved to: {output_file}")
                            except OSError as e:
                                logger.error("Failed to save report: %s", e)
                                st.warning(f"Could not save to file: {e}")

                except Exception as e:
                    handle_error(e)

# Tab 3: View Past Reports
with tab3:
    st.subheader("Previous Reports")

    try:
        import glob

        report_pattern = str(Path(config.output_dir) / "*.md")
        reports = sorted(glob.glob(report_pattern), reverse=True)

        if reports:
            st.info(f"Found {len(reports)} saved reports")

            selected_report = st.selectbox(
                "Select a report to view:",
                reports,
                format_func=lambda x: Path(x).name,
            )

            if selected_report:
                content = Path(selected_report).read_text(encoding="utf-8")
                st.markdown("---")
                st.markdown(content)

                st.download_button(
                    label="📥 Download This Report",
                    data=content,
                    file_name=Path(selected_report).name,
                    mime="text/markdown",
                )
        else:
            st.warning("No reports found. Generate one first!")

    except Exception as e:
        handle_error(e)

# Sidebar
with st.sidebar:
    st.header("⚙️ Settings")
    st.markdown("**Status**")

    # Check API keys
    if config.has_anthropic():
        st.success("✅ Claude Connected")
    else:
        st.error("❌ Claude Key Missing")

    if config.has_slack():
        st.success("✅ Slack Connected")
    else:
        st.warning("⚠️ Slack Not Connected")

    st.markdown("---")
    st.markdown("**About**")
    st.markdown("AI-powered incident report generator using Claude")
    st.markdown("Transforms messy notes into structured documentation")
