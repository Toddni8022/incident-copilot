"""Tests for incident parsing and report formatting."""

import pytest
from unittest.mock import MagicMock, patch

from incident_copilot.models import IncidentReport, TimelineEvent, ActionItem
from incident_copilot.parser.incident_parser import IncidentCopilot


class TestIncidentCopilotInit:
    """Tests for IncidentCopilot initialization."""

    def test_raises_without_api_key(self, tmp_path):
        """IncidentCopilot raises ValueError when OPENAI_API_KEY is missing."""
        with patch.dict("os.environ", {"OPENAI_API_KEY": "", "OUTPUT_DIR": str(tmp_path)}):
            from incident_copilot.config import Config

            config = Config()
        with pytest.raises(ValueError, match="OPENAI_API_KEY"):
            IncidentCopilot(config)

    def test_initializes_with_valid_config(self, mock_config):
        """IncidentCopilot initializes successfully with a valid config."""
        with patch("incident_copilot.parser.incident_parser.OpenAI"):
            copilot = IncidentCopilot(mock_config)
        assert copilot.config is mock_config


class TestParseIncident:
    """Tests for IncidentCopilot.parse_incident."""

    def test_raises_on_empty_input(self, mock_config):
        """parse_incident raises ValueError for empty input."""
        with patch("incident_copilot.parser.incident_parser.OpenAI"):
            copilot = IncidentCopilot(mock_config)
        with pytest.raises(ValueError, match="empty"):
            copilot.parse_incident("")

    def test_raises_on_whitespace_input(self, mock_config):
        """parse_incident raises ValueError for whitespace-only input."""
        with patch("incident_copilot.parser.incident_parser.OpenAI"):
            copilot = IncidentCopilot(mock_config)
        with pytest.raises(ValueError, match="empty"):
            copilot.parse_incident("   \n  ")

    def test_returns_incident_report(self, mock_config, sample_report, sample_incident_text):
        """parse_incident returns an IncidentReport for valid input."""
        mock_openai = MagicMock()
        mock_response = MagicMock()
        mock_response.choices[0].message.parsed = sample_report
        mock_openai.return_value.beta.chat.completions.parse.return_value = mock_response

        with patch("incident_copilot.parser.incident_parser.OpenAI", mock_openai):
            copilot = IncidentCopilot(mock_config)
            result = copilot.parse_incident(sample_incident_text)

        assert isinstance(result, IncidentReport)
        assert result.title == sample_report.title


class TestFormatMarkdown:
    """Tests for IncidentCopilot.format_markdown."""

    def test_raises_on_none(self, mock_config):
        """format_markdown raises ValueError when report is None."""
        with patch("incident_copilot.parser.incident_parser.OpenAI"):
            copilot = IncidentCopilot(mock_config)
        with pytest.raises(ValueError, match="None"):
            copilot.format_markdown(None)

    def test_contains_title(self, mock_config, sample_report):
        """format_markdown output contains the incident title."""
        with patch("incident_copilot.parser.incident_parser.OpenAI"):
            copilot = IncidentCopilot(mock_config)
        md = copilot.format_markdown(sample_report)
        assert sample_report.title in md

    def test_contains_all_sections(self, mock_config, sample_report):
        """format_markdown output contains all standard report sections."""
        with patch("incident_copilot.parser.incident_parser.OpenAI"):
            copilot = IncidentCopilot(mock_config)
        md = copilot.format_markdown(sample_report)

        for section in [
            "Executive Summary",
            "Affected Systems",
            "Timeline",
            "Root Cause Analysis",
            "Impact Assessment",
            "Resolution",
            "Action Items",
        ]:
            assert section in md, f"Missing section: {section}"

    def test_timeline_events_formatted(self, mock_config, sample_report):
        """format_markdown includes timeline event timestamps and descriptions."""
        with patch("incident_copilot.parser.incident_parser.OpenAI"):
            copilot = IncidentCopilot(mock_config)
        md = copilot.format_markdown(sample_report)
        assert "14:45" in md
        assert "15:10" in md

    def test_action_items_numbered(self, mock_config, sample_report):
        """format_markdown numbers action items."""
        with patch("incident_copilot.parser.incident_parser.OpenAI"):
            copilot = IncidentCopilot(mock_config)
        md = copilot.format_markdown(sample_report)
        assert "1." in md
        assert "2." in md

    def test_severity_tag_included(self, mock_config, sample_report):
        """format_markdown includes severity tags when present."""
        with patch("incident_copilot.parser.incident_parser.OpenAI"):
            copilot = IncidentCopilot(mock_config)
        md = copilot.format_markdown(sample_report)
        assert "[critical]" in md

    def test_related_incidents_section_when_present(self, mock_config, sample_report):
        """format_markdown adds Related Incidents section when field is set."""
        sample_report.related_incidents = ["INC-1234"]
        with patch("incident_copilot.parser.incident_parser.OpenAI"):
            copilot = IncidentCopilot(mock_config)
        md = copilot.format_markdown(sample_report)
        assert "Related Incidents" in md
        assert "INC-1234" in md

    def test_no_related_incidents_section_when_absent(self, mock_config, sample_report):
        """format_markdown omits Related Incidents section when field is None."""
        sample_report.related_incidents = None
        with patch("incident_copilot.parser.incident_parser.OpenAI"):
            copilot = IncidentCopilot(mock_config)
        md = copilot.format_markdown(sample_report)
        assert "Related Incidents" not in md
