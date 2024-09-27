"""Test the usage of the templates."""

import pytest

MERGE_NAMES_TEMPLATE = """
VCALENDAR:
    attributes:
        NAME: >
            {% for calendar in calendars -%}
                {{ '' if loop.first else ', ' -}}
                {{ calendar.get("NAME", calendar.get("X-WR-CALNAME")) -}}
            {% endfor -%}
"""


@pytest.mark.parametrize(
    ("calendars", "template", "attr", "value"),
    [
        (["no_events.ics"], "", "NAME", None),
        (
            ["no_events.ics"],
            "VCALENDAR:\n attributes:\n  NAME: 'My Calendar'",
            "NAME",
            "My Calendar",
        ),
        (["no_events.ics"], MERGE_NAMES_TEMPLATE, "NAME", "test"),
        (["rfc_7986.ics"], MERGE_NAMES_TEMPLATE, "NAME", "7986"),
        (["no_events.ics", "rfc_7986.ics"], MERGE_NAMES_TEMPLATE, "NAME", "test, 7986"),
    ],
)
def test_tempalte_for_calendar(calendars, template, attr, value, merge):
    """Check that the merging works."""
    calendar = merge(calendars, template=template)
    assert calendar.get(attr) == value
