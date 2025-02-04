from datetime import date, datetime
from typing import Any


def test_merge_calendars_with_date_recurrence_id(merge: Any) -> None:
    """Test that merging calendars works with both date and datetime recurrence IDs."""
    merged = merge(["calendar_with_date_recurrence_id.ics"])
    events = list(merged.walk("VEVENT"))

    # Verify we found events
    assert len(events) > 0, "Expected to find events in merged calendar"

    # Find events with recurrence IDs
    recurrence_events = [e for e in events if "RECURRENCE-ID" in e]
    assert any(recurrence_events), "Expected to find at least one recurring event"

    # Verify recurrence_id can be either date or datetime
    for event in recurrence_events:
        recurrence_id = event["RECURRENCE-ID"].dt
        # Should be either a date or datetime
        assert isinstance(recurrence_id, (date, datetime)), (
            "Recurrence ID should be a date or datetime object"
        )
