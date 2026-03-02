"""Core incident parsing and report generation using OpenAI GPT-4."""

from openai import OpenAI, APIError, APIConnectionError, RateLimitError
from pydantic import ValidationError
from typing import Optional
import logging

from incident_copilot.config import Config, setup_logging
from incident_copilot.models import IncidentReport

# Setup logging
logger = setup_logging(__name__)


class IncidentCopilot:
    """AI-powered incident report generator using OpenAI GPT-4."""

    def __init__(self, config: Optional[Config] = None):
        """Initialize the incident copilot.

        Args:
            config: Optional configuration object. If not provided, uses default Config.

        Raises:
            ValueError: If OpenAI API key is not configured.
        """
        self.config = config or Config()
        self.config.validate_openai()
        self.client = OpenAI(api_key=self.config.openai_api_key)
        logger.info("IncidentCopilot initialized with model: %s", self.config.model)

    def parse_incident(
        self, raw_input: str, model: Optional[str] = None
    ) -> IncidentReport:
        """Transform messy incident notes into structured report using GPT-4.

        Args:
            raw_input: Raw incident text (tickets, logs, chat messages, etc.).
            model: Optional model override. Defaults to configured model.

        Returns:
            IncidentReport: Structured incident report with all fields populated.

        Raises:
            ValueError: If raw_input is empty or whitespace-only.
            APIConnectionError: If unable to connect to OpenAI API.
            RateLimitError: If OpenAI rate limit is exceeded.
            APIError: For other OpenAI API errors.
            ValidationError: If the API response doesn't match expected schema.
        """
        if not raw_input or not raw_input.strip():
            raise ValueError("Input cannot be empty. Please provide incident notes to analyze.")

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

Be concise but thorough. If information is missing, indicate it clearly rather than fabricating details."""

        try:
            response = self.client.beta.chat.completions.parse(
                model=model_name,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"Analyze this incident:\n\n{raw_input}"},
                ],
                response_format=IncidentReport,
                temperature=self.config.temperature,
            )

            parsed_report = response.choices[0].message.parsed
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
            action_items.append(f"{i}. **[{item.priority}]** {item.task}{assigned_tag}")
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
