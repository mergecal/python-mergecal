"""The timezones are a valuable part of the calendar and must be included."""

from icalendar import Calendar


def test_merged_calendars_include_a_timezone(merge, calendars):
    """The timezones should be included."""
    calendar: Calendar = merge([calendars.one_event])
    assert len(calendar.timezones) == 1
    assert calendar.timezones[0].tz_name == "Europe/Berlin"


def test_merge_with_no_calendars(merge):
    """No calendars no timezone."""
    calendar: Calendar = merge([])
    assert len(calendar.timezones) == 0


def test_empty_calendar_has_no_timezone(merge):
    """Empty calendar merged ahs no timezone."""
    calendar: Calendar = merge([Calendar()])
    assert len(calendar.timezones) == 0


def test_x_wr_timezone_is_included(merge, calendars):
    """The x-wr-timezone property should create a timezone."""
    calendar: Calendar = merge([calendars.x_wr_timezone])
    assert calendar.timezones[0].tz_name == "America/New_York"
    assert calendar.events[1].start.tzname() == "EST"
