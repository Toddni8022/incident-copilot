# 🚨 IT Incident Copilot

AI-powered incident analysis tool that transforms messy IT incident tickets and Slack conversations into professional incident reports.

## Features

- **Slack Integration** - Monitor incident channels in real-time
- **Claude AI Analysis** - Intelligent parsing and categorization using Claude 3.5 Sonnet
- **Automated Reports** - Generate executive summaries, timelines, and action items
- **Multi-format Support** - Handle tickets, chat logs, and unstructured data
- **Web Interface** - User-friendly Streamlit dashboard

## Tech Stack

- Python 3.11+
- Anthropic Claude 3.5 Sonnet
- Slack SDK
- Streamlit
- Pydantic

## Installation

\\\ash
# Clone repository
git clone https://github.com/Toddni8022/incident-copilot.git
cd incident-copilot

# Create virtual environment
python -m venv venv
.\venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt
\\\

## Configuration

Create a .env file with your API keys:

\\\
ANTHROPIC_API_KEY=your_anthropic_key
SLACK_BOT_TOKEN=your_slack_token  # Optional
SLACK_APP_TOKEN=your_app_token    # Optional
\\\

Get your Anthropic API key from: https://console.anthropic.com/

## Usage

\\\ash
streamlit run app.py
\\\

## License

MIT License

<img width="1862" height="861" alt="app-main" src="https://github.com/user-attachments/assets/5bd4ad68-4be0-4c34-9108-fe4077884ebf" />
<img width="1902" height="850" alt="app-report" src="https://github.com/user-attachments/assets/e59a7d67-e479-42a6-9f19-445417761a27" />

