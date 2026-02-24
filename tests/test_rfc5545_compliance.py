"""Tests for RFC 5545 compliance."""

from mergecal import CalendarMerger, merge_calendars


def test_empty_merge_has_required_properties():
    """Empty merge should include all standard RFC 5545 properties."""
    result = merge_calendars([])

    assert result.get("VERSION") == "2.0"
    assert result.get("PRODID") is not None
    assert "-//mergecal.org//MergeCal//EN" in str(result.get("PRODID"))
    assert result.get("CALSCALE") == "GREGORIAN"


def test_custom_calscale_parameter():
    """Should accept custom calendar scale values."""
    result = merge_calendars([], calscale="JULIAN")
    assert result.get("CALSCALE") == "JULIAN"


def test_calendar_merger_calscale_parameter():
    """CalendarMerger should accept calscale parameter."""
    merger = CalendarMerger([], calscale="HEBREW")
    result = merger.merge()
    assert result.get("CALSCALE") == "HEBREW"


def test_calscale_defaults_to_gregorian():
    """CALSCALE should default to GREGORIAN when not specified."""
    merger = CalendarMerger([])
    result = merger.merge()
    assert result.get("CALSCALE") == "GREGORIAN"


def test_merged_calendar_properties_complete(merge):
    """Merged calendar should have all expected properties."""
    result = merge([])

    ics_content = result.to_ical().decode("utf-8")
    assert "BEGIN:VCALENDAR" in ics_content
    assert "VERSION:2.0" in ics_content
    assert "PRODID:" in ics_content
    assert "CALSCALE:GREGORIAN" in ics_content
    assert "END:VCALENDAR" in ics_content


def test_method_parameter_still_works():
    """Existing METHOD parameter should continue working."""
    result = merge_calendars([], method="PUBLISH")
    assert result.get("METHOD") == "PUBLISH"
    assert result.get("CALSCALE") == "GREGORIAN"


def test_all_parameters_together():
    """All parameters should work together."""
    result = merge_calendars(
        [], calscale="ISLAMIC", method="REQUEST", prodid="-//Custom//App//EN"
    )

    assert result.get("CALSCALE") == "ISLAMIC"
    assert result.get("METHOD") == "REQUEST"
    assert result.get("PRODID") == "-//Custom//App//EN"
    assert result.get("VERSION") == "2.0"
