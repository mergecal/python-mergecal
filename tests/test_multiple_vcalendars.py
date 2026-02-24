"""Tests for ICS files containing multiple VCALENDAR components."""

import pytest
from mergecal import calendars_from_ical, merge_calendars


@pytest.fixture
def two_vcalendars_cals(calendars_dir):
    """Fixture providing parsed calendars from two_vcalendars.ics file."""
    data = (calendars_dir / "two_vcalendars.ics").read_bytes()
    return calendars_from_ical(data)


def test_calendars_from_ical_returns_two_calendars(two_vcalendars_cals) -> None:
    """Parse an ICS file with two VCALENDAR blocks and get two Calendar objects."""
    assert len(two_vcalendars_cals) == 2


def test_merge_file_with_two_vcalendars_yields_both_events(two_vcalendars_cals) -> None:
    """Merging calendars from a multi-VCALENDAR file produces all events."""
    merged = merge_calendars(two_vcalendars_cals)
    summaries = {str(e.get("summary")) for e in merged.walk("VEVENT")}
    assert summaries == {"Event A", "Event B"}


def test_merging_multi_vcalendar_file_with_itself_deduplicates(two_vcalendars_cals) -> None:
    """Merging a multi-VCALENDAR file with itself produces no duplicate events."""
    cals = two_vcalendars_cals
    merged_once = merge_calendars(cals)
    merged_twice = merge_calendars(cals + cals)
    assert merged_once == merged_twice
    summaries = {str(e.get("summary")) for e in merged_twice.walk("VEVENT")}
    assert summaries == {"Event A", "Event B"}
