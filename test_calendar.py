import pytest
from calendar_logic import (
    load_events,
    save_events,
    list_events,
    create_event,
    delete_event,
    move_event,
    check_conflicts,
    find_free_time,
)

SAMPLE_EVENTS = [
    {"name": "basketball", "date": "2026-05-13", "start": "10:00", "end": "11:30"},
    {"name": "running", "date": "2026-05-15", "start": "09:00", "end": "10:00"},
    {"name": "math exam", "date": "2026-05-27", "start": "15:00", "end": "18:00"},
]


@pytest.fixture(autouse=True)
def reset_events():
    save_events([e.copy() for e in SAMPLE_EVENTS])
    yield
    save_events([e.copy() for e in SAMPLE_EVENTS])


# --- create_event ---

def test_create_event_adds_to_list():
    new_event = {"name": "yoga", "date": "2026-05-13", "start": "12:00", "end": "13:00"}
    create_event(new_event)
    names = [e["name"] for e in load_events()]
    assert "yoga" in names


def test_create_event_returns_confirmation():
    new_event = {"name": "yoga", "date": "2026-05-13", "start": "12:00", "end": "13:00"}
    result = create_event(new_event)
    assert "yoga" in result


# --- delete_event ---

def test_delete_event_removes_it():
    delete_event("basketball")
    names = [e["name"] for e in load_events()]
    assert "basketball" not in names


def test_delete_event_not_found():
    result = delete_event("nonexistent")
    assert "No event found" in result


# --- move_event ---

def test_move_event_forward():
    move_event("basketball", 60)
    events = load_events()
    for e in events:
        if e["name"] == "basketball":
            assert e["start"] == "11:00"
            assert e["end"] == "12:30"


def test_move_event_backward():
    move_event("basketball", -30)
    events = load_events()
    for e in events:
        if e["name"] == "basketball":
            assert e["start"] == "09:30"
            assert e["end"] == "11:00"


def test_move_event_not_found():
    result = move_event("nonexistent", 60)
    assert "No event found" in result


# --- check_conflicts ---

def test_check_conflicts_finds_overlap():
    conflicts = check_conflicts("2026-05-13", "10:30", "11:00")
    assert len(conflicts) == 1
    assert conflicts[0]["name"] == "basketball"


def test_check_conflicts_no_overlap():
    conflicts = check_conflicts("2026-05-13", "12:00", "13:00")
    assert len(conflicts) == 0


def test_check_conflicts_adjacent_no_overlap():
    conflicts = check_conflicts("2026-05-13", "11:30", "12:30")
    assert len(conflicts) == 0


# --- find_free_time ---

def test_find_free_time_returns_slots():
    slots = find_free_time("2026-05-13", 60)
    assert len(slots) > 0


def test_find_free_time_slots_long_enough():
    slots = find_free_time("2026-05-13", 60)
    for slot in slots:
        from datetime import datetime
        start = datetime.strptime(slot["start"], "%H:%M")
        end = datetime.strptime(slot["end"], "%H:%M")
        duration = int((end - start).total_seconds() // 60)
        assert duration >= 60


def test_find_free_time_no_slots_for_impossible_duration():
    slots = find_free_time("2026-05-13", 9999)
    assert len(slots) == 0
