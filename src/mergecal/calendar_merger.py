from typing import Optional

from icalendar import Calendar
from jinja2.nativetypes import NativeEnvironment
from yaml import safe_load


def generate_default_prodid() -> str:
    """Generate a default PRODID."""
    return "-//mergecal.org//MergeCal//EN"


TYPE_TEMPLATE = dict[str, dict[str, str]]


class CalendarMerger:
    """Merge multiple calendars into one."""

    def __init__(
        self,
        calendars: list[Calendar],
        prodid: Optional[str] = None,
        version: str = "2.0",
        method: Optional[str] = None,
        template: str | TYPE_TEMPLATE = "",
    ):
        if not calendars:
            raise ValueError("At least one calendar must be provided")

        self.merged_calendar = Calendar()

        # Set required properties
        self.merged_calendar.add("prodid", prodid or generate_default_prodid())
        self.merged_calendar.add("version", version)

        # Set optional properties if provided
        if method:
            self.merged_calendar.add("method", method)

        self.calendars: list[Calendar] = calendars

        self.template: TYPE_TEMPLATE = (
            safe_load(template) or {} if isinstance(template, str) else template
        )

    def add_calendar(self, calendar: Calendar) -> None:
        """Add a calendar to be merged."""
        self.calendars.append(calendar)

    def merge(self) -> Calendar:
        """Merge the calendars."""
        # template the calendar
        env = NativeEnvironment()
        calendar_template = self.template.get("VCALENDAR", {})
        calendar_attributes_template = calendar_template.get(  # type: ignore
            "attributes", {}
        )
        for attribute in sorted(calendar_attributes_template.keys()):  # type: ignore
            attribute_template = calendar_attributes_template[attribute]
            value = env.from_string(attribute_template).render(
                calendars=self.calendars, attribute=attribute
            )
            self.merged_calendar.add(attribute, value)
        # add events
        for cal in self.calendars:
            for component in cal.walk("VEVENT"):
                self.merged_calendar.add_component(component)

        return self.merged_calendar


def merge_calendars(calendars: list[Calendar], **kwargs: object) -> Calendar:
    """Convenience function to merge calendars."""
    merger = CalendarMerger(calendars, **kwargs)  # type: ignore
    return merger.merge()


__all__ = ["CalendarMerger", "merge_calendars"]
