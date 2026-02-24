"""Tests for RFC 7986 COLOR property merging."""

import pytest

from mergecal import merge_calendars


@pytest.mark.parametrize("component_type", ["VEVENT", "VTODO", "VJOURNAL"])
def test_component_inherits_calendar_color(calendars, component_type):
    result = merge_calendars(calendars.color_rfc7986.stream)
    assert result.walk(component_type)[0].color == "turquoise"


def test_event_inherits_apple_calendar_color(calendars):
    result = merge_calendars(calendars.color_apple.stream)
    assert result.events[0].color == "#e78074"


@pytest.mark.parametrize("component_type", ["VEVENT", "VTODO", "VJOURNAL"])
def test_component_own_color_not_overwritten(calendars, component_type):
    result = merge_calendars(calendars.color_event_own.stream)
    assert result.walk(component_type)[0].color == "navy"


def test_no_color_when_calendar_has_none(calendars):
    result = merge_calendars(calendars.color_none.stream)
    assert not result.color
    assert not result.events[0].color


def test_merged_calendar_color_first_wins(calendars):
    cals = calendars.color_rfc7986.stream + calendars.color_apple.stream
    result = merge_calendars(cals)
    assert result.color == "turquoise"


def test_merged_calendar_color_when_only_one_has_color(calendars):
    cals = calendars.color_none.stream + calendars.color_rfc7986.stream
    result = merge_calendars(cals)
    assert result.color == "turquoise"


@pytest.mark.parametrize("component_type", ["VEVENT", "VTODO", "VJOURNAL"])
def test_component_own_color_preserved_across_calendars(calendars, component_type):
    cals = calendars.color_event_own.stream + calendars.color_rfc7986.stream
    result = merge_calendars(cals)
    assert result.walk(component_type)[0].color == "navy"
