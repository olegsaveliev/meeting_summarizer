"""
Prompt templates for Meeting Summarizer
Using your Day 3-4 prompt engineering skills!
"""

class Prompts:
    """
    Collection of prompts for meeting summarization
    """
    
    SYSTEM_PROMPT = """
You are an expert executive assistant and project manager with 10+ years of experience.

Your specialties:
- Extracting key decisions from discussions
- Identifying action items with precision
- Flagging risks and blockers
- Writing clear, actionable summaries

Your communication style:
- Professional and concise
- Action-oriented
- Uses structured formats
- Never adds information not present in the notes

You understand that meeting notes can be messy, incomplete, or informal.
You work with what you have and flag missing information when critical.
"""

    MEETING_SUMMARY = """
Transform these meeting notes into a comprehensive, structured summary.

MEETING NOTES:
{notes}

Generate a summary with these sections:

# MEETING SUMMARY
**Date:** {date}
**Topic:** [Extract or infer from notes]

---

## 📋 EXECUTIVE SUMMARY
[2-3 sentences capturing: what was discussed, what was decided, what happens next.
Written for someone who wasn't there. Focus on business impact.]

---

## ✅ KEY DECISIONS
[List major decisions made, with brief context of why each matters.
Format: "Decision - Why it matters / Context"
If no decisions were made, state: "No major decisions - discussion/planning phase"]

---

## 🎯 ACTION ITEMS

**High Priority (Urgent/Blocking):**
- [ ] [Task description] - **@[Owner if mentioned]** - Due: [Date if mentioned]

**Medium Priority:**
- [ ] [Task description] - **@[Owner if mentioned]** - Due: [Date if mentioned]

**Low Priority / Follow-up:**
- [ ] [Task description] - **@[Owner if mentioned]** - Due: [Date if mentioned]

**⚠️ Missing Information:**
- [ ] [Tasks where owner or deadline is unclear]

[If no action items, state: "No action items identified"]

---

## 🚨 RISKS & BLOCKERS

**Risks Identified:**
- [Risk description] - Severity: [High/Medium/Low] - [Mitigation if discussed]

**Current Blockers:**
- [Blocker description] - [Who can unblock if known]

[If none, state: "No risks or blockers identified"]

---

## 💡 KEY DISCUSSION POINTS

[Capture main topics discussed, organized by theme if possible.
Include important context, concerns raised, or questions that came up.
Keep it concise - this is NOT a transcript.]

---

## 📅 NEXT STEPS

**Immediate (This Week):**
- [What needs to happen immediately]

**Short-term (Next 2 Weeks):**
- [What's coming up soon]

**Next Meeting:**
- **Date:** [If mentioned, or suggest timing]
- **Agenda:**
  - [Topic 1 - based on unresolved items or next logical steps]
  - [Topic 2]

---

**IMPORTANT RULES:**
1. Only include information from the notes - don't invent details
2. If information is missing (owner, date, details), mark it with ⚠️
3. Maintain professional tone
4. Use checkboxes [ ] for action items
5. Be concise but complete
6. Prioritize action items by urgency and impact
7. For vague action items, note what clarification is needed
"""

    EMAIL_FOLLOWUP = """
Create a professional follow-up email based on this meeting summary.

MEETING SUMMARY:
{summary}

Generate an email with this structure:

Subject: [Meeting topic] - Summary & Action Items - [Date]

Hi [Team/Names if known, otherwise "team"],

Thanks for the productive meeting [add "on [topic]" if clear from summary].

**KEY DECISIONS:**
- [Decision 1]
- [Decision 2]

**ACTION ITEMS:**
- [Name/Role] - [Task] - [Due date]
- [Name/Role] - [Task] - [Due date]

**NEXT STEPS:**
[2-3 sentence overview of immediate actions and timeline]

**BLOCKERS/NEEDS:**
[Only if there are blockers or items needing attention]

[If next meeting scheduled: "Our next meeting is [date] to discuss [topics]."]

Please let me know if I missed anything or if you have questions!

Best,
[Your name]

---

**RULES:**
1. Professional but warm tone
2. Concise - aim for 150-200 words
3. Action-oriented
4. Easy to skim (use bullets and sections)
5. Only include information from the summary
6. If no action items or decisions, adjust format accordingly
"""

    EXECUTIVE_BRIEF = """
Create a brief executive summary from this meeting information.

MEETING SUMMARY:
{summary}

Generate an executive brief in this format:

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
EXECUTIVE BRIEF: [Meeting Topic]
[Date] | Status: 🟢/🟡/🔴
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

**THE HEADLINE:**
[One sentence capturing the most important outcome or development]

**WHAT HAPPENED:**
[2-3 sentences providing context and key discussion points]

**KEY DECISIONS:**
- [Decision 1]
- [Decision 2]

**BUSINESS IMPACT:**
[How this affects the business/project - timeline, resources, risks, opportunities]

**WHAT'S NEEDED:**
[Any decisions, resources, or actions needed from leadership]

**NEXT MILESTONE:**
[What's the next big deliverable or checkpoint, and when]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

**RULES:**
1. Maximum 200 words
2. Lead with impact
3. Be specific with timeline and numbers
4. Action-oriented
5. Written for C-level audience
6. Status: 🟢 = on track, 🟡 = at risk, 🔴 = blocked/critical
"""

    @staticmethod
    def format_meeting_summary(notes: str, date: str = None) -> str:
        """Format the meeting summary prompt with variables"""
        from datetime import datetime
        
        if date is None:
            date = datetime.now().strftime("%B %d, %Y")
        
        return Prompts.MEETING_SUMMARY.format(
            notes=notes,
            date=date
        )
    
    @staticmethod
    def format_email_followup(summary: str) -> str:
        """Format the email followup prompt"""
        return Prompts.EMAIL_FOLLOWUP.format(summary=summary)
    
    @staticmethod
    def format_executive_brief(summary: str) -> str:
        """Format the executive brief prompt"""
        return Prompts.EXECUTIVE_BRIEF.format(summary=summary)