"""Tests for Slack integration."""

import pytest
from unittest.mock import MagicMock, patch

from incident_copilot.integrations.slack import SlackIntegration
from incident_copilot.utils import combine_messages


class TestCombineMessages:
    """Tests for the combine_messages utility."""

    def test_combines_text_fields(self):
        """combine_messages joins text fields with newlines."""
        messages = [{"text": "hello"}, {"text": "world"}]
        result = combine_messages(messages)
        assert result == "hello\nworld"

    def test_skips_messages_without_text(self):
        """combine_messages skips messages that lack a 'text' key."""
        messages = [{"text": "hello"}, {"user": "dave"}, {"text": "bye"}]
        result = combine_messages(messages)
        assert result == "hello\nbye"

    def test_returns_empty_string_for_no_messages(self):
        """combine_messages returns empty string for empty list."""
        assert combine_messages([]) == ""

    def test_returns_empty_string_for_messages_without_text(self):
        """combine_messages returns empty string when no messages have text."""
        messages = [{"user": "alice"}, {"ts": "123"}]
        assert combine_messages(messages) == ""


class TestSlackIntegration:
    """Tests for the SlackIntegration class."""

    def _make_integration(self, token: str = "xoxb-test") -> SlackIntegration:
        with patch("incident_copilot.integrations.slack.WebClient"):
            integration = SlackIntegration(token=token)
        return integration

    def test_fetch_messages_returns_list(self):
        """fetch_messages returns the messages list from the API response."""
        with patch("incident_copilot.integrations.slack.WebClient") as mock_wc:
            mock_client = MagicMock()
            mock_client.conversations_history.return_value = {
                "messages": [{"text": "msg1"}, {"text": "msg2"}]
            }
            mock_wc.return_value = mock_client
            integration = SlackIntegration(token="xoxb-test")

        messages = integration.fetch_messages("C1234", limit=10)
        assert messages == [{"text": "msg1"}, {"text": "msg2"}]
        mock_client.conversations_history.assert_called_once_with(channel="C1234", limit=10)

    def test_fetch_messages_returns_empty_on_no_messages(self):
        """fetch_messages returns empty list when API returns no messages."""
        with patch("incident_copilot.integrations.slack.WebClient") as mock_wc:
            mock_client = MagicMock()
            mock_client.conversations_history.return_value = {}
            mock_wc.return_value = mock_client
            integration = SlackIntegration(token="xoxb-test")

        messages = integration.fetch_messages("C1234", limit=10)
        assert messages == []

    def test_post_report_calls_chat_post(self):
        """post_report calls chat_postMessage with the formatted report."""
        with patch("incident_copilot.integrations.slack.WebClient") as mock_wc:
            mock_client = MagicMock()
            mock_wc.return_value = mock_client
            integration = SlackIntegration(token="xoxb-test")

        integration.post_report("C1234", "## Report Content")
        mock_client.chat_postMessage.assert_called_once_with(
            channel="C1234", text="`## Report Content`"
        )
