from __future__ import annotations

from dataclasses import dataclass, field

from icalendar import Calendar, Component, Timezone
from x_wr_timezone import to_standard

ComponentId = tuple[str, int, str | None]

# Avoids expensive re-generation of VTIMEZONE components across CalendarMerger
# instances.
_timezone_cache: dict[str, Timezone] = {}

DEFAULT_COMPONENTS = ["VEVENT", "VTIMEZONE"]


def calendars_from_ical(data: bytes) -> list[Calendar]:
    """Parse ICS data, returning one Calendar per VCALENDAR component found."""
    return Calendar.from_ical(data, multiple=True)


def generate_default_prodid() -> str:
    """Generate a default PRODID."""
    return "-//mergecal.org//MergeCal//EN"


@dataclass
class _ComponentTracker:
    target: Calendar
    seen: set[ComponentId] = field(default_factory=set)
    no_uid: list[Component] = field(default_factory=list)

    def add(self, component: Component, calendar_color: str | None) -> None:
        uid = component.uid
        component_id: ComponentId = (
            uid,
            component.sequence,
            component.get("recurrence-id", None),
        )
        if not uid:
            if component in self.no_uid:
                return
            self.no_uid.append(component)
        else:
            if component_id in self.seen:
                return
            self.seen.add(component_id)
        if calendar_color and not component.color:
            component.color = calendar_color
        self.target.add_component(component)


class CalendarMerger:
    """Merge multiple calendars into one."""

    def __init__(
        self,
        calendars: list[Calendar],
        prodid: str | None = None,
        version: str = "2.0",
        calscale: str = "GREGORIAN",
        method: str | None = None,
        generate_vtimezone: bool = True,
        components: list[str] | None = None,
    ):
        self.merged_calendar = Calendar()

        self.merged_calendar.add("prodid", prodid or generate_default_prodid())
        self.merged_calendar.add("version", version)
        self.merged_calendar.add("calscale", calscale)

        if method:
            self.merged_calendar.add("method", method)

        self.calendars: list[Calendar] = []
        self._merged = False
        self.generate_vtimezone = generate_vtimezone
        self.components = (
            [c.strip().upper() for c in components if c.strip()]
            if components is not None
            else list(DEFAULT_COMPONENTS)
        )

        for calendar in calendars:
            self.add_calendar(calendar)

    def _get_components(self, cal: Calendar) -> list[Component]:
        result: list[Component] = []
        if "VEVENT" in self.components:
            result.extend(cal.events)
        if "VTODO" in self.components:
            result.extend(cal.todos)
        if "VJOURNAL" in self.components:
            result.extend(cal.walk("VJOURNAL"))
        return result

    def _should_generate_timezones(self) -> bool:
        return "VTIMEZONE" in self.components and self.generate_vtimezone

    def add_calendar(self, calendar: Calendar) -> None:
        """Add a calendar to be merged."""
        cal = to_standard(
            calendar, add_timezone_component=self._should_generate_timezones()
        )

        if self._should_generate_timezones():
            for tz in cal.timezones:
                if tz.tz_name not in _timezone_cache:
                    _timezone_cache[tz.tz_name] = tz

            # to_standard() may add a VTIMEZONE even when one already exists for
            # the same TZID, causing get_missing_tzids() to raise KeyError
            # (collective/icalendar#1124). Deduplicate before calling
            # add_missing_timezones(). Also drop VTIMEZONEs not referenced by
            # any component — get_missing_tzids() assumes every VTIMEZONE is
            # used, so an unreferenced one causes a KeyError too.
            used_tzids = cal.get_used_tzids()
            seen_tzids: set[str] = set()
            deduped: list[Component] = []
            for c in cal.subcomponents:
                if isinstance(c, Timezone):
                    if c.tz_name in seen_tzids or c.tz_name not in used_tzids:
                        continue
                    seen_tzids.add(c.tz_name)
                deduped.append(c)
            cal.subcomponents[:] = deduped

            if cal.get_used_tzids():
                missing_tzids = cal.get_missing_tzids()

                for tzid in missing_tzids:
                    if tzid in _timezone_cache:
                        cal.add_component(_timezone_cache[tzid])

                remaining = cal.get_missing_tzids()
                if remaining:
                    cal.add_missing_timezones()
                    for tz in cal.timezones:
                        if tz.tz_name in remaining:
                            _timezone_cache[tz.tz_name] = tz

        self.calendars.append(cal)

    def merge(self) -> Calendar:
        """Merge the calendars."""
        if self._merged:
            raise RuntimeError(
                "merge() can only be called once; "
                "create a new CalendarMerger instance to merge again"
            )
        self._merged = True
        tracker = _ComponentTracker(self.merged_calendar)
        tzids: set[str] = set()

        for cal in self.calendars:
            # .color resolves COLOR then X-APPLE-CALENDAR-COLOR (RFC 7986 §5.9)
            calendar_color = cal.color

            if calendar_color and not self.merged_calendar.color:
                self.merged_calendar.color = calendar_color

            if "VTIMEZONE" in self.components:
                for timezone in cal.timezones:
                    if timezone.tz_name == "UTC":
                        # UTC needs no VTIMEZONE per RFC 5545 §3.6.5; skip spurious
                        # entries generated by add_missing_timezones()
                        # (collective/icalendar#1124)
                        continue
                    if timezone.tz_name not in tzids:
                        self.merged_calendar.add_component(timezone)
                        tzids.add(timezone.tz_name)

            for component in self._get_components(cal):
                tracker.add(component, calendar_color)

        return self.merged_calendar


def merge_calendars(
    calendars: list[Calendar],
    generate_vtimezone: bool = True,
    components: list[str] | None = None,
    **kwargs: object,
) -> Calendar:
    """Convenience function to merge calendars."""
    merger = CalendarMerger(
        calendars,
        generate_vtimezone=generate_vtimezone,
        components=components,
        **kwargs,  # type: ignore[arg-type]
    )
    return merger.merge()


__all__ = ["CalendarMerger", "calendars_from_ical", "merge_calendars"]
