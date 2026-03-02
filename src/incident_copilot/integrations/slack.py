"""Slack API integration for IT Incident Copilot."""

from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from typing import List, Dict
import logging

from incident_copilot.config import setup_logging, DEFAULT_MESSAGE_LIMIT
from incident_copilot.models import IncidentReport

logger = setup_logging(__name__)


class SlackIntegration:
    """Slack API integration for fetching and posting incident data."""

    def __init__(self, token: str) -> None:
        """Initialize Slack integration.

        Args:
            token: Slack bot OAuth token (xoxb-...).
        """
        self.client = WebClient(token=token)

    def fetch_messages(
        self, channel_id: str, limit: int = DEFAULT_MESSAGE_LIMIT
    ) -> List[Dict]:
        """Fetch messages from a Slack channel.

        Args:
            channel_id: Slack channel ID to fetch from.
            limit: Maximum number of messages to fetch.

        Returns:
            List[Dict]: List of message dictionaries.

        Raises:
            SlackApiError: If Slack API request fails.
        """
        logger.info("Fetching %d messages from channel %s", limit, channel_id)
        result = self.client.conversations_history(channel=channel_id, limit=limit)
        messages = result.get("messages", [])
        logger.info("Retrieved %d messages", len(messages))
        return messages

    def post_report(self, channel_id: str, report_markdown: str) -> None:
        """Post a formatted incident report back to a Slack channel.

        Args:
            channel_id: Slack channel ID to post to.
            report_markdown: Markdown-formatted incident report.

        Raises:
            SlackApiError: If Slack API request fails.
        """
        logger.info("Posting report to Slack channel %s", channel_id)
        self.client.chat_postMessage(channel=channel_id, text=f"`{report_markdown}`")
        logger.info("Report successfully posted to Slack")
