"""Tests that CalendarMerger options can only be passed by keyword."""

import inspect

from mergecal import CalendarMerger


def test_options_are_keyword_only():
    parameters = inspect.signature(CalendarMerger).parameters
    options = [p for name, p in parameters.items() if name != "calendars"]
    assert options
    assert all(p.kind is inspect.Parameter.KEYWORD_ONLY for p in options)


def test_keyword_options_are_applied():
    result = CalendarMerger([], method="PUBLISH", calscale="JULIAN").merge()
    assert result["method"] == "PUBLISH"
    assert result["calscale"] == "JULIAN"
