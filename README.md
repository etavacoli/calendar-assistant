# Calendar Assistant

> A natural language calendar assistant powered by the Claude LLM API. Type commands in plain English — the assistant parses intent, routes to the correct logic, and manages your calendar automatically.

---

## What makes this different

- **Understands arbitrary natural language input** — interprets 10 categories of calendar intent with no hardcoded keywords, regex, or rules. "Push my workout back a bit", "move gym one hour later", and "shift my 10am forward by 60 minutes" all resolve to the same operation.
- **Sub-second response time** for all local calendar operations
- **12 automated tests** covering create, delete, move, conflict detection, and free-time search
- **Conflict detection** on every event creation with user confirmation flow
- **Structured LLM output** — Claude returns strict JSON that Python validates before execution, isolating the AI layer from the logic layer
- **Secure API key handling** via environment variables — key never touches source code

---

## What It Does

The user types a plain English command. The assistant figures out what they mean, executes the right operation, and responds — no menus, no forms, no dropdowns.

```
You: Push everything on Thursday back an hour
→ Moved 3 event(s) on 2026-05-15: running, study session, call with advisor.

You: Find a free 90-minute block tomorrow
→ Free 90-minute blocks on 2026-05-14:
     - 08:00 to 10:00
     - 13:30 to 22:00

You: Does anything conflict with 3-4pm on Friday?
→ Conflicts found:
     - math exam: 15:00 to 18:00

You: Move gym to 2pm
→ Moved 'gym' to 14:00 - 15:00.
```

---

## Supported Commands

| Natural Language Example | Action |
|---|---|
| "List my events tomorrow" | List events on a date |
| "What do I have this week?" | List all upcoming events |
| "Create a study session Friday from 3 to 5" | Create event |
| "Delete my chemistry review" | Delete event by name |
| "Move gym one hour later" | Shift event by relative time |
| "Move gym to 2pm" | Move event to specific time |
| "Push everything on Thursday back an hour" | Shift all events on a date |
| "Check if 3–4pm conflicts with anything tomorrow" | Conflict check |
| "Find a free 90-minute block tomorrow" | Free time search |

---

## Architecture

The project is intentionally split into three isolated layers:

```
app.py              ← Entry point. Handles user input and routes actions.
llm_parser.py       ← Sends input to Claude API. Returns structured JSON only.
calendar_logic.py   ← Pure Python calendar functions. No LLM dependency.
events.json         ← Local calendar store.
```

**Why this matters:** The LLM never directly modifies the calendar. It only translates language into a structured command like:

```json
{"action": "move_event", "name": "Gym", "shift_minutes": 60}
```

Python then validates the action and calls the correct function. This separation means the calendar logic can be tested independently of the LLM, and the LLM can be swapped out without touching the core logic.

---

## Tech Stack

| Tool | Purpose |
|---|---|
| Python 3.9+ | Core language |
| Claude API (Anthropic) | Natural language parsing |
| python-dotenv | Secure API key management |
| pytest | Automated testing |
| JSON | Local event persistence |

---

## Setup

### 1. Clone the repo

```bash
git clone https://github.com/etavacoli/calendar-assistant.git
cd calendar-assistant
```

### 2. Install dependencies

```bash
pip3 install -r requirements.txt
```

### 3. Set up your API key

```bash
cp .env.example .env
```

Open `.env` and add your Anthropic API key:

```
ANTHROPIC_API_KEY=your_key_here
```

Get a key at [console.anthropic.com](https://console.anthropic.com). Your `.env` file is listed in `.gitignore` and will never be committed.

### 4. Run the app

```bash
python3 app.py
```

### 5. Run the tests

```bash
python3 -m pytest test_calendar.py -v
# or if pytest is on your PATH:
pytest test_calendar.py -v
```

---

## File Structure

```
calendar-assistant/
├── app.py              # Entry point and action router
├── calendar_logic.py   # All calendar operations (9 functions)
├── llm_parser.py       # Claude API integration and JSON validation
├── test_calendar.py    # 12 automated tests
├── events.json         # Local calendar data
├── .env.example        # API key template
├── .env                # Your API key (gitignored)
├── .gitignore
├── requirements.txt
└── README.md
```

---

## Design Decisions

**Why separate the LLM from the logic?**
Keeping the LLM as a pure translator means the calendar functions are deterministic and testable. If the LLM fails or returns malformed JSON, the app catches it gracefully without corrupting calendar data.

**Why JSON instead of a database?**
Intentional — this project is scoped to demonstrate LLM integration and calendar logic. The storage layer is designed to be swappable: replacing `load_events()` and `save_events()` with database calls would require changing two functions and nothing else.

**Why 24-hour time format?**
String-based time comparison only works correctly with zero-padded 24-hour format. `"09:00" < "14:00"` works. `"9:00am" < "2:00pm"` does not.

---

## What's next

The immediate next step is a web frontend so this runs in a browser instead of a terminal. The storage layer is already designed to be swappable — moving from `events.json` to a real database only requires changing two functions. Google Calendar sync and multi-user support follow naturally from there.
