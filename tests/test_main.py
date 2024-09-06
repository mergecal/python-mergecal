from datetime import datetime

from icalendar import Calendar, Event

from mergecal.main import CalendarMerger


def create_test_calendar(summary, dtstart):
    cal = Calendar()
    event = Event()
    event.add("summary", summary)
    event.add("dtstart", dtstart)
    cal.add_component(event)
    return cal


def test_calendar_merger():
    # Create two test calendars
    cal1 = create_test_calendar("Test Event 1", datetime(2023, 1, 1, 9, 0, 0))
    cal2 = create_test_calendar("Test Event 2", datetime(2023, 1, 2, 10, 0, 0))

    # Create a CalendarMerger instance
    merger = CalendarMerger([cal1, cal2])

    # Merge the calendars
    merged_cal = merger.merge()

    # Check that the merged calendar has both events
    events = [
        component for component in merged_cal.walk() if component.name == "VEVENT"
    ]
    assert len(events) == 2
    assert events[0]["summary"] == "Test Event 1"
    assert events[1]["summary"] == "Test Event 2"

    # Check that the PRODID is set correctly
    assert merged_cal["prodid"].startswith("-//mergecal.org//MergeCal//")
