"""Select which components to merge (Issue #182)."""

from mergecal import CalendarMerger, merge_calendars


def test_default_components_vevent_and_vtimezone_only(calendars):
    """Only VEVENT and VTIMEZONE are merged by default."""
    result = merge_calendars(calendars.color_rfc7986.stream)

    assert len(list(result.events)) == 1
    assert len(list(result.todos)) == 0
    assert len(list(result.walk("VJOURNAL"))) == 0


def test_select_events_only(calendars):
    """Only VEVENTs are merged; no timezones when VTIMEZONE excluded."""
    result = merge_calendars(calendars.color_rfc7986.stream, components=["VEVENT"])

    assert len(list(result.events)) == 1
    assert len(list(result.todos)) == 0
    assert len(list(result.walk("VJOURNAL"))) == 0
    assert len(list(result.timezones)) == 0


def test_select_todos_only(calendars):
    """Only VTODOs are merged."""
    result = merge_calendars(calendars.color_rfc7986.stream, components=["VTODO"])

    assert len(list(result.events)) == 0
    assert len(list(result.todos)) == 1
    assert len(list(result.timezones)) == 0


def test_select_journals_only(calendars):
    """Only VJOURNALs are merged."""
    result = merge_calendars(calendars.color_rfc7986.stream, components=["VJOURNAL"])

    assert len(list(result.events)) == 0
    assert len(list(result.todos)) == 0
    assert len(list(result.walk("VJOURNAL"))) == 1
    assert len(list(result.timezones)) == 0


def test_select_events_and_timezones(calendars):
    """Timezones are generated when VTIMEZONE is included in components."""
    result = merge_calendars(
        calendars.no_vtimezone_google.stream, components=["VEVENT", "VTIMEZONE"]
    )

    assert len(list(result.events)) == 2
    assert len(list(result.timezones)) > 0


def test_calendar_merger_components_parameter(calendars):
    """CalendarMerger respects the components parameter."""
    result = CalendarMerger(
        calendars.color_rfc7986.stream, components=["VEVENT", "VTODO"]
    ).merge()

    assert len(list(result.events)) == 1
    assert len(list(result.todos)) == 1
    assert len(list(result.walk("VJOURNAL"))) == 0
    assert len(list(result.timezones)) == 0


def test_empty_components_list(calendars):
    """An empty components list produces an empty calendar."""
    result = merge_calendars(calendars.color_rfc7986.stream, components=[])

    assert len(list(result.events)) == 0
    assert len(list(result.todos)) == 0
    assert len(list(result.walk("VJOURNAL"))) == 0
    assert len(list(result.timezones)) == 0


def test_timezone_generation_only_when_vtimezone_in_components(calendars):
    """generate_vtimezone has no effect when VTIMEZONE is not in the components list."""
    cals = calendars.no_vtimezone_google.stream

    result_with = merge_calendars(
        cals, components=["VEVENT", "VTIMEZONE"], generate_vtimezone=True
    )
    result_without = merge_calendars(
        cals, components=["VEVENT"], generate_vtimezone=True
    )

    assert len(list(result_with.timezones)) > 0
    assert len(list(result_without.timezones)) == 0


def test_multiple_calendars_component_filtering(calendars):
    """Component filtering applies across all merged calendars."""
    cals = calendars.one_event.stream + calendars.color_rfc7986.stream
    result = merge_calendars(cals, components=["VEVENT"])

    assert len(list(result.events)) == 2
    assert len(list(result.todos)) == 0
    assert len(list(result.walk("VJOURNAL"))) == 0


def test_unknown_components_silently_ignored(calendars):
    """Unknown component names do not crash the merger."""
    cals = calendars.test_empty_calendar.stream

    result = CalendarMerger(cals, components=["VEVENT", "UNKNOWN"]).merge()

    assert len(list(result.events)) == 0
