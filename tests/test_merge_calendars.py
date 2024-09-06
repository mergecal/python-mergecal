"""Tests to merge the calendars."""


def test_merge_calendars_with_one_event_contain_two_events(merge) -> None:  # type: ignore
    """Test that merging calendars with one event contain two events."""
    merged = merge(["one_event.ics", "another_event.ics"])
    events = list(merged.walk("VEVENT"))
    assert len(events) == 2
    assert events[0].get("summary") == "Event 1"
    assert events[1].get("summary") == "Event 2"
