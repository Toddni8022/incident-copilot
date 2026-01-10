"""Core incident parsing and report generation using Claude API."""

import json
from anthropic import Anthropic, APIError, APIConnectionError, RateLimitError
from pydantic import BaseModel, ValidationError
from typing import List, Optional
import logging
from config import Config, setup_logging, DEFAULT_MODEL

# Setup logging
logger = setup_logging(__name__)


class TimelineEvent(BaseModel):
    """Represents a single event in the incident timeline.

    Attributes:
        timestamp: When the event occurred (e.g., "14:45", "2024-01-08 14:45").
        event_description: What happened during this event.
        severity: Optional severity level (e.g., "critical", "warning", "info").
    """

    timestamp: str
    event_description: str
    severity: Optional[str] = None


class ActionItem(BaseModel):
    """Represents a follow-up action item from the incident.

    Attributes:
        task: Description of the action to be taken.
        priority: Priority level (e.g., "high", "medium", "low").
        assigned_to: Optional person or team assigned to this task.
        estimated_completion: Optional estimated completion date/time.
    """

    task: str
    priority: str
    assigned_to: Optional[str] = None
    estimated_completion: Optional[str] = None


class IncidentReport(BaseModel):
    """Complete structured incident report.

    Attributes:
        incident_id: Optional incident tracking ID.
        title: Brief title summarizing the incident.
        executive_summary: High-level overview of the incident.
        affected_systems: List of systems/services impacted.
        timeline: Chronological sequence of events.
        root_cause_hypothesis: Analysis of what caused the incident.
        impact_assessment: Description of business/user impact.
        resolution_summary: How the incident was resolved.
        action_items: Follow-up tasks and improvements.
        related_incidents: Optional list of related incident IDs.
    """

    incident_id: Optional[str] = None
    title: str
    executive_summary: str
    affected_systems: List[str]
    timeline: List[TimelineEvent]
    root_cause_hypothesis: str
    impact_assessment: str
    resolution_summary: str
    action_items: List[ActionItem]
    related_incidents: Optional[List[str]] = None


