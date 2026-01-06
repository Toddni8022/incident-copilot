# 🚨 IT Incident Copilot

AI-powered incident analysis tool that transforms messy IT incident tickets and Slack conversations into professional incident reports.

![App Screenshot](images/app-main.png)

## Features

- **Slack Integration** - Monitor incident channels in real-time
- **GPT-4 Analysis** - Intelligent parsing and categorization
- **Automated Reports** - Generate executive summaries, timelines, and action items
- **Multi-format Support** - Handle tickets, chat logs, and unstructured data
- **Web Interface** - User-friendly Streamlit dashboard

## Demo

![Report Generation](images/app-report.png)

## Tech Stack

- Python 3.11+
- OpenAI GPT-4
- Slack SDK
- Streamlit
- Pydantic

## Prerequisites

- Python 3.11 or higher
- OpenAI API key
- Slack Bot Token (optional for Slack integration)

## Installation

\\\ash
# Clone repository
git clone https://github.com/Toddni8022/incident-copilot.git
cd incident-copilot

# Create virtual environment (Windows)
python -m venv venv
.\venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt
\\\

## Configuration

Create a \.env\ file in the project root:

\\\
OPENAI_API_KEY=your_openai_key_here
SLACK_BOT_TOKEN=your_slack_token_here
SLACK_APP_TOKEN=your_slack_app_token_here
\\\

## Usage

\\\ash
# Activate virtual environment
.\venv\Scripts\Activate.ps1

# Run the application
streamlit run app.py
\\\

The app will open in your browser at \http://localhost:8501\

## Project Structure

\\\
incident-copilot/
├── app.py                 # Main Streamlit application
├── incident_parser.py     # Incident data parsing logic
├── slack_integration.py   # Slack API integration (if used)
├── requirements.txt       # Python dependencies
├── .env.example          # Environment variables template
└── README.md             # This file
\\\

## Troubleshooting

**Issue: OpenAI API errors**
- Verify your API key is correct in \.env\
- Check your OpenAI account has credits

**Issue: Module not found**
- Run \pip install -r requirements.txt\ again
- Ensure virtual environment is activated

## License

MIT License
