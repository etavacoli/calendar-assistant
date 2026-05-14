from llm_parser import parse_command
from calendar_logic import (
    list_events,
    list_upcoming_events,
    create_event,
    delete_event,
    move_event,
    move_event_to,
    move_all_events,
    check_conflicts,
    find_free_time,
)


def handle_command(parsed):
    action = parsed.get("action")

    if action == "list_upcoming":
        days = parsed.get("days", 7)
        events = list_upcoming_events(days)
        if not events:
            print(f"No upcoming events in the next {days} days.")
        else:
            print(f"\nUpcoming events (next {days} days):")
            for e in events:
                print(f"  - {e['date']} | {e['name']}: {e['start']} to {e['end']}")

    elif action == "list_events":
        events = list_events(parsed["date"])
        if not events:
            print(f"No events on {parsed['date']}.")
        else:
            print(f"\nEvents on {parsed['date']}:")
            for e in events:
                print(f"  - {e['name']}: {e['start']} to {e['end']}")

    elif action == "create_event":
        conflicts = check_conflicts(parsed["date"], parsed["start"], parsed["end"])
        if conflicts:
            print("\nWarning: this event conflicts with:")
            for c in conflicts:
                print(f"  - {c['name']}: {c['start']} to {c['end']}")
            confirm = input("Create anyway? (y/n): ").strip().lower()
            if confirm != "y":
                print("Cancelled.")
                return
        result = create_event({
            "name": parsed["name"],
            "date": parsed["date"],
            "start": parsed["start"],
            "end": parsed["end"],
        })
        print(result)

    elif action == "delete_event":
        result = delete_event(parsed["name"])
        print(result)

    elif action == "move_event":
        result = move_event(parsed["name"], parsed["shift_minutes"])
        print(result)

    elif action == "move_event_to":
        result = move_event_to(parsed["name"], parsed["new_start"])
        print(result)

    elif action == "move_all_events":
        result = move_all_events(parsed["date"], parsed["shift_minutes"])
        print(result)

    elif action == "check_conflicts":
        conflicts = check_conflicts(parsed["date"], parsed["start"], parsed["end"])
        if not conflicts:
            print(f"No conflicts between {parsed['start']} and {parsed['end']} on {parsed['date']}.")
        else:
            print(f"\nConflicts found:")
            for c in conflicts:
                print(f"  - {c['name']}: {c['start']} to {c['end']}")

    elif action == "find_free_time":
        slots = find_free_time(parsed["date"], parsed["duration_minutes"])
        if not slots:
            print(f"No free {parsed['duration_minutes']}-minute blocks found on {parsed['date']}.")
        else:
            print(f"\nFree {parsed['duration_minutes']}-minute blocks on {parsed['date']}:")
            for slot in slots:
                print(f"  - {slot['start']} to {slot['end']}")

    elif action == "unsupported":
        print(f"Sorry, I didn't understand that: {parsed.get('reason', 'unknown')}")

    else:
        print(f"Unknown action: {action}")


def main():
    print("=" * 40)
    print("  Calendar Assistant")
    print("  Type 'quit' to exit")
    print("=" * 40)
    print()

    while True:
        try:
            user_input = input("You: ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nGoodbye.")
            break

        if not user_input:
            continue

        if user_input.lower() in ("quit", "exit"):
            print("Goodbye.")
            break

        try:
            parsed = parse_command(user_input)
            handle_command(parsed)
        except Exception as e:
            print(f"Something went wrong: {e}")

        print()


if __name__ == "__main__":
    main()
