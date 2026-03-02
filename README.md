# 🚨 IT Incident Copilot

![Python](https://img.shields.io/badge/python-3.11%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![CI](https://github.com/Toddni8022/incident-copilot/actions/workflows/ci.yml/badge.svg)

An AI-powered IT incident analysis tool that transforms messy incident tickets and raw Slack conversations into clean, professional incident reports. Built for SOC teams, IT ops, and incident responders who need fast, structured analysis without the manual work.

---

## Overview

IT Incident Copilot connects to your Slack workspace, reads incident channel history, and uses GPT-4 to produce a fully structured report — complete with a timeline, root cause hypothesis, affected systems, impact assessment, and prioritised action items.

---

## Features

- **Slack integration** — fetch messages directly from any channel
- **AI-powered analysis** — GPT-4 structured output via OpenAI SDK
- **Incident parsing** — timeline reconstruction, root cause analysis, action items
- **Streamlit dashboard** — interactive web UI for analysis and report history
- **CLI support** — pipe text or pass a file for headless use
- **Markdown reports** — download or post reports back to Slack
- **Pydantic validation** — schema-enforced responses, no hallucinated fields

---

## Architecture

```
Slack Channel / Raw Text
        │
        ▼
  IT Incident Copilot
  ┌─────────────────────────────┐
  │  IncidentCopilot (parser)   │ ──► OpenAI GPT-4
  │  SlackIntegration           │ ──► Slack API
  │  Streamlit UI / CLI         │
  └─────────────────────────────┘
        │
        ▼
  Structured IncidentReport
  (title, timeline, root cause,
   affected systems, action items)
        │
        ▼
  Markdown Report (download / Slack post)
```

---

## Prerequisites

- Python 3.11+
- An [OpenAI API key](https://platform.openai.com/api-keys)
- (Optional) A Slack workspace with a [bot token](docs/slack_setup.md)

---

## Quick Start

```bash
# 1. Clone and enter the repo
git clone https://github.com/Toddni8022/incident-copilot.git
cd incident-copilot

# 2. Create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure environment
cp .env.example .env
# Edit .env and add your OPENAI_API_KEY

# 5. Run the web UI
streamlit run app.py
```

Open [http://localhost:8501](http://localhost:8501) in your browser.

---

## Installation (package)

```bash
pip install -e .
```

---

## Usage

### Web UI

```bash
streamlit run app.py
```

- **Text Input** tab — paste raw notes and click **Generate Report**
- **Slack Channel** tab — enter a channel ID and click **Fetch & Analyze**
- **View Reports** tab — browse and download saved reports

### CLI

```bash
# Analyze a file
python main.py data/examples/sample_ticket.txt

# Pipe text directly
echo "db down, 500s on checkout since 3pm" | python main.py
```

### Manual Slack script

```bash
python slack_manual.py
```

---

## Configuration

Copy `.env.example` to `.env` and set values:

| Variable | Required | Default | Description |
|---|---|---|---|
| `OPENAI_API_KEY` | **Yes** | — | OpenAI API key |
| `SLACK_BOT_TOKEN` | No | — | Slack bot OAuth token (`xoxb-...`) |
| `MODEL` | No | `gpt-4o-2024-08-06` | OpenAI model |
| `OUTPUT_DIR` | No | `output` | Report save directory |
| `TEMPERATURE` | No | `0.3` | Model temperature |
| `LOG_LEVEL` | No | `INFO` | Logging level |

---

## Slack Setup

See [docs/slack_setup.md](docs/slack_setup.md) for step-by-step instructions to create and configure a Slack app.

---

## Project Structure

```
incident-copilot/
├── src/
│   └── incident_copilot/       ← installable Python package
│       ├── app.py              ← Streamlit UI
│       ├── config.py           ← configuration
│       ├── models.py           ← Pydantic data models
│       ├── utils.py            ← shared utilities
│       ├── parser/
│       │   └── incident_parser.py
│       └── integrations/
│           └── slack.py
├── tests/                      ← pytest test suite
├── data/examples/              ← sample incident tickets
├── docs/                       ← documentation
├── app.py                      ← Streamlit entry point
├── main.py                     ← CLI entry point
├── Dockerfile
├── docker-compose.yml
├── pyproject.toml
└── Makefile
```

---

## Docker

```bash
# Build and run with Docker Compose
docker compose up
```

The app will be available at [http://localhost:8501](http://localhost:8501).

---

## Development

```bash
# Install dev dependencies
make setup

# Run tests
make test

# Lint and format
make lint
make format

# All checks (lint + typecheck + test)
make check
```

---

## API Reference

See [docs/api.md](docs/api.md) for the Python API reference.

---

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

---

## License

[MIT](LICENSE)
