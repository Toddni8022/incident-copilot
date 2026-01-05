import os
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from incident_parser import IncidentCopilot
from dotenv import load_dotenv

load_dotenv()

app = App(token=os.getenv("SLACK_BOT_TOKEN"))
copilot = IncidentCopilot()

@app.command("/incident-report")
def handle_incident_command(ack, command, say):
    ack()
    
    # Get thread messages if in a thread
    thread_ts = command.get("thread_ts") or command.get("ts")
    channel_id = command["channel_id"]
    
    # Fetch conversation history
    result = app.client.conversations_replies(
        channel=channel_id,
        ts=thread_ts
    )
    
    # Combine all messages
    raw_text = "\n".join([msg["text"] for msg in result["messages"]])
    
    # Generate report
    report = copilot.parse_incident(raw_text)
    markdown = copilot.format_markdown(report)
    
    say(f"```{markdown}```", thread_ts=thread_ts)

if __name__ == "__main__":
    handler = SocketModeHandler(app, os.getenv("SLACK_APP_TOKEN"))
    handler.start()
