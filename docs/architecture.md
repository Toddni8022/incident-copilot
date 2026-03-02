# System Architecture

## Overview

IT Incident Copilot is a Python application with two user-facing interfaces:

1. **Streamlit Web Dashboard** — interactive UI for pasting text or fetching Slack channels
2. **CLI** — pipe incident text or pass a file path for headless use

Both interfaces share the same core parsing pipeline.

---

## Component Diagram

```
┌─────────────────────────────────────────────────────────┐
│                      User Interfaces                    │
│                                                         │
│  ┌─────────────────┐       ┌──────────────────────┐    │
│  │  Streamlit UI   │       │   CLI (main.py)       │    │
│  │  (app.py)       │       │                       │    │
│  └────────┬────────┘       └──────────┬────────────┘    │
│           │                           │                  │
└───────────┼───────────────────────────┼──────────────────┘
            │                           │
            ▼                           ▼
┌─────────────────────────────────────────────────────────┐
│                   Core Package                          │
│   src/incident_copilot/                                 │
│                                                         │
│  ┌──────────────────────────────────────────────────┐  │
│  │              parser/incident_parser.py            │  │
│  │              IncidentCopilot                      │  │
│  │  - parse_incident(raw_text) → IncidentReport      │  │
│  │  - format_markdown(report) → str                  │  │
│  └───────────────────┬──────────────────────────────┘  │
│                      │                                  │
│  ┌───────────────────┼──────────────────────────────┐  │
│  │   models.py       │   config.py    utils.py       │  │
│  │   IncidentReport  │   Config       save_report     │  │
│  │   TimelineEvent   │   setup_logging combine_msgs   │  │
│  │   ActionItem      │                               │  │
│  └───────────────────┴──────────────────────────────┘  │
│                                                         │
│  ┌──────────────────────────────────────────────────┐  │
│  │  integrations/slack.py                            │  │
│  │  SlackIntegration                                 │  │
│  │  - fetch_messages(channel_id) → List[Dict]        │  │
│  │  - post_report(channel_id, markdown)              │  │
│  └──────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────┘
            │                           │
            ▼                           ▼
    ┌───────────────┐         ┌─────────────────┐
    │  OpenAI API   │         │   Slack API      │
    │  GPT-4        │         │   (WebClient)    │
    └───────────────┘         └─────────────────┘
```

---

## Directory Structure

```
incident-copilot/
├── src/
│   └── incident_copilot/       ← installable Python package
│       ├── __init__.py
│       ├── app.py              ← Streamlit UI
│       ├── config.py           ← env-based configuration
│       ├── models.py           ← Pydantic data models
│       ├── utils.py            ← shared utilities
│       ├── parser/
│       │   ├── __init__.py
│       │   └── incident_parser.py  ← OpenAI parsing logic
│       └── integrations/
│           ├── __init__.py
│           └── slack.py        ← Slack SDK wrapper
├── tests/                      ← pytest test suite
├── data/examples/              ← sample incident tickets
├── docs/                       ← documentation
├── app.py                      ← root entry point (Streamlit)
├── main.py                     ← root entry point (CLI)
└── slack_manual.py             ← root entry point (Slack CLI)
```

---

## Key Design Decisions

| Decision | Rationale |
|---|---|
| Pydantic structured output | Eliminates JSON parsing errors; enforces schema at the SDK level |
| Streamlit for UI | Zero-boilerplate dashboard; suitable for internal tooling |
| `src/` layout | Prevents accidental imports of the package before installation |
| Environment-based config | Follows 12-factor app principles; no secrets in code |
| Optional Slack | App works fully with text input; Slack is additive |
