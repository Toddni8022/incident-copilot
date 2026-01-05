from openai import OpenAI
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

class TimelineEvent(BaseModel):
    timestamp: str
    event_description: str
    severity: Optional[str] = None

class ActionItem(BaseModel):
    task: str
    priority: str
    assigned_to: Optional[str] = None
    estimated_completion: Optional[str] = None

class IncidentReport(BaseModel):
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
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    
    def parse_incident(self, raw_input: str, model: str = "gpt-4o-2024-08-06") -> IncidentReport:
        """Transform messy incident notes into structured report using GPT-4 structured outputs"""
        
        system_prompt = """You are an expert IT incident analyst. Transform messy ticket notes, logs, or outage descriptions into a comprehensive structured incident report.

Extract and organize:
- Timeline events with timestamps (infer relative times if exact timestamps unavailable)
- Root cause analysis based on symptoms and error patterns
- Affected systems and services
- Impact assessment (users affected, downtime duration, business impact)
- Actionable next steps with priorities

Be concise but thorough. If information is missing, indicate it clearly rather than fabricating details."""

        response = self.client.beta.chat.completions.parse(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Analyze this incident:\n\n{raw_input}"}
            ],
            response_format=IncidentReport,
            temperature=0.3
        )
        
        return response.choices[0].message.parsed
    
    def format_markdown(self, report: IncidentReport) -> str:
        """Convert structured report to readable markdown"""
        
        md = f"""# Incident Report: {report.title}

## Executive Summary
{report.executive_summary}

## Affected Systems
{chr(10).join(f"- {system}" for system in report.affected_systems)}

## Timeline
{chr(10).join(f"**{event.timestamp}** - {event.event_description}" + (f" [{event.severity}]" if event.severity else "") for event in report.timeline)}

## Root Cause Analysis
{report.root_cause_hypothesis}

## Impact Assessment
{report.impact_assessment}

## Resolution
{report.resolution_summary}

## Action Items
{chr(10).join(f"{i+1}. **[{item.priority}]** {item.task}" + (f" (Assigned: {item.assigned_to})" if item.assigned_to else "") for i, item in enumerate(report.action_items))}
"""
        
        if report.related_incidents:
            md += f"\n## Related Incidents\n{chr(10).join(f'- {inc}' for inc in report.related_incidents)}"
        
        return md
