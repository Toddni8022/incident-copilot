# API Reference

IT Incident Copilot exposes a Streamlit web interface. There is no standalone REST API; the application is designed to be run locally or within a trusted network.

---

## Web Interface Tabs

### Tab 1 — Text Input

| Element | Description |
|---|---|
| Text area | Paste raw incident notes, ticket text, or chat logs |
| **Generate Report** button | Sends text to OpenAI and renders the structured report |
| **Download Report** button | Downloads the report as a `.md` file |

### Tab 2 — Slack Channel

| Element | Description |
|---|---|
| Channel ID input | Slack channel ID (e.g. `C01234ABCDE`) |
| Message limit slider | How many recent messages to fetch (10–100) |
| **Fetch & Analyze** button | Fetches messages from Slack, runs analysis |
| **Post Back to Slack** button | Posts the generated report to the same channel |

### Tab 3 — View Reports

| Element | Description |
|---|---|
| Report selector | Dropdown of all previously saved `.md` reports |
| Report viewer | Rendered markdown of the selected report |
| **Download This Report** | Downloads the selected report |

---

## Python API

### `IncidentCopilot`

```python
from incident_copilot.parser.incident_parser import IncidentCopilot
from incident_copilot.config import Config

config = Config()
copilot = IncidentCopilot(config)

report = copilot.parse_incident("prod db down since 3pm, 500 errors")
markdown = copilot.format_markdown(report)
```

#### `parse_incident(raw_input, model=None) → IncidentReport`

- **raw_input** `str` — Raw incident text
- **model** `str | None` — Override the model (default: `gpt-4o-2024-08-06`)
- Returns: `IncidentReport` Pydantic model
- Raises: `ValueError`, `APIConnectionError`, `RateLimitError`, `APIError`, `ValidationError`

#### `format_markdown(report) → str`

- **report** `IncidentReport` — Structured report
- Returns: Markdown-formatted string
- Raises: `ValueError` if report is `None`

---

### `SlackIntegration`

```python
from incident_copilot.integrations.slack import SlackIntegration

slack = SlackIntegration(token="xoxb-...")
messages = slack.fetch_messages("C01234ABCDE", limit=50)
slack.post_report("C01234ABCDE", markdown)
```

#### `fetch_messages(channel_id, limit=50) → List[Dict]`

- **channel_id** `str` — Slack channel ID
- **limit** `int` — Max messages to return
- Returns: List of Slack message dicts

#### `post_report(channel_id, report_markdown) → None`

- **channel_id** `str` — Channel to post to
- **report_markdown** `str` — Formatted report content

---

### `Config`

```python
from incident_copilot.config import Config

config = Config()
config.validate_openai()   # raises ValueError if key missing
config.has_openai()        # bool
config.has_slack()         # bool
```

---

### `utils`

```python
from incident_copilot.utils import save_report, combine_messages

path = save_report(markdown, output_dir)
text = combine_messages(slack_messages)
```
