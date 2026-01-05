import os
from dataclasses import dataclass
from typing import Any, Dict, Optional

from openai import OpenAI


@dataclass
class IncidentReport:
    summary: str
    timeline: str
    impact: str
    root_cause: str
    action_items: str
    owners: str
    followups: str


class IncidentCopilot:
    """
    Parses an incident thread into a structured incident report using OpenAI.
    Reads OPENAI_API_KEY from environment automatically.
    """

    def __init__(self, model: str = "gpt-4o-mini"):
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise RuntimeError("Missing OPENAI_API_KEY in environment/.env")

        self.client = OpenAI(api_key=api_key)
        self.model = model

    def parse_incident(self, raw_text: str) -> IncidentReport:
        if not raw_text or not raw_text.strip():
            return IncidentReport(
                summary="No content provided.",
                timeline="",
                impact="",
                root_cause="",
                action_items="",
                owners="",
                followups="",
            )

        system = (
            "You are an incident management assistant. "
            "Turn messy Slack incident threads into a concise, actionable incident report."
        )

        prompt = f"""
Convert the incident thread into a structured report with these sections:

1) Summary (2-4 sentences)
2) Timeline (bullet list with timestamps if present)
3) Impact (who/what affected, severity)
4) Root Cause (best guess if unknown)
5) Action Items (bullets with clear tasks)
6) Owners (if inferable; otherwise 'TBD')
7) Follow-ups (questions / missing info)

Incident thread:
{raw_text}
""".strip()

        # Using Chat Completions style
        resp = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": prompt},
            ],
            temperature=0.2,
        )

        text = resp.choices[0].message.content or ""

        # Super-simple parsing: you can improve this later.
        # For now, format_markdown() will just wrap the model output.
        return IncidentReport(
            summary=text,
            timeline="",
            impact="",
            root_cause="",
            action_items="",
            owners="",
            followups="",
        )

    def format_markdown(self, report: IncidentReport) -> str:
        # If you later parse fields properly, render them nicely here.
        # For now, return the model output directly.
        return report.summary.strip()
