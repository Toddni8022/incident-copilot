# 🤖 Real-time Slack Bot Setup

This guide shows you how to set up a **real-time Slack bot** that automatically generates incident reports when triggered.

## 🆚 Two Slack Modes

| Feature | **Web App (Current)** | **Real-time Bot (New)** |
|---------|----------------------|-------------------------|
| **How it works** | Manual: Paste channel ID → Fetch → Analyze | Automatic: Listens to channels 24/7 |
| **Trigger** | Click "Fetch & Analyze" button | Type `@incident-report` or react with 🚨 |
| **Setup complexity** | Easy (just need bot token) | Medium (need app token + Socket Mode) |
| **Use case** | On-demand analysis | Continuous monitoring |
| **File** | `app.py` (Streamlit) | `slack_bot_realtime.py` |

## 🚀 Setting Up the Real-time Bot

### Step 1: Create a Slack App

1. Go to https://api.slack.com/apps
2. Click **"Create New App"** → **"From scratch"**
3. Name: `Incident Copilot`
4. Select your workspace
5. Click **"Create App"**

### Step 2: Enable Socket Mode

1. In your app settings, go to **"Socket Mode"**
2. Toggle **"Enable Socket Mode"** to ON
3. When prompted, create an app-level token:
   - Token Name: `incident-bot`
   - Scopes: `connections:write`
4. Copy the **App Token** (starts with `xapp-...`)
5. Save to `.env`:
   ```
   SLACK_APP_TOKEN=xapp-1-AXXXXXXXXXX-XXXXXXXXXXXX-XXXXXXXXXXXXXXXXXXXXXXXX
   ```

### Step 3: Add Bot Token Scopes

1. Go to **"OAuth & Permissions"**
2. Scroll to **"Scopes"** → **"Bot Token Scopes"**
3. Add these scopes:
   - `channels:history` - Read messages
   - `channels:read` - List channels
   - `chat:write` - Post reports
   - `reactions:read` - Detect emoji reactions
4. Scroll up and click **"Install to Workspace"**
5. Authorize the app
6. Copy the **Bot User OAuth Token** (starts with `xoxb-...`)
7. Save to `.env`:
   ```
   SLACK_BOT_TOKEN=xoxb-XXXXXXXXXXXX-XXXXXXXXXXXXX-XXXXXXXXXXXXXXXXXXXXXXXX
   ```

### Step 4: Enable Event Subscriptions

1. Go to **"Event Subscriptions"**
2. Toggle **"Enable Events"** to ON
3. Under **"Subscribe to bot events"**, add:
   - `message.channels` - Listen to channel messages
   - `reaction_added` - Listen to emoji reactions
4. Click **"Save Changes"**

### Step 5: Invite Bot to Channel

1. In Slack, go to the channel you want to monitor
2. Type: `/invite @Incident Copilot`
3. The bot is now listening!

### Step 6: Configure .env

Your `.env` should have:

```bash
# Claude API
ANTHROPIC_API_KEY=sk-ant-your-actual-key

# Slack Bot
SLACK_BOT_TOKEN=xoxb-your-bot-token
SLACK_APP_TOKEN=xapp-your-app-token
```

### Step 7: Run the Bot

```bash
python slack_bot_realtime.py
```

You should see:
```
🤖 Incident Copilot Slack Bot is running!
   Triggers:
   - Type: @incident-report, /incident, or !incident
   - React with: 🚨 :rotating_light: :fire: :incident:

Press Ctrl+C to stop...
```

## 🎯 Using the Bot

### Method 1: Keyword Trigger

In any channel where the bot is invited, type:

```
@incident-report
```

or

```
/incident Please analyze this channel
```

The bot will:
1. Fetch the last 50 messages from the channel
2. Generate an incident report
3. Post it back to the thread

### Method 2: Emoji Reaction

React to any message with:
- 🚨 `:rotating_light:`
- 🔥 `:fire:`
- `:incident:` (custom emoji)

The bot will analyze recent messages and create a report.

## 📦 Creating Bot Executable

To include the Slack bot in your executable:

1. **Update build script** - Edit `build_exe.py`, change:
   ```python
   'launcher.py',  # Main entry point
   ```
   to:
   ```python
   'slack_bot_realtime.py',  # For Slack bot executable
   ```

2. **Build separate executables:**
   ```bash
   # Build web app
   python build_exe.py

   # Build Slack bot (modify build_exe.py first)
   python build_exe.py
   ```

3. **Result:**
   - `dist/IncidentCopilot.exe` - Web interface
   - `dist/SlackBot.exe` - Real-time bot

## 🔧 Troubleshooting

### Bot doesn't respond

1. Check if bot is online:
   ```bash
   python slack_bot_realtime.py
   ```
   Should show "Slack bot is running!"

2. Verify bot is in the channel:
   - In Slack, type `/invite @Incident Copilot`

3. Check `.env` configuration:
   - `ANTHROPIC_API_KEY` - Set and valid?
   - `SLACK_BOT_TOKEN` - Starts with `xoxb-`?
   - `SLACK_APP_TOKEN` - Starts with `xapp-`?

### "Socket mode is not enabled"

- Go to your Slack app settings
- Navigate to "Socket Mode"
- Toggle it ON
- Generate an app-level token

### "Missing scopes" error

- Go to "OAuth & Permissions"
- Add the required scopes listed in Step 3
- Reinstall the app to your workspace

### Bot crashes on startup

Check logs:
```bash
LOG_LEVEL=DEBUG python slack_bot_realtime.py
```

Common issues:
- Missing `SLACK_APP_TOKEN`
- Invalid tokens
- Socket mode not enabled

## 🎭 Comparison with Web App

**Use the Web App (`app.py`) if you want:**
- ✅ Manual, on-demand analysis
- ✅ Web-based UI
- ✅ Browse past reports
- ✅ Easy setup

**Use the Real-time Bot (`slack_bot_realtime.py`) if you want:**
- ✅ 24/7 monitoring
- ✅ Automatic report generation
- ✅ Trigger from within Slack
- ✅ No manual intervention

**Use BOTH:**
- Web app for scheduled/planned analysis
- Bot for real-time incident response

## 🚀 Advanced: Running as Service

### Windows (Task Scheduler)

1. Create `start_bot.bat`:
   ```batch
   @echo off
   cd C:\path\to\incident-copilot
   python slack_bot_realtime.py
   ```

2. Open Task Scheduler
3. Create Basic Task:
   - Name: Incident Copilot Bot
   - Trigger: At startup
   - Action: Start a program
   - Program: `C:\path\to\start_bot.bat`

### Linux (systemd)

Create `/etc/systemd/system/incident-bot.service`:

```ini
[Unit]
Description=IT Incident Copilot Slack Bot
After=network.target

[Service]
Type=simple
User=youruser
WorkingDirectory=/path/to/incident-copilot
Environment="PATH=/usr/bin:/usr/local/bin"
ExecStart=/usr/bin/python3 slack_bot_realtime.py
Restart=always

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl enable incident-bot
sudo systemctl start incident-bot
sudo systemctl status incident-bot
```

## 🎉 Success!

Your bot is now monitoring Slack channels and automatically generating incident reports when triggered!

Test it by typing `@incident-report` in a channel where the bot is present.
