"""Shared pytest fixtures for IT Incident Copilot tests."""

import pytest
from unittest.mock import MagicMock, patch

from incident_copilot.config import Config
from incident_copilot.models import IncidentReport, TimelineEvent, ActionItem


@pytest.fixture
def mock_config(tmp_path):
    """Return a Config instance with dummy API keys and a temp output directory."""
    with patch.dict(
        "os.environ",
        {
            "OPENAI_API_KEY": "sk-test-key",
            "SLACK_BOT_TOKEN": "xoxb-test-token",
            "OUTPUT_DIR": str(tmp_path),
        },
    ):
        yield Config()


@pytest.fixture
def sample_incident_text():
    """Return a sample raw incident description."""
    return (
        "prod db slow, users reporting 500 errors on checkout page starting around 2:45pm\n"
        "checked logs - connection pool maxed out\n"
        "dave restarted db instance at 3:10\n"
        "errors stopped at 3:15\n"
        "looks like the marketing batch job ran during business hours\n"
        "need to fix cron schedule and add connection pool monitoring\n"
        "ticket #INC-8472"
    )


@pytest.fixture
def sample_report():
    """Return a fully populated IncidentReport instance."""
    return IncidentReport(
        incident_id="INC-8472",
        title="Production Database Connection Pool Exhaustion",
        executive_summary="The production database experienced connection pool exhaustion causing 500 errors.",
        affected_systems=["Production Database", "Checkout Service"],
        timeline=[
            TimelineEvent(
                timestamp="14:45",
                event_description="Users began reporting 500 errors on checkout page.",
                severity="critical",
            ),
            TimelineEvent(
                timestamp="15:10",
                event_description="Database restarted by Dave.",
                severity="info",
            ),
            TimelineEvent(
                timestamp="15:15",
                event_description="Errors resolved.",
                severity="info",
            ),
        ],
        root_cause_hypothesis="Marketing batch job ran during business hours exhausting the connection pool.",
        impact_assessment="Checkout page unavailable for ~30 minutes affecting all purchasing users.",
        resolution_summary="Database restarted, errors resolved. Root cause identified.",
        action_items=[
            ActionItem(task="Fix cron schedule for batch job", priority="high"),
            ActionItem(task="Add connection pool monitoring", priority="medium"),
            ActionItem(task="Increase pool size from 50 to 100", priority="low"),
        ],
    )
