# Quick Start Guide

## 1. Get Claude API Key
- Visit: https://console.anthropic.com/
- Create account / Sign in
- Go to "API Keys"
- Click "Create Key"
- Copy the key (starts with sk-ant-...)

## 2. Configure Environment
Edit the `.env` file in the project root:
```
ANTHROPIC_API_KEY=sk-ant-paste-your-key-here
```

## 3. Install Dependencies
```bash
pip install -r requirements.txt
```

## 4. Run the App
```bash
streamlit run app.py
```

## 5. Use the Tool
- Paste incident notes in the text box
- Click "Generate Report"
- Download the markdown report

That's it!

---

## Optional: Slack Integration
If you want Slack integration, also add:
```
SLACK_BOT_TOKEN=xoxb-your-slack-bot-token
```

Get Slack token from: https://api.slack.com/apps
