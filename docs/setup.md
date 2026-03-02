# Setup Guide

This guide walks you through setting up IT Incident Copilot from scratch.

## Prerequisites

- Python 3.11 or higher
- pip (Python package manager)
- An OpenAI API key ([create one here](https://platform.openai.com/api-keys))
- (Optional) A Slack workspace with a bot token for live channel analysis

---

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/your-org/incident-copilot.git
cd incident-copilot
```

### 2. Create a virtual environment

```bash
python -m venv .venv
source .venv/bin/activate      # Linux / macOS
.venv\Scripts\activate         # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

Or install the package in editable mode:

```bash
pip install -e .
```

### 4. Configure environment variables

Copy the example environment file and fill in your credentials:

```bash
cp .env.example .env
```

Edit `.env`:

```
OPENAI_API_KEY=sk-your-openai-key
SLACK_BOT_TOKEN=xoxb-your-slack-bot-token   # optional
```

---

## Running the Application

### Web UI (Streamlit)

```bash
streamlit run app.py
# or using the package
streamlit run src/incident_copilot/app.py
```

The dashboard opens at `http://localhost:8501` by default.

### Command-line interface

```bash
# Analyze a ticket file
python main.py data/examples/sample_ticket.txt

# Pipe raw text
echo "db down, users getting 500s since 3pm" | python main.py
```

### Manual Slack analysis

```bash
python slack_manual.py
```

---

## Docker

See [Docker Compose](#docker-compose) or refer to the `Dockerfile` and `docker-compose.yml` in the project root.

```bash
docker compose up
```

---

## Environment Variables

| Variable | Required | Default | Description |
|---|---|---|---|
| `OPENAI_API_KEY` | Yes | — | OpenAI API key |
| `SLACK_BOT_TOKEN` | No | — | Slack bot OAuth token |
| `MODEL` | No | `gpt-4o-2024-08-06` | OpenAI model to use |
| `OUTPUT_DIR` | No | `output` | Directory for saved reports |
| `TEMPERATURE` | No | `0.3` | Model temperature |
| `LOG_LEVEL` | No | `INFO` | Logging verbosity |
