"""Tests for ICS files containing multiple VCALENDAR components."""

from pathlib import Path

from mergecal import calendars_from_ical, merge_calendars

CALENDARS_DIR = Path(__file__).parent / "calendars"
TWO_VCALENDARS_DATA = (CALENDARS_DIR / "two_vcalendars.ics").read_bytes()


def test_calendars_from_ical_returns_two_calendars() -> None:
    """Parse an ICS file with two VCALENDAR blocks and get two Calendar objects."""
    cals = calendars_from_ical(TWO_VCALENDARS_DATA)
    assert len(cals) == 2


def test_merge_file_with_two_vcalendars_yields_both_events() -> None:
    """Merging calendars from a multi-VCALENDAR file produces all events."""
    cals = calendars_from_ical(TWO_VCALENDARS_DATA)
    merged = merge_calendars(cals)
    summaries = {str(e.get("summary")) for e in merged.walk("VEVENT")}
    assert summaries == {"Event A", "Event B"}


def test_merging_multi_vcalendar_file_with_itself_deduplicates() -> None:
    """Merging a multi-VCALENDAR file with itself produces no duplicate events."""
    cals = calendars_from_ical(TWO_VCALENDARS_DATA)
    merged_once = merge_calendars(cals)
    merged_twice = merge_calendars(cals + cals)
    assert merged_once == merged_twice
    summaries = {str(e.get("summary")) for e in merged_twice.walk("VEVENT")}
    assert summaries == {"Event A", "Event B"}
