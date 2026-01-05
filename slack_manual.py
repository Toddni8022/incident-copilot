from slack_sdk import WebClient
from incident_parser import IncidentCopilot
import os
from dotenv import load_dotenv

load_dotenv()

client = WebClient(token=os.getenv("SLACK_BOT_TOKEN"))
copilot = IncidentCopilot()

def process_channel_history(channel_id, limit=50):
    print(f"Fetching messages from channel {channel_id}...")
    
    # Get recent messages
    result = client.conversations_history(channel=channel_id, limit=limit)
    messages = result['messages']
    
    print(f"Found {len(messages)} messages. Analyzing...")
    
    # Combine into text
    raw_text = '\n'.join([msg.get('text', '') for msg in messages if 'text' in msg])
    
    # Generate report
    report = copilot.parse_incident(raw_text)
    markdown = copilot.format_markdown(report)
    
    print("\n" + markdown + "\n")
    
    # Post back to channel
    client.chat_postMessage(channel=channel_id, text=f'`{markdown}`')
    
    print('✅ Report posted to Slack!')

if __name__ == '__main__':
    print("Slack Incident Copilot - Manual Mode")
    print("=====================================\n")
    channel_id = input('Enter Slack channel ID (right-click channel > View channel details): ')
    process_channel_history(channel_id)
