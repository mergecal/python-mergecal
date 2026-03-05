"""Select which components to merge (Issue #182)."""

import pytest

from mergecal import CalendarMerger, merge_calendars


def test_default_components_include_all_types(calendars):
    """All component types are merged by default."""
    result = merge_calendars(calendars.color_rfc7986.stream)

    assert len(list(result.events)) == 1
    assert len(list(result.todos)) == 1
    assert len(result.journals) == 1
    assert len(list(result.timezones)) == 0


@pytest.mark.parametrize(
    "components,num_events,num_todos,num_journals",
    [
        (["VEVENT"], 1, 0, 0),
        (["VTODO"], 0, 1, 0),
        (["VJOURNAL"], 0, 0, 1),
    ],
)
def test_select_single_component_type(
    calendars, components, num_events, num_todos, num_journals
):
    """Only the selected component type is merged."""
    result = merge_calendars(calendars.color_rfc7986.stream, components=components)

    assert len(list(result.events)) == num_events
    assert len(list(result.todos)) == num_todos
    assert len(result.journals) == num_journals
    assert len(list(result.timezones)) == 0


def test_events_include_required_timezones(calendars):
    """
    VTIMEZONEs required by events are generated even without VTIMEZONE in components.

    Timezones follow events automatically; the components list only filters event types.
    """
    result = merge_calendars(
        calendars.no_vtimezone_google.stream, components=["VEVENT"]
    )

    assert len(list(result.events)) == 2
    assert "America/New_York" in {tz.tz_name for tz in result.timezones}
    assert "Europe/London" in {tz.tz_name for tz in result.timezones}


def test_select_vtimezone_only(calendars):
    """components=['VTIMEZONE'] copies existing VTIMEZONE components, no events."""
    result = merge_calendars(calendars.one_event.stream, components=["VTIMEZONE"])

    assert len(list(result.events)) == 0
    assert len(list(result.timezones)) == 1


def test_calendar_merger_components_parameter(calendars):
    """CalendarMerger respects the components parameter."""
    result = CalendarMerger(
        calendars.color_rfc7986.stream, components=["VEVENT", "VTODO"]
    ).merge()

    assert len(list(result.events)) == 1
    assert len(list(result.todos)) == 1
    assert len(result.journals) == 0
    assert len(list(result.timezones)) == 0


def test_empty_components_list(calendars):
    """An empty components list produces an empty calendar."""
    result = merge_calendars(calendars.color_rfc7986.stream, components=[])

    assert len(list(result.events)) == 0
    assert len(list(result.todos)) == 0
    assert len(result.journals) == 0
    assert len(list(result.timezones)) == 0


def test_generate_vtimezone_false_disables_generation(calendars):
    """generate_vtimezone=False suppresses all VTIMEZONE output."""
    result = merge_calendars(
        calendars.no_vtimezone_google.stream, generate_vtimezone=False
    )

    assert len(list(result.timezones)) == 0


def test_multiple_calendars_component_filtering(calendars):
    """Component filtering applies across all merged calendars."""
    cals = calendars.one_event.stream + calendars.color_rfc7986.stream
    result = merge_calendars(cals, components=["VEVENT"])

    assert len(list(result.events)) == 2
    assert len(list(result.todos)) == 0
    assert len(result.journals) == 0


def test_unknown_components_silently_ignored(calendars):
    """Unknown component names do not crash the merger."""
    result = CalendarMerger(
        calendars.test_empty_calendar.stream, components=["VEVENT", "UNKNOWN"]
    ).merge()

    assert len(list(result.events)) == 0
