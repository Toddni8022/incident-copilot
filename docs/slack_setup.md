# Slack App Setup

This guide explains how to create and configure a Slack app to use with IT Incident Copilot.

---

## 1. Create a Slack App

1. Go to [https://api.slack.com/apps](https://api.slack.com/apps)
2. Click **Create New App** → **From scratch**
3. Name it (e.g., `Incident Copilot`) and select your workspace
4. Click **Create App**

---

## 2. Configure Bot Token Scopes

In the left sidebar go to **OAuth & Permissions** → **Scopes** → **Bot Token Scopes**.

Add the following scopes:

| Scope | Purpose |
|---|---|
| `channels:history` | Read messages from public channels |
| `channels:read` | List public channels |
| `groups:history` | Read messages from private channels |
| `groups:read` | List private channels |
| `chat:write` | Post messages to channels |
| `users:read` | Look up user info for attribution |

---

## 3. Install the App to Your Workspace

1. Go to **OAuth & Permissions** → click **Install to Workspace**
2. Authorize the requested permissions
3. Copy the **Bot User OAuth Token** (starts with `xoxb-`)

---

## 4. Add the Bot to a Channel

1. Open the Slack channel you want to analyze
2. Type `/invite @IncidentCopilot` (use the bot's display name)
3. The bot can now read and post in that channel

---

## 5. Find Your Channel ID

Right-click the channel name → **View channel details** → scroll to the bottom to find the **Channel ID** (e.g., `C01234ABCDE`).

---

## 6. Set Environment Variables

Add your token to `.env`:

```
SLACK_BOT_TOKEN=xoxb-your-bot-token
```

---

## Troubleshooting

| Error | Fix |
|---|---|
| `not_in_channel` | Invite the bot to the channel |
| `missing_scope` | Add the required scope in API settings |
| `invalid_auth` | Check that your token starts with `xoxb-` |
| `channel_not_found` | Verify the channel ID is correct |
