# 🎯 Demo Guide for Employers

This guide helps you quickly understand and test the IT Incident Copilot project.

## 📋 **What This Project Does**

Transforms messy IT incident notes into professional, structured reports using Claude AI:

**Input (messy notes):**
```
prod db slow, users reporting 500 errors starting around 2:45pm
checked logs - connection pool maxed out
dave restarted db at 3:10
errors stopped at 3:15
need to fix cron schedule and add monitoring
```

**Output (structured report):**
- Executive summary
- Affected systems list
- Timeline with timestamps
- Root cause analysis
- Impact assessment
- Action items with priorities

## 🚀 **Quick Demo (3 Minutes)**

### Option 1: View Sample Output

Check out the pre-generated example:
- **Input**: `examples/sample_ticket.txt`
- **Output**: `examples/sample_output_report.md`

### Option 2: Run It Yourself

1. **Prerequisites:**
   - Python 3.11+
   - Claude API key (get free tier at https://console.anthropic.com/)

2. **Setup (2 minutes):**
   ```bash
   # Clone the repo
   git clone https://github.com/Toddni8022/incident-copilot.git
   cd incident-copilot

   # Install dependencies
   pip install -r requirements.txt

   # Add your API key
   echo "ANTHROPIC_API_KEY=your-key-here" > .env

   # Run the web app
   python -m streamlit run app.py
   ```

3. **Test it:**
   - Browser opens automatically to http://localhost:8501
   - Paste sample incident text (or use the placeholder example)
   - Click "Generate Report"
   - See structured output in seconds!

## 🛠️ **Technical Highlights**

### Architecture
- **Frontend**: Streamlit web interface
- **AI Engine**: Anthropic Claude 3.5 Sonnet
- **Data Validation**: Pydantic models
- **Integrations**: Slack SDK for channel analysis
- **Deployment**: Standalone Windows executable or Python

### Code Quality Features
- Type hints throughout
- Comprehensive error handling
- Logging system
- Configuration management
- Input validation
- Modular design

### Key Files to Review
- `incident_parser.py` - Core AI parsing logic
- `app.py` - Streamlit web interface
- `config.py` - Configuration management
- `slack_bot_realtime.py` - Real-time Slack bot
- `build.ps1` - Automated executable builder

## 📊 **Project Metrics**

- **Lines of Code**: ~1,500 (Python)
- **Files**: 15 source files
- **Test Coverage**: Input validation, error handling
- **Documentation**: 8 markdown guides
- **Commits**: [View on GitHub]
- **Time to Demo**: < 3 minutes

## 🎬 **Use Cases**

1. **IT Teams**: Transform Slack incident discussions into formal reports
2. **DevOps**: Auto-generate post-mortems from monitoring alerts
3. **Support Teams**: Convert ticket notes into executive summaries
4. **Compliance**: Standardize incident documentation

## 💡 **Technical Decisions**

### Why Claude over OpenAI?
- Better instruction following for structured outputs
- More reliable JSON generation
- Excellent at technical analysis
- Strong reasoning for root cause analysis

### Why Streamlit?
- Rapid prototyping
- Clean UI with minimal code
- Easy deployment
- Real-time updates

### Why Pydantic?
- Strong type validation
- Automatic documentation
- IDE support
- Runtime validation

## 🔐 **Security Considerations**

- API keys stored in `.env` (gitignored)
- No hardcoded credentials
- Input sanitization
- Rate limiting awareness
- Secure by default configuration

## 📈 **Future Enhancements**

- [ ] Multi-tenant support
- [ ] Custom report templates
- [ ] Email integration
- [ ] Jira ticket creation
- [ ] Historical analysis dashboard
- [ ] Team analytics

## 🤝 **Questions?**

**"Does this require an API key?"**
Yes, but Claude offers a free tier. The app gracefully handles missing keys with clear error messages.

**"Can I test without API key?"**
See the sample output in `examples/sample_output_report.md` to see what it generates.

**"How long does analysis take?"**
2-5 seconds typically, depending on input length.

**"Can it handle non-English text?"**
Yes, Claude supports 95+ languages.

**"Is there a cost?"**
Claude API costs ~$0.003 per report (free tier available).

## 📞 **Contact**

- **GitHub**: https://github.com/Toddni8022/incident-copilot
- **Demo Video**: [Link if available]
- **Portfolio**: [Your portfolio site]

---

**Ready to see it in action?** Follow the "Run It Yourself" instructions above!
