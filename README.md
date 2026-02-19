# Incident Copilot

An AI-powered IT incident analysis tool that transforms messy incident tickets and raw Slack conversations into clean, professional incident reports. Built for SOC teams, IT ops, and incident responders who need fast, structured analysis without the manual work.

---

## What It Does

- **Monitors Slack** in real time for incident-related conversations
- **Parses incident tickets** and unstructured log data
- **Uses GPT-4** to categorize, analyze, and summarize incidents
- **Generates professional reports** with executive summaries, timelines, and action items
- **Streamlit dashboard** for viewing and managing incident history

---

## Features

- Real-time Slack channel monitoring via Slack SDK
- AI-driven incident categorization and severity scoring
- Automated executive summaries
- Timeline reconstruction from fragmented messages
- Action item extraction
- Web dashboard for report management

---

## Tech Stack

- **Python 3.11+**
- **OpenAI GPT-4** — Incident analysis and report generation
- **Slack SDK** — Real-time channel monitoring
- **Streamlit** — Web dashboard
- **Pydantic** — Data validation and modeling

---

## Setup

1. Clone the repo
2. Install dependencies:
```bash
pip install -r requirements.txt
```
3. Create a `.env` file with your credentials:
```
OPENAI_API_KEY=your_key_here
SLACK_BOT_TOKEN=your_bot_token
SLACK_APP_TOKEN=your_app_token
```
4. Run the app:
```bash
streamlit run app.py
```

---

## Use Cases

- SOC teams needing fast incident summaries from Slack war rooms
- IT operations automating post-incident reports
- Incident commanders who need timelines without digging through chat logs
- Anyone turning noisy alert channels into structured reports
