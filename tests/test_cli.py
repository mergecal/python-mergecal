from datetime import datetime

from icalendar import Calendar, Event
from typer.testing import CliRunner

from mergecal.cli import app

runner = CliRunner()


def create_test_calendar_file(filename, summary, dtstart):
    cal = Calendar()
    event = Event()
    event.add("summary", summary)
    event.add("dtstart", dtstart)
    cal.add_component(event)

    with open(filename, "wb") as f:
        f.write(cal.to_ical())


def test_mergecal_cli(tmp_path):
    # Create two test calendar files
    cal1_path = tmp_path / "cal1.ics"
    cal2_path = tmp_path / "cal2.ics"
    output_path = tmp_path / "merged.ics"

    create_test_calendar_file(cal1_path, "Test Event 1", datetime(2023, 1, 1, 9, 0, 0))
    create_test_calendar_file(cal2_path, "Test Event 2", datetime(2023, 1, 2, 10, 0, 0))

    # Run the CLI command
    result = runner.invoke(
        app, [str(cal1_path), str(cal2_path), "-o", str(output_path)]
    )

    # Check that the command was successful
    assert result.exit_code == 0
    assert "Successfully merged calendars" in result.stdout

    # Verify the merged calendar file
    assert output_path.exists()

    with open(output_path, "rb") as f:
        merged_cal = Calendar.from_ical(f.read())

    events = [
        component for component in merged_cal.walk() if component.name == "VEVENT"
    ]
    assert len(events) == 2
    assert events[0]["summary"] == "Test Event 1"
    assert events[1]["summary"] == "Test Event 2"
