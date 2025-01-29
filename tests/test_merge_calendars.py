"""Tests to merge the calendars."""


def test_merge_calendars_with_one_event_contain_two_events(merge) -> None:  # type: ignore
    """Test that merging calendars with one event contain two events."""
    merged = merge(["one_event.ics", "another_event.ics"])
    events = list(merged.walk("VEVENT"))
    assert len(events) == 2
    assert events[0].get("summary") == "Event 1"
    assert events[1].get("summary") == "Event 2"


def test_merge_calendars_with_recurring_events(merge):
    """Test merging calendars with recurring events and RECURRENCE-ID."""
    merged = merge(
        ["four_week_recurring.ics", "four_week_recurring_with_recurrence_id.ics"]
    )
    events = list(merged.walk("VEVENT"))

    # Check that we have the correct number of events
    assert len(events) == 2, "Expected 2 events after merging"

    # Check that we have one recurring event and one event with RECURRENCE-ID
    assert sum(1 for e in events if "RRULE" in e) == 1, "Expected 1 recurring event"
    assert sum(1 for e in events if "RECURRENCE-ID" in e) == 1, (
        "Expected 1 event with RECURRENCE-ID"
    )

    # Check that the event with RECURRENCE-ID has a different summary
    recurring_event = next(e for e in events if "RRULE" in e)
    modified_event = next(e for e in events if "RECURRENCE-ID" in e)
    assert recurring_event.get("summary") != modified_event.get("summary"), (
        "Modified event should have a different summary"
    )

    # Check that the sequence number of the modified event is higher
    assert modified_event.get("sequence", 0) > recurring_event.get("sequence", 0), (
        "Modified event should have a higher sequence number"
    )
