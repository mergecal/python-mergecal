from typing import Optional

from icalendar import Calendar, Event
from x_wr_timezone import to_standard


def generate_default_prodid() -> str:
    """Generate a default PRODID."""
    return "-//mergecal.org//MergeCal//EN"


class CalendarMerger:
    """Merge multiple calendars into one."""

    def __init__(
        self,
        calendars: list[Calendar],
        prodid: Optional[str] = None,
        version: str = "2.0",
        method: Optional[str] = None,
    ):
        self.merged_calendar = Calendar()

        # Set required properties
        self.merged_calendar.add("prodid", prodid or generate_default_prodid())
        self.merged_calendar.add("version", version)

        # Set optional properties if provided
        if method:
            self.merged_calendar.add("method", method)

        self.calendars: list[Calendar] = []

        for calendar in calendars:
            self.add_calendar(calendar)

    def add_calendar(self, calendar: Calendar) -> None:
        """Add a calendar to be merged."""
        self.calendars.append(to_standard(calendar, add_timezone_component=True))

    def merge(self) -> Calendar:
        """Merge the calendars."""
        existing_uids: set[tuple[Optional[str], int, Optional[str]]] = set()
        no_uid_events: list[Event] = []
        tzids: set[str] = set()
        for cal in self.calendars:
            for timezone in cal.timezones:
                if timezone.tz_name not in tzids:
                    self.merged_calendar.add_component(timezone)
                    tzids.add(timezone.tz_name)
            for component in cal.events:
                uid = component.get("uid", None)
                sequence = component.get("sequence", 0)
                recurrence_id = component.get("recurrence-id", None)

                # Create a unique identifier for the component
                component_id = (uid, sequence, recurrence_id)

                if uid is None:
                    if component in no_uid_events:
                        continue
                    no_uid_events.append(component)
                elif component_id in existing_uids:
                    continue

                existing_uids.add(component_id)
                self.merged_calendar.add_component(component)

        return self.merged_calendar


def merge_calendars(calendars: list[Calendar], **kwargs: object) -> Calendar:
    """Convenience function to merge calendars."""
    merger = CalendarMerger(calendars, **kwargs)  # type: ignore
    return merger.merge()


__all__ = ["CalendarMerger", "merge_calendars"]
