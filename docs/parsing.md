# How Incident Parsing Works

IT Incident Copilot transforms raw, unstructured incident text into a structured `IncidentReport` using OpenAI's structured output feature with Pydantic schema validation.

---

## Data Flow

```
Raw Input (text / Slack messages)
        │
        ▼
  Input Validation
        │
        ▼
  OpenAI GPT-4 (structured output)
        │
        ▼
  Pydantic IncidentReport validation
        │
        ▼
  Markdown Formatting
        │
        ▼
  Display / Save / Post to Slack
```

---

## Data Models

### `IncidentReport`

The top-level model returned by the parser.

| Field | Type | Description |
|---|---|---|
| `incident_id` | `str \| None` | Optional ticket/incident ID |
| `title` | `str` | Short incident title |
| `executive_summary` | `str` | High-level overview |
| `affected_systems` | `List[str]` | Impacted services |
| `timeline` | `List[TimelineEvent]` | Ordered sequence of events |
| `root_cause_hypothesis` | `str` | Probable root cause |
| `impact_assessment` | `str` | Business/user impact |
| `resolution_summary` | `str` | How it was resolved |
| `action_items` | `List[ActionItem]` | Follow-up tasks |
| `related_incidents` | `List[str] \| None` | Related incident IDs |

### `TimelineEvent`

| Field | Type | Description |
|---|---|---|
| `timestamp` | `str` | Time string (e.g. "14:45") |
| `event_description` | `str` | What happened |
| `severity` | `str \| None` | e.g. "critical", "warning" |

### `ActionItem`

| Field | Type | Description |
|---|---|---|
| `task` | `str` | Task description |
| `priority` | `str` | "high", "medium", or "low" |
| `assigned_to` | `str \| None` | Person or team |
| `estimated_completion` | `str \| None` | Completion estimate |

---

## System Prompt

The parser uses the following system prompt:

> You are an expert IT incident analyst. Transform messy ticket notes, logs, or outage descriptions into a comprehensive structured incident report.
>
> Extract and organize:
> - Timeline events with timestamps
> - Root cause analysis
> - Affected systems and services
> - Impact assessment
> - Actionable next steps with priorities

---

## Structured Output

The `openai` Python SDK's `beta.chat.completions.parse` endpoint is used with `response_format=IncidentReport` to guarantee the response matches the Pydantic schema. This eliminates JSON parsing errors and hallucinated fields.

---

## Error Handling

| Exception | Cause | Behaviour |
|---|---|---|
| `ValueError` | Empty input | Raised before API call |
| `APIConnectionError` | Network failure | Re-raised with user-friendly message |
| `RateLimitError` | OpenAI rate limit | Re-raised with retry advice |
| `APIError` | Other OpenAI error | Re-raised as-is |
| `ValidationError` | Schema mismatch | Re-raised |
