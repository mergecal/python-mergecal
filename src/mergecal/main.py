from __future__ import annotations

from icalendar import Calendar


def generate_default_prodid() -> str:
    """Generate a default PRODID."""
    return "-//mergecal.org//MergeCal//EN"


class CalendarMerger:
    """Merge multiple calendars into one."""

    def __init__(
        self,
        calendars: list[Calendar],
        prodid: str | None = None,
        version: str = "2.0",
        calscale: str | None = None,
        method: str | None = None,
    ):
        if not calendars:
            raise ValueError("At least one calendar must be provided")

        self.merged_calendar = Calendar()

        # Set required properties
        self.merged_calendar.add("prodid", prodid or generate_default_prodid())
        self.merged_calendar.add("version", version)

        # Set optional properties if provided
        if calscale:
            self.merged_calendar.add("calscale", calscale)
        if method:
            self.merged_calendar.add("method", method)

        self.calendars: list[Calendar] = calendars

    def add_calendar(self, calendar: Calendar) -> None:
        """Add a calendar to be merged."""
        self.calendars.append(calendar)

    def merge(self) -> Calendar:
        """Merge the calendars."""
        for cal in self.calendars:
            for component in cal.walk("VEVENT"):
                self.merged_calendar.add_component(component)

        return self.merged_calendar


def merge_calendars(calendars: list[Calendar], **kwargs: object) -> Calendar:
    """Convenience function to merge calendars."""
    merger = CalendarMerger(calendars, **kwargs)  # type: ignore
    return merger.merge()


# Keep the original add function for backward compatibility
def add(n1: int, n2: int) -> int:
    """Add the arguments."""
    return n1 + n2
