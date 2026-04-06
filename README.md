# Incident Copilot

AI-powered incident analysis tool that converts unstructured Slack incident conversations into structured incident reports.

This project demonstrates how large language models can assist engineering and IT teams during incident response by extracting timelines, root causes, and action items from chat discussions.

---

## Overview

During production incidents, teams often coordinate in Slack channels. Important information becomes scattered across dozens or hundreds of messages.

Incident Copilot analyzes these conversations and automatically generates structured incident reports including:

- Timeline of key events
- Incident summary
- Suspected root cause
- Impact analysis
- Recommended follow-up actions

This helps teams reduce the time required to produce post-incident reports and improves incident documentation.

---

## Features

- Parse Slack conversation logs
- Extract key events and timestamps
- Generate incident summaries using LLMs
- Identify potential root causes
- Output structured reports
- Export reports in Markdown or JSON format

---

## Architecture

Slack Logs  
↓  
Preprocessing Pipeline  
↓  
LLM Analysis  
↓  
Incident Report Generator  

The system processes conversation logs, extracts relevant context, and uses an LLM to generate a structured incident report.

---

## Tech Stack

- Python
- Pandas
- OpenAI / LLM API
- JSON processing
- CLI interface

---

## Example Workflow

1. Export Slack incident channel messages
2. Save conversation logs as JSON
3. Run the analysis pipeline
4. Generate a structured incident report

Example command:

