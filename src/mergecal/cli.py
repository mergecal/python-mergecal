from pathlib import Path
from typing import Optional

import typer
from icalendar import Calendar
from rich import print

from .calendar_merger import CalendarMerger

app = typer.Typer()

# Define arguments and options outside of the function
calendars_arg = typer.Argument(..., help="Paths to the calendar files to merge")
output_opt = typer.Option(
    "merged_calendar.ics", "--output", "-o", help="Output file path"
)
prodid_opt = typer.Option(None, "--prodid", help="Product ID for the merged calendar")
method_opt = typer.Option(None, "--method", help="Calendar method")


@app.command()
def main(
    calendars: list[Path] = calendars_arg,
    output: Path = output_opt,
    prodid: Optional[str] = prodid_opt,
    method: Optional[str] = method_opt,
) -> None:
    """Merge multiple iCalendar files into one."""
    try:
        calendar_objects = []
        for calendar_path in calendars:
            with open(calendar_path, "rb") as cal_file:
                calendar_objects.append(Calendar.from_ical(cal_file.read()))

        merger = CalendarMerger(
            calendars=calendar_objects, prodid=prodid, method=method
        )
        merged_calendar = merger.merge()

        with open(output, "wb") as output_file:
            output_file.write(merged_calendar.to_ical())

        print(f"[green]Successfully merged calendars into {output}[/green]")
    except Exception as e:
        print(f"[red]Error merging calendars: {e!s}[/red]")


if __name__ == "__main__":
    app()
