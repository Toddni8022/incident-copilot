"""Core incident parsing and report generation using OpenAI GPT-4."""

from openai import OpenAI, APIError, APIConnectionError, RateLimitError
from pydantic import BaseModel, ValidationError
from typing import List, Optional, Literal
from config import Config, setup_logging


# Setup logging
logger = setup_logging(__name__)


class TimelineEvent(BaseModel):
    """Represents a single event in the incident timeline."""

    timestamp: str
    event_description: str
    severity: Optional[Literal["critical", "warning", "info"]] = None


class ActionItem(BaseModel):
    """Represents a follow-up action item from the incident."""

    task: str
    priority: Literal["high", "medium", "low"]
    assigned_to: Optional[str] = None
    estimated_completion: Optional[str] = None


class IncidentReport(BaseModel):
    """Complete structured incident report."""

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
    missing_information: Optional[List[str]] = None


class IncidentCopilot:
    """AI-powered incident report generator using OpenAI GPT-4."""

    def __init__(self, config: Optional[Config] = None):
        """Initialize the incident copilot."""

        self.config = config or Config()
        self.config.validate_openai()
        self.client = OpenAI(api_key=self.config.openai_api_key)

        logger.info("IncidentCopilot initialized with model: %s", self.config.model)

    def parse_incident(
        self, raw_input: str, model: Optional[str] = None
    ) -> IncidentReport:
        """Transform messy incident notes into a structured incident report."""

        if not raw_input or not raw_input.strip():
            raise ValueError(
                "Input cannot be empty. Please provide incident notes to analyze."
            )

        model_name = model or self.config.model

        logger.info(
            "Parsing incident with model: %s (input length: %d chars)",
            model_name,
            len(raw_input),
        )

        system_prompt = """You are an expert IT incident analyst. Transform messy ticket notes, logs, or outage descriptions into a comprehensive structured incident report.

Extract and organize:
- Timeline events with timestamps (infer relative times if exact timestamps unavailable)
- Root cause analysis based on symptoms and error patterns
- Affected systems and services
- Impact assessment (users affected, downtime duration, business impact)
- Actionable next steps with priorities
- Missing information that would help confirm the incident details

Be concise but thorough. If information is missing, indicate it clearly rather than fabricating details."""

        try:
            response = self.client.beta.chat.completions.parse(
                model=model_name,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {
                        "role": "user",
                        "content": f"Analyze this incident:\n\n{raw_input}",
                    },
                ],
                response_format=IncidentReport,
                temperature=self.config.temperature,
            )

            parsed_report = response.choices[0].message.parsed

            if parsed_report is None:
                raise ValueError("OpenAI returned no parsed incident report.")

            logger.info("Successfully parsed incident: %s", parsed_report.title)
            return parsed_report

        except APIConnectionError as e:
            logger.error("Failed to connect to OpenAI API: %s", e)
            raise APIConnectionError(
                "Unable to connect to OpenAI API. Please check your internet connection."
            ) from e

        except RateLimitError as e:
            logger.error("OpenAI rate limit exceeded: %s", e)
            raise RateLimitError(
                "OpenAI rate limit exceeded. Please try again later."
            ) from e

        except APIError as e:
            logger.error("OpenAI API error: %s", e)
            raise

        except ValidationError as e:
            logger.error("Failed to validate API response: %s", e)
            raise ValueError(
                "Received invalid structured response from OpenAI API. Please try again."
            ) from e

    def format_markdown(self, report: IncidentReport) -> str:
        """Convert structured report to readable markdown format."""

        if report is None:
            raise ValueError("Report cannot be None")

        logger.debug("Formatting report to markdown: %s", report.title)

        # Build affected systems section
        systems_text = (
            "\n".join(f"- {system}" for system in report.affected_systems)
            or "_No affected systems provided._"
        )

        # Build timeline section
        timeline_items = []

        for event in report.timeline:
            severity_tag = f" [{event.severity}]" if event.severity else ""
            timeline_items.append(
                f"**{event.timestamp}** - {event.event_description}{severity_tag}"
            )

        timeline_text = "\n".join(timeline_items) or "_No timeline events provided._"

        # Build action items section
        action_items = []

        for i, item in enumerate(report.action_items, 1):
            assigned_tag = (
                f" (Assigned: {item.assigned_to})" if item.assigned_to else ""
            )
            completion_tag = (
                f" (Estimated completion: {item.estimated_completion})"
                if item.estimated_completion
                else ""
            )

            action_items.append(
                f"{i}. **[{item.priority}]** {item.task}{assigned_tag}{completion_tag}"
            )

        action_items_text = "\n".join(action_items) or "_No action items provided._"

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
            md += f"\n## Related Incidents\n{related_text}\n"

        # Add optional missing information section
        if report.missing_information:
            missing_text = "\n".join(f"- {item}" for item in report.missing_information)
            md += f"\n## Missing Information\n{missing_text}\n"

        return md
