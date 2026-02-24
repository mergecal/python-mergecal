from dataclasses import dataclass, field

from icalendar import Calendar, Component
from x_wr_timezone import to_standard

ComponentId = tuple[str | None, int, str | None]


def calendars_from_ical(data: bytes) -> list[Calendar]:
    """Parse ICS data, returning one Calendar per VCALENDAR component found."""
    return Calendar.from_ical(data, multiple=True)


def generate_default_prodid() -> str:
    """Generate a default PRODID."""
    return "-//mergecal.org//MergeCal//EN"


@dataclass
class _ComponentTracker:
    seen: set[ComponentId] = field(default_factory=set)
    no_uid: list[Component] = field(default_factory=list)

    def add(
        self, component: Component, cal_color: str | None, target: Calendar
    ) -> None:
        uid = component.get("uid", None)
        component_id: ComponentId = (
            uid,
            component.get("sequence", 0),
            component.get("recurrence-id", None),
        )
        if uid is None:
            if component in self.no_uid:
                return
            self.no_uid.append(component)
        else:
            if component_id in self.seen:
                return
            self.seen.add(component_id)
        if cal_color and not component.color:
            component.color = cal_color
        target.add_component(component)


class CalendarMerger:
    """Merge multiple calendars into one."""

    def __init__(
        self,
        calendars: list[Calendar],
        prodid: str | None = None,
        version: str = "2.0",
        calscale: str = "GREGORIAN",
        method: str | None = None,
    ):
        self.merged_calendar = Calendar()

        self.merged_calendar.add("prodid", prodid or generate_default_prodid())
        self.merged_calendar.add("version", version)
        self.merged_calendar.add("calscale", calscale)

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
        events = _ComponentTracker()
        todos = _ComponentTracker()
        journals = _ComponentTracker()
        tzids: set[str] = set()

        for cal in self.calendars:
            # .color resolves COLOR then X-APPLE-CALENDAR-COLOR (RFC 7986 §5.9)
            cal_color = cal.color

            if cal_color and not self.merged_calendar.color:
                self.merged_calendar.color = cal_color

            for timezone in cal.timezones:
                if timezone.tz_name not in tzids:
                    self.merged_calendar.add_component(timezone)
                    tzids.add(timezone.tz_name)

            for event in cal.events:
                events.add(event, cal_color, self.merged_calendar)
            for todo in cal.todos:
                todos.add(todo, cal_color, self.merged_calendar)
            for journal in cal.walk("VJOURNAL"):  # icalendar has no .journals property
                journals.add(journal, cal_color, self.merged_calendar)

        return self.merged_calendar


def merge_calendars(calendars: list[Calendar], **kwargs: object) -> Calendar:
    """Convenience function to merge calendars."""
    merger = CalendarMerger(calendars, **kwargs)  # type: ignore
    return merger.merge()


__all__ = ["CalendarMerger", "calendars_from_ical", "merge_calendars"]
