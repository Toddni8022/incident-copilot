"""Data models for IT Incident Copilot."""

from pydantic import BaseModel
from typing import List, Optional


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
