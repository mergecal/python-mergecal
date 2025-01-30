from typing import Any


def test_merge_calendars_with_no_uids(merge: Any) -> None:
    """Test that merging calendars works correctly when events have no UIDs."""
    merged = merge(["no_uids_calendar.ics"])
    events = list(merged.walk("VEVENT"))
    # Should find all events even without UIDs
    assert len(events) == 3, "Expected all events to be included, even without UIDs"

    # Verify all expected events are present
    summaries = sorted(event.get("summary") for event in events)
    assert summaries == [
        "Event with no UID 1",
        "Event with no UID 2",
        "Event with no UID 3",
    ], "All events should be included regardless of missing UIDs"

    # Verify none of the events have UIDs
    assert all(event.get("uid") is None for event in events), (
        "Test events should not have UIDs"
    )
