from typing import Optional
from zoneinfo import ZoneInfo

from icalendar import Calendar


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

    def add_calendar(self, calendar: Calendar) -> None:
        """Add a calendar to be merged."""
        self.calendars.append(calendar)

    def merge(self) -> Calendar:
        """Merge the calendars."""
        exisitng_uids = set()
        for cal in self.calendars:
            for component in cal.walk("VEVENT"):
                uid = component.get("uid", None)
                sequence = component.get("sequence", 0)
                recurrence_id = component.get("recurrence-id", None)
                if recurrence_id:
                    recurrence_id = recurrence_id.dt.astimezone(ZoneInfo("UTC"))
                if (uid, sequence, recurrence_id) in exisitng_uids:
                    continue
                exisitng_uids.add((uid, sequence, recurrence_id))

                self.merged_calendar.add_component(component)

        return self.merged_calendar


def merge_calendars(calendars: list[Calendar], **kwargs: object) -> Calendar:
    """Convenience function to merge calendars."""
    merger = CalendarMerger(calendars, **kwargs)  # type: ignore
    return merger.merge()


__all__ = ["CalendarMerger", "merge_calendars"]
