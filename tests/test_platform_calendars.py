"""Tests for merging calendars from various real-world platforms."""

import pytest

from mergecal import merge_calendars

PLATFORM_PAIRS = [
    ("google_with_vtimezone", "google_x_location"),
    ("google_with_vtimezone", "thunderbird"),
    ("google_x_location", "thunderbird"),
    ("google_with_vtimezone", "android_etar"),
    ("thunderbird", "android_etar"),
]


@pytest.mark.parametrize("cal_a,cal_b", PLATFORM_PAIRS)
def test_merging_platform_calendars_is_reproducible(calendars, cal_a, cal_b):
    """Each platform pair merges to the same result on repeated calls."""
    cals = [getattr(calendars, cal_a), getattr(calendars, cal_b)]
    assert merge_calendars(cals) == merge_calendars(cals)


@pytest.mark.parametrize("cal_a,cal_b", PLATFORM_PAIRS)
def test_merging_platform_calendar_pair_is_idempotent(calendars, cal_a, cal_b):
    """Merging a platform pair twice produces the same result as merging it once."""
    cals = [getattr(calendars, cal_a), getattr(calendars, cal_b)]
    assert merge_calendars(cals) == merge_calendars(cals * 2)


def test_merging_all_platforms_produces_events(calendars):
    """All platform calendars can be merged together into a single output."""
    platforms = [
        calendars.google_with_vtimezone,
        calendars.google_x_location,
        calendars.thunderbird,
        calendars.android_etar,
    ]
    result = merge_calendars(platforms)
    assert len(list(result.events)) == 4


def test_google_alarm_email_attendee_survives_merge(calendars):
    """Google Calendar EMAIL alarm with ATTENDEE is preserved after merging."""
    result = merge_calendars([calendars.google_with_vtimezone])
    events = list(result.events)
    alarms = [c for e in events for c in e.subcomponents if c.name == "VALARM"]
    email_alarms = [a for a in alarms if a.get("action") == "EMAIL"]
    assert len(email_alarms) == 1


def test_google_recurring_with_x_apple_location_survives_merge(calendars):
    """Google recurring event with X-APPLE-STRUCTURED-LOCATION merges cleanly."""
    result = merge_calendars([calendars.google_x_location])
    events = list(result.events)
    assert len(events) == 1
    assert "X-APPLE-STRUCTURED-LOCATION" in events[0]


def test_thunderbird_x_moz_generation_survives_merge(calendars):
    """Thunderbird X-MOZ-GENERATION property is preserved after merging."""
    result = merge_calendars([calendars.thunderbird])
    events = list(result.events)
    assert events[0].get("x-moz-generation") is not None


def test_cross_platform_dedup_by_uid(calendars):
    """Events with the same UID from two feeds are deduplicated."""
    result = merge_calendars(
        [calendars.google_with_vtimezone, calendars.google_with_vtimezone]
    )
    uids = [e.uid for e in result.events]
    assert len(uids) == len(set(uids))
