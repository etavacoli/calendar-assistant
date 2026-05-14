import os
import json
from datetime import date
from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()

client = Anthropic()

SYSTEM_PROMPT = """You are a calendar assistant parser. Your only job is to convert natural language calendar commands into structured JSON.

Return ONLY a valid JSON object with no extra text, no markdown, no explanation.

Allowed actions and their required fields:

1.  list_events:      {{"action": "list_events", "date": "YYYY-MM-DD"}}
2.  list_upcoming:    {{"action": "list_upcoming", "days": integer}}
3.  create_event:     {{"action": "create_event", "name": "string", "date": "YYYY-MM-DD", "start": "HH:MM", "end": "HH:MM"}}
4.  delete_event:     {{"action": "delete_event", "name": "string"}}
5.  move_event:       {{"action": "move_event", "name": "string", "shift_minutes": integer}}
6.  move_event_to:    {{"action": "move_event_to", "name": "string", "new_start": "HH:MM"}}
7.  move_all_events:  {{"action": "move_all_events", "date": "YYYY-MM-DD", "shift_minutes": integer}}
8.  check_conflicts:  {{"action": "check_conflicts", "date": "YYYY-MM-DD", "start": "HH:MM", "end": "HH:MM"}}
9.  find_free_time:   {{"action": "find_free_time", "date": "YYYY-MM-DD", "duration_minutes": integer}}
10. unsupported:      {{"action": "unsupported", "reason": "string"}}

Rules:
- Use 24-hour time format (e.g. 3pm = 15:00)
- Today is {today}. Calculate actual dates for "today", "tomorrow", day names, etc.
- "push back by an hour" or "move one hour later" means shift_minutes = 60
- "move earlier by 30 minutes" means shift_minutes = -30
- "move gym to 2pm" means move_event_to with new_start = 14:00
- "push everything on Thursday back an hour" means move_all_events
- "what do I have this week" means list_upcoming with days = 7
- Return ONLY the JSON object, nothing else."""


def parse_command(user_input):
    today = date.today().strftime("%Y-%m-%d")

    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=256,
        system=SYSTEM_PROMPT.format(today=today),
        messages=[{"role": "user", "content": user_input}]
    )

    raw = response.content[0].text.strip()

    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        return {"action": "unsupported", "reason": f"Could not parse LLM response: {raw}"}
