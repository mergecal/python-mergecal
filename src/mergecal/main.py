from typing import List

from icalendar import Calendar


def merge(calendars: List[Calendar]) -> Calendar:
    """
    Merge multiple Calendar objects into a single calendar.

    Args:
    calendars (List[Calendar]): List of calendars to merge

    Returns:
    Calendar: Merged calendar

    """
    merged_cal = Calendar()

    # Copy properties from the first calendar
    for prop in calendars[0].property_items():
        if prop[0] != "VERSION":  # Skip VERSION as we'll set it explicitly
            merged_cal.add(prop[0], prop[1])

    # Ensure the VERSION is set to 2.0
    merged_cal["VERSION"] = "2.0"

    # Merge components (events, todos, etc.) from all calendars
    for cal in calendars:
        for component in cal.walk():
            if component.name != "VCALENDAR":
                merged_cal.add_component(component)

    return merged_cal


# Keep the original add function for backward compatibility
def add(n1: int, n2: int) -> int:
    """Add the arguments."""
    return n1 + n2
