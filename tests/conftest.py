"""Mergcal test parametrization and other functions."""

from pathlib import Path

import icalendar
import pytest
from typer.testing import CliRunner

from mergecal import merge_calendars
from mergecal.cli import app

HERE = Path(__file__).parent
CALENDARS_DIR = HERE / "calendars"


def merge_func(calendars: list[str]) -> icalendar.Calendar:
    """Use the main merge function to merge the calendars."""
    icalendars = []
    for calendar in calendars:
        if isinstance(calendar, icalendar.Calendar):
            icalendars.append(calendar)
            continue
        if not calendar.endswith(".ics"):
            calendar += ".ics"
        calendar_path = CALENDARS_DIR / calendar
        icalendars.append(icalendar.Calendar.from_ical(calendar_path.read_bytes()))
    return merge_calendars(icalendars)


def merge_cli(calendars: list[str]) -> None:
    """Use the main CLI to merge the calendars."""
    runner = CliRunner()
    calendar_paths = []
    for calendar in calendars:
        if not calendar.endswith(".ics"):
            calendar += "/.ics"
        calendar_paths.append(CALENDARS_DIR / calendar)
    result = runner.invoke(app, calendar_paths)
    assert result.exit_code == 0, "Calendars should merge without error."
    return icalendar.Calendar.from_ical(result.output)


@pytest.fixture(params=[merge_cli, merge_func])
def merge():
    """Fixture for the merge function."""
    return merge_func


class ICSCalendars:
    """A collection of parsed ICS calendars."""

    def get_calendar(self, content):
        """Return the calendar given the content."""
        return icalendar.Calendar.from_ical(content)

    def __getitem__(self, name):
        """Return the calendar from the calendars directory."""
        return getattr(self, name)

    @staticmethod
    def keys() -> list[str]:
        """The names of all calendars."""
        return [calendar_path.stem for calendar_path in CALENDARS_DIR.iterdir()]


for calendar_path in CALENDARS_DIR.iterdir():
    content = calendar_path.read_bytes()

    def get_calendar(
        self: ICSCalendars, content: bytes = content
    ) -> icalendar.Calendar:
        return self.get_calendar(content)

    setattr(ICSCalendars, calendar_path.stem, property(get_calendar))


@pytest.fixture
def calendars() -> ICSCalendars:
    """Fixture to easy access parsed calendars from the test/calendars directory."""
    return ICSCalendars()


@pytest.fixture(params=ICSCalendars.keys())
def a_calendar(request):
    """Return a calendar."""
    return request.param


def doctest_print(obj):
    """Doctest print."""
    if isinstance(obj, bytes):
        obj = obj.decode("UTF-8")
    print(str(obj).strip().replace("\r\n", "\n").replace("\r", "\n"))


@pytest.fixture()
def env_for_doctest(monkeypatch):
    """Modify the environment to make doctests run."""
    return {
        "print": doctest_print,
        "CALENDARS": CALENDARS_DIR,
    }
