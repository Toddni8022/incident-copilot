import streamlit as st
from incident_parser import IncidentCopilot
from slack_sdk import WebClient
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

st.set_page_config(page_title="IT Incident Copilot", page_icon="🚨", layout="wide")

# Initialize
copilot = IncidentCopilot()
slack_client = WebClient(token=os.getenv("SLACK_BOT_TOKEN"))

# Header
st.title("🚨 IT Incident Copilot")
st.markdown("Transform messy incident notes into professional reports")

# Tabs
tab1, tab2, tab3 = st.tabs(["📝 Text Input", "💬 Slack Channel", "📊 View Reports"])

# Tab 1: Direct Text Input
with tab1:
    st.subheader("Paste Incident Notes")
    
    incident_text = st.text_area(
        "Enter messy ticket notes, chat logs, or outage descriptions:",
        height=300,
        placeholder="""Example:
prod db slow, users reporting 500 errors starting around 2:45pm
checked logs - connection pool maxed out
dave restarted db at 3:10
errors stopped at 3:15
need to fix cron schedule and add monitoring"""
    )
    
    col1, col2 = st.columns([1, 4])
    with col1:
        analyze_btn = st.button("Generate Report", type="primary", use_container_width=True)
    
    if analyze_btn and incident_text:
        with st.spinner("🔄 Analyzing incident with AI..."):
            try:
                report = copilot.parse_incident(incident_text)
                markdown = copilot.format_markdown(report)
                
                st.success("✅ Report generated!")
                
                # Display report
                st.markdown("---")
                st.markdown(markdown)
                
                # Download button
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                st.download_button(
                    label="📥 Download Report",
                    data=markdown,
                    file_name=f"incident_report_{timestamp}.md",
                    mime="text/markdown"
                )
                
                # Save to file
                output_file = f"output/incident_report_{timestamp}.md"
                with open(output_file, 'w', encoding='utf-8') as f:
                    f.write(markdown)
                st.info(f"Report saved to: {output_file}")
                
            except Exception as e:
                st.error(f"Error: {str(e)}")

# Tab 2: Slack Integration
with tab2:
    st.subheader("Analyze Slack Channel")
    
    channel_id = st.text_input(
        "Slack Channel ID",
        placeholder="C01234ABCDE",
        help="Right-click channel in Slack > View channel details > Copy Channel ID"
    )
    
    message_limit = st.slider("Number of messages to analyze", 10, 100, 50)
    
    col1, col2 = st.columns([1, 4])
    with col1:
        fetch_btn = st.button("Fetch & Analyze", type="primary", use_container_width=True)
    
    if fetch_btn and channel_id:
        with st.spinner(f"🔄 Fetching {message_limit} messages from Slack..."):
            try:
                result = slack_client.conversations_history(
                    channel=channel_id,
                    limit=message_limit
                )
                messages = result['messages']
                
                if not messages:
                    st.warning("No messages found in channel")
                else:
                    st.info(f"Found {len(messages)} messages")
                    
                    # Combine messages
                    raw_text = '\n'.join([
                        msg.get('text', '') for msg in messages if 'text' in msg
                    ])
                    
                    with st.spinner("🤖 Generating incident report..."):
                        report = copilot.parse_incident(raw_text)
                        markdown = copilot.format_markdown(report)
                        
                        st.success("✅ Report generated!")
                        
                        # Display
                        st.markdown("---")
                        st.markdown(markdown)
                        
                        # Options
                        col_a, col_b = st.columns(2)
                        
                        with col_a:
                            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                            st.download_button(
                                label="📥 Download Report",
                                data=markdown,
                                file_name=f"incident_report_{timestamp}.md",
                                mime="text/markdown"
                            )
                        
                        with col_b:
                            if st.button("📤 Post Back to Slack"):
                                slack_client.chat_postMessage(
                                    channel=channel_id,
                                    text=f"`{markdown}`"
                                )
                                st.success("Posted to Slack!")
                        
            except Exception as e:
                st.error(f"Error: {str(e)}")

# Tab 3: View Past Reports
with tab3:
    st.subheader("Previous Reports")
    
    try:
        import glob
        reports = sorted(glob.glob("output/*.md"), reverse=True)
        
        if reports:
            st.info(f"Found {len(reports)} saved reports")
            
            selected_report = st.selectbox(
                "Select a report to view:",
                reports,
                format_func=lambda x: x.split('/')[-1].split('\\')[-1]
            )
            
            if selected_report:
                with open(selected_report, 'r', encoding='utf-8') as f:
                    content = f.read()
                st.markdown("---")
                st.markdown(content)
                
                st.download_button(
                    label="📥 Download This Report",
                    data=content,
                    file_name=selected_report.split('/')[-1].split('\\')[-1],
                    mime="text/markdown"
                )
        else:
            st.warning("No reports found. Generate one first!")
            
    except Exception as e:
        st.error(f"Error loading reports: {str(e)}")

# Sidebar
with st.sidebar:
    st.header("⚙️ Settings")
    st.markdown("**Status**")
    
    # Check API keys
    if os.getenv("OPENAI_API_KEY"):
        st.success("✅ OpenAI Connected")
    else:
        st.error("❌ OpenAI Key Missing")
    
    if os.getenv("SLACK_BOT_TOKEN"):
        st.success("✅ Slack Connected")
    else:
        st.warning("⚠️ Slack Not Connected")
    
    st.markdown("---")
    st.markdown("**About**")
    st.markdown("AI-powered incident report generator using GPT-4")
    st.markdown("Transforms messy notes into structured documentation")
