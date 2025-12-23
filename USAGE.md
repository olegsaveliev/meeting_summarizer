# Usage Guide

## Quick Start

### 1. First Time Setup
```bash
./install.sh
# Edit .env with your API key
```

### 2. Your First Summary
```bash
python agent.py --input examples/example_input.txt
cat output/meeting_summary_*.md
```

## Common Use Cases

### After Every Meeting
```bash
# Option A: Interactive (fastest)
python agent.py --interactive
[paste notes, Ctrl+D]

# Option B: From file
cat > my_meeting.txt
[type notes, Ctrl+D]
python agent.py --input my_meeting.txt
```

### Weekly Batch Processing
```bash
# Process all meetings from the week
python agent.py --batch ./this_week_meetings/
```

### Important Client Meeting
```bash
# Use GPT-4 for best quality
python agent.py --input client_meeting.txt --model gpt-4 --email --brief
```

## Tips & Tricks

### Getting Better Results
1. Include participant names
2. Note explicit decisions
3. Mention deadlines/dates
4. Flag concerns/risks
5. Be specific about action items

### Example Good Input
Team Planning - Jan 15
Attendees: John (eng), Sarah (design), Client (Mike)
Discussed Q1 timeline. Client wants March 15 launch.
Budget: $50k approved.
Decisions:

Going with approach B
John leads backend, Sarah frontend
Weekly check-ins Tuesday 2pm

Action items:

John: API docs by Friday
Sarah: performance testing this week
Oleg: send update template to client

Risks:

Timeline tight if issues
Waiting on external API docs

### Example Bad Input
had a meeting
discussed stuff
john will do things
need to launch soon

## Advanced Usage

### Custom Output Directory
```bash
python agent.py --input notes.txt --output ./client_meetings/
```

### Skip Email/Brief
```bash
python agent.py --input notes.txt --no-email
```

### Quiet Mode (for scripts)
```bash
python agent.py --input notes.txt --quiet
```

## Integration Ideas

### With Alfred/Raycast
Create a workflow that:
1. Takes clipboard content
2. Runs agent on it
3. Shows notification when done

### With Obsidian
Save summaries to your Obsidian vault:
```bash
python agent.py --input notes.txt --output ~/Documents/Obsidian/Meetings/
```

### With Shortcuts (Mac/iOS)
Create a shortcut that:
1. Gets clipboard
2. Runs agent via SSH
3. Opens result file