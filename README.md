# 🤖 Meeting Summarizer Agent

AI-powered meeting summarizer that transforms messy meeting notes into structured summaries, action items, and follow-up emails.

## ✨ Features

- 📝 Structured meeting summaries
- 📧 Professional follow-up emails
- 🎯 Action items with owners and deadlines
- 🚨 Risk and blocker identification
- 💰 Cost tracking
- 🎤 Interactive mode
- 📦 Batch processing
- ⚡ Fast (GPT-3.5-turbo) or Quality (GPT-4) modes

## 🚀 Quick Start

### Installation
```bash
# Clone repository
git clone <your-repo-url>
cd meeting-summarizer

# Create virtual environment
python3.11 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Set up API key
echo "OPENAI_API_KEY=your-key-here" > .env
```

### Basic Usage
```bash
# Summarize from file
python agent.py --input notes.txt

# Summarize from text
python agent.py --text "Meeting notes here..."

# Interactive mode
python agent.py --interactive

# Use GPT-4 for higher quality
python agent.py --input notes.txt --model gpt-4
```

## 📖 Usage Examples

### Example 1: Basic Summary
```bash
python agent.py --input examples/example_input.txt
```

Output:
- `meeting_summary_TIMESTAMP.md` - Structured summary
- `meeting_followup_email_TIMESTAMP.txt` - Email draft

### Example 2: Custom Options
```bash
# Summary + Email + Brief with GPT-4
python agent.py \
  --input notes.txt \
  --model gpt-4 \
  --email \
  --brief \
  --output ./my_summaries/
```

### Example 3: Batch Processing
```bash
# Process all meetings in a folder
python agent.py --batch ./meetings/

# Uses all .txt files in the directory
```

### Example 4: Quick Interactive Summary
```bash
python agent.py --interactive

# Paste your notes
# Press Ctrl+D when done
# Choose options
# Get instant summary!
```

## 📋 Command-Line Options
Required (choose one):
--input, -i PATH      Path to meeting notes file
--text, -t TEXT       Meeting notes as text
--interactive, -I     Interactive mode
--batch, -b DIR       Batch process directory
Optional:
--date, -d DATE       Meeting date (default: today)
--model, -m MODEL     AI model (gpt-3.5-turbo, gpt-4, gpt-4-turbo)
--output, -o DIR      Output directory (default: output/)
--email               Generate follow-up email
--no-email            Skip email generation
--brief               Generate executive brief
--no-brief            Skip brief generation
--quiet, -q           Minimal output

## 💰 Cost Estimates

Based on typical meeting notes (~500 words):

| Model | Cost per Meeting | Quality |
|-------|------------------|---------|
| GPT-3.5-turbo | $0.01-0.02 | Good |
| GPT-4-turbo | $0.05-0.10 | Better |
| GPT-4 | $0.15-0.30 | Best |

Monthly cost for 20 meetings:
- GPT-3.5: ~$0.40
- GPT-4: ~$4.00

💡 Tip: Use GPT-3.5 for routine meetings, GPT-4 for important client meetings!

## 📁 Output Format

### Meeting Summary (Markdown)
```markdown
# MEETING SUMMARY
**Date:** January 15, 2024

## 📋 EXECUTIVE SUMMARY
[2-3 sentence overview]

## ✅ KEY DECISIONS
- Decision 1 - Why it matters

## 🎯 ACTION ITEMS
**High Priority:**
- [ ] Task - @Owner - Due: Date

## 🚨 RISKS & BLOCKERS
- Risk description - Severity

## 📅 NEXT STEPS
...
```

### Follow-up Email (Text)
Subject: Meeting Topic - Summary & Action Items
Professional email with:

Key decisions
Action items with owners
Next steps
Blockers/needs

## ⚙️ Configuration

Edit `config.py` to customize:
```python
# Model settings
DEFAULT_MODEL = "gpt-3.5-turbo"  # Default model
TEMPERATURE = 0.3                # Consistency (0-1)

# Features
GENERATE_EMAIL = True             # Auto-generate emails
GENERATE_EXEC_BRIEF = False      # Executive briefs

# Output
OUTPUT_DIR = "output"            # Where to save files
```

## 🧪 Running Tests
```bash
# Test with example file
python agent.py --input examples/example_input.txt

# Test interactive mode
python agent.py --interactive

# Test batch processing
python agent.py --batch examples/
```

## 🛠️ Development

### Project Structure
meeting-summarizer/
├── agent.py          # Main agent logic
├── prompts.py        # Prompt templates
├── config.py         # Configuration
├── utils.py          # Utility functions
├── requirements.txt  # Dependencies
├── .env             # API keys (not committed)
├── .gitignore       # Git ignore rules
├── README.md        # This file
├── examples/        # Example inputs
│   └── example_input.txt
└── output/          # Generated summaries

### Adding Custom Prompts

Edit `prompts.py` to customize the output format:
```python
# Customize the summary template
MEETING_SUMMARY = """
Your custom prompt here...
"""
```

## 🤝 Contributing

Improvements welcome! Some ideas:
- Support for more LLM providers (Anthropic, local models)
- Integration with calendar apps
- Slack/email integration
- Web interface
- Meeting recording transcription

## 📝 License

MIT License - use it however you want!

## 🙏 Credits

Built during the 30-day AI + DevOps challenge.

## 💡 Tips for Best Results

1. **Write clear notes:** The better your input, the better the output
2. **Include names:** Helps identify action item owners
3. **Note dates:** Makes action items more specific
4. **Capture decisions:** Explicitly note what was decided
5. **Flag risks:** Mention concerns or blockers

## 🐛 Troubleshooting

**Error: "API key not found"**
- Make sure `.env` file exists
- Check that `OPENAI_API_KEY` is set
- Verify no extra spaces or quotes

**Error: "Connection error"**
- Check internet connection
- Verify firewall isn't blocking OpenAI
- Check API service status

**Output not as expected**
- Try GPT-4 for better quality
- Make input notes more detailed
- Customize prompts in `prompts.py`

## 📞 Support

Questions? Issues? Open an issue on GitHub!

---

**Save 10+ hours per week on meeting follow-ups! 🚀**