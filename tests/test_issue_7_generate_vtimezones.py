"""Generate VTIMEZONEs when not available (Issue #7)."""

from mergecal import CalendarMerger, merge_calendars
from mergecal.calendar_merger import _timezone_cache


def test_generate_vtimezone_enabled_by_default(calendars):
    """Missing VTIMEZONEs are generated and included in the merged calendar."""
    _timezone_cache.clear()

    result = merge_calendars(calendars.no_vtimezone_google.stream)

    timezone_names = {tz.tz_name for tz in result.timezones}
    assert "America/New_York" in timezone_names
    assert "Europe/London" in timezone_names


def test_utc_timezone_filtered_out(calendars):
    """UTC needs no VTIMEZONE per RFC 5545 §3.6.5."""
    result = merge_calendars(calendars.no_vtimezone_google.stream)

    assert "UTC" not in {tz.tz_name for tz in result.timezones}


def test_generate_vtimezone_can_be_disabled(calendars):
    """Generation can be disabled; no VTIMEZONE components are added."""
    result = merge_calendars(
        calendars.no_vtimezone_google.stream, generate_vtimezone=False
    )

    assert len(list(result.timezones)) == 0


def test_calendar_merger_generate_vtimezone_parameter(calendars):
    """CalendarMerger respects generate_vtimezone=False."""
    cals = calendars.no_vtimezone_google.stream

    result_on = CalendarMerger(cals, generate_vtimezone=True).merge()
    result_off = CalendarMerger(cals, generate_vtimezone=False).merge()

    assert len(list(result_on.timezones)) > 0
    assert len(list(result_off.timezones)) == 0


def test_existing_vtimezone_components_preserved(calendars):
    """Existing VTIMEZONE components survive the merge."""
    result = merge_calendars(calendars.x_wr_timezone.stream)

    assert len(list(result.timezones)) > 0


def test_x_wr_timezone_conversion_still_works(calendars):
    """X-WR-TIMEZONE events are still present when generation is disabled."""
    result = merge_calendars(calendars.x_wr_timezone.stream, generate_vtimezone=False)

    assert len(list(result.events)) == 2
    assert len(list(result.timezones)) == 0


def test_timezone_deduplication(calendars):
    """Each timezone appears exactly once even when merged from duplicate calendars."""
    cals = calendars.no_vtimezone_google.stream * 2
    result = merge_calendars(cals, generate_vtimezone=True)

    timezone_names = [tz.tz_name for tz in result.timezones]
    assert timezone_names.count("America/New_York") == 1
    assert timezone_names.count("Europe/London") == 1


def test_generated_timezones_cached_across_instances(calendars):
    """Generated timezones are cached so subsequent merges avoid re-generation."""
    _timezone_cache.clear()

    merge_calendars(calendars.no_vtimezone_google.stream)

    assert "America/New_York" in _timezone_cache
    assert "Europe/London" in _timezone_cache


def test_cache_not_populated_when_vtimezone_excluded(calendars):
    """Cache is not populated when VTIMEZONE is excluded from the components list."""
    _timezone_cache.clear()

    merge_calendars(
        calendars.no_vtimezone_google.stream,
        components=["VEVENT"],
        generate_vtimezone=True,
    )

    assert "America/New_York" not in _timezone_cache
    assert "Europe/London" not in _timezone_cache
