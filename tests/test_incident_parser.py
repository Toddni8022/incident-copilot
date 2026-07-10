import pytest

from incident_parser import ActionItem, IncidentCopilot, IncidentReport, TimelineEvent


def sample_report() -> IncidentReport:
    return IncidentReport(
        title="Checkout errors",
        executive_summary="Checkout returned HTTP 500 responses.",
        affected_systems=["checkout", "database"],
        timeline=[TimelineEvent(timestamp="14:45", event_description="Errors started", severity="critical")],
        root_cause_hypothesis="Connection pool exhaustion correlated with a batch job.",
        impact_assessment="Checkout requests failed.",
        resolution_summary="Database was restarted.",
        action_items=[ActionItem(task="Correct the schedule", priority="high", assigned_to="Dave")],
        missing_information=["Number of affected users"],
    )


def test_format_markdown_includes_validated_sections():
    copilot = object.__new__(IncidentCopilot)
    markdown = copilot.format_markdown(sample_report())

    assert "# Incident Report: Checkout errors" in markdown
    assert "**14:45** - Errors started [critical]" in markdown
    assert "Number of affected users" in markdown


def test_report_rejects_unknown_priority():
    with pytest.raises(ValueError):
        ActionItem(task="Do work", priority="urgent")


def test_parse_rejects_blank_input_before_api_call():
    copilot = object.__new__(IncidentCopilot)
    with pytest.raises(ValueError, match="Input cannot be empty"):
        copilot.parse_incident("  ")