class IncidentCopilot:
    """AI-powered incident report generator using Claude API."""

    def __init__(self, config: Optional[Config] = None):
        """Initialize the incident copilot.

        Args:
            config: Optional configuration object. If not provided, uses default Config.

        Raises:
            ValueError: If Anthropic API key is not configured.
        """
        self.config = config or Config()
        self.config.validate_anthropic()
        self.client = Anthropic(api_key=self.config.anthropic_api_key)
        logger.info("IncidentCopilot initialized with model: %s", self.config.model)

    def parse_incident(
        self, raw_input: str, model: Optional[str] = None
    ) -> IncidentReport:
        """Transform messy incident notes into structured report using Claude.

        Args:
            raw_input: Raw incident text (tickets, logs, chat messages, etc.).
            model: Optional model override. Defaults to configured model.

        Returns:
            IncidentReport: Structured incident report with all fields populated.

        Raises:
            ValueError: If raw_input is empty or whitespace-only.
            APIConnectionError: If unable to connect to Anthropic API.
            RateLimitError: If Anthropic rate limit is exceeded.
            APIError: For other Anthropic API errors.
            ValidationError: If the API response doesn't match expected schema.
        """
        # Input validation
        if not raw_input or not raw_input.strip():
            raise ValueError("Input cannot be empty. Please provide incident notes to analyze.")

        model_name = model or self.config.model
        logger.info("Parsing incident with model: %s (input length: %d chars)", model_name, len(raw_input))

        system_prompt = """You are an expert IT incident analyst. Transform messy ticket notes, logs, or outage descriptions into a comprehensive structured incident report.

Extract and organize:
- Timeline events with timestamps (infer relative times if exact timestamps unavailable)
- Root cause analysis based on symptoms and error patterns
- Affected systems and services
- Impact assessment (users affected, downtime duration, business impact)
- Actionable next steps with priorities

Be concise but thorough. If information is missing, indicate it clearly rather than fabricating details.

You MUST respond with valid JSON in this exact format:
{
  "incident_id": "string or null",
  "title": "string",
  "executive_summary": "string",
  "affected_systems": ["string"],
  "timeline": [
    {
      "timestamp": "string",
      "event_description": "string",
      "severity": "string or null"
    }
  ],
  "root_cause_hypothesis": "string",
  "impact_assessment": "string",
  "resolution_summary": "string",
  "action_items": [
    {
      "task": "string",
      "priority": "string",
      "assigned_to": "string or null",
      "estimated_completion": "string or null"
    }
  ],
  "related_incidents": ["string"] or null
}

Only return the JSON object, nothing else."""

        user_prompt = f"Analyze this incident and return a JSON report:\n\n{raw_input}"

        try:
            response = self.client.messages.create(
                model=model_name,
                max_tokens=self.config.max_tokens,
                temperature=self.config.temperature,
                system=system_prompt,
                messages=[
                    {"role": "user", "content": user_prompt}
                ],
            )

            # Extract text content from response
            response_text = response.content[0].text

            # Parse JSON response
            try:
                json_data = json.loads(response_text)
                parsed_report = IncidentReport(**json_data)
                logger.info("Successfully parsed incident: %s", parsed_report.title)
                return parsed_report
            except json.JSONDecodeError as e:
                logger.error("Failed to parse JSON from Claude response: %s", e)
                logger.debug("Response text: %s", response_text)
                raise ValidationError(
                    f"Claude returned invalid JSON. Please try again."
                ) from e

        except APIConnectionError as e:
            logger.error("Failed to connect to Anthropic API: %s", e)
            raise APIConnectionError(
                "Unable to connect to Anthropic API. Please check your internet connection."
            ) from e
        except RateLimitError as e:
            logger.error("Anthropic rate limit exceeded: %s", e)
            raise RateLimitError(
                "Anthropic rate limit exceeded. Please try again later."
            ) from e
        except APIError as e:
            logger.error("Anthropic API error: %s", e)
            raise
        except ValidationError as e:
            logger.error("Failed to validate API response: %s", e)
            raise

    def format_markdown(self, report: IncidentReport) -> str:
        """Convert structured report to readable markdown format.

        Args:
            report: Structured incident report to format.

        Returns:
            str: Markdown-formatted report ready for display or saving.

        Raises:
            ValueError: If report is None.
        """
        if report is None:
            raise ValueError("Report cannot be None")

        logger.debug("Formatting report to markdown: %s", report.title)

        # Build timeline section
        timeline_items = []
        for event in report.timeline:
            severity_tag = f" [{event.severity}]" if event.severity else ""
            timeline_items.append(
                f"**{event.timestamp}** - {event.event_description}{severity_tag}"
            )
        timeline_text = "\n".join(timeline_items)

        # Build action items section
        action_items = []
        for i, item in enumerate(report.action_items, 1):
            assigned_tag = f" (Assigned: {item.assigned_to})" if item.assigned_to else ""
            action_items.append(
                f"{i}. **[{item.priority}]** {item.task}{assigned_tag}"
            )
        action_items_text = "\n".join(action_items)

        # Build affected systems section
        systems_text = "\n".join(f"- {system}" for system in report.affected_systems)

        # Build main markdown
        md = f"""# Incident Report: {report.title}

## Executive Summary
{report.executive_summary}

## Affected Systems
{systems_text}

## Timeline
{timeline_text}

## Root Cause Analysis
{report.root_cause_hypothesis}

## Impact Assessment
{report.impact_assessment}

## Resolution
{report.resolution_summary}

## Action Items
{action_items_text}
"""

        # Add optional related incidents section
        if report.related_incidents:
            related_text = "\n".join(f"- {inc}" for inc in report.related_incidents)
            md += f"\n## Related Incidents\n{related_text}"

        return md
