from pathlib import Path

import typer
from rich import print

from .calendar_merger import CalendarMerger, calendars_from_ical

app = typer.Typer()

calendars_arg = typer.Argument(..., help="Paths to the calendar files to merge")
output_opt = typer.Option(
    "merged_calendar.ics", "--output", "-o", help="Output file path"
)
prodid_opt = typer.Option(None, "--prodid", help="Product ID for the merged calendar")
method_opt = typer.Option(None, "--method", help="Calendar method")
no_generate_vtimezone_opt = typer.Option(
    False,
    "--no-generate-vtimezone",
    help=(
        "Do not generate missing VTIMEZONE components although they might be"
        " required. This increases performance."
    ),
)
components_opt = typer.Option(
    None,
    "--components",
    help="Comma-separated component types to merge (VEVENT,VTODO,VJOURNAL,VTIMEZONE)",
)


@app.command()
def main(
    calendars: list[Path] = calendars_arg,
    output: Path = output_opt,
    prodid: str | None = prodid_opt,
    method: str | None = method_opt,
    no_generate_vtimezone: bool = no_generate_vtimezone_opt,
    components: str | None = components_opt,
) -> None:
    """Merge multiple iCalendar files into one."""
    try:
        calendar_objects = []
        for calendar_path in calendars:
            with open(calendar_path, "rb") as cal_file:
                calendar_objects.extend(calendars_from_ical(cal_file.read()))

        merger = CalendarMerger(
            calendars=calendar_objects,
            prodid=prodid,
            method=method,
            generate_vtimezone=not no_generate_vtimezone,
            components=(
                [p.strip() for p in components.split(",") if p.strip()]
                if components
                else None
            ),
        )
        merged_calendar = merger.merge()

        with open(output, "wb") as output_file:
            output_file.write(merged_calendar.to_ical())

        print(f"[green]Successfully merged calendars into {output}[/green]")
    except Exception as e:
        print(f"[red]Error merging calendars: {e!s}[/red]")


if __name__ == "__main__":
    app()
