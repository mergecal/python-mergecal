# Python MergeCal

<p align="center">
  <a href="https://github.com/mergecal/python-mergecal/actions/workflows/ci.yml?query=branch%3Amain">
    <img src="https://img.shields.io/github/actions/workflow/status/mergecal/python-mergecal/ci.yml?branch=main&label=CI&logo=github&style=flat-square" alt="CI Status" >
  </a>
  <a href="https://mergecal.readthedocs.io">
    <img src="https://img.shields.io/readthedocs/mergecal.svg?logo=read-the-docs&logoColor=fff&style=flat-square" alt="Documentation Status">
  </a>
  <a href="https://codecov.io/gh/mergecal/python-mergecal">
    <img src="https://img.shields.io/codecov/c/github/mergecal/python-mergecal.svg?logo=codecov&logoColor=fff&style=flat-square" alt="Test coverage percentage">
  </a>
</p>
<p align="center">
  <a href="https://python-poetry.org/">
    <img src="https://img.shields.io/endpoint?url=https://python-poetry.org/badge/v0.json" alt="Poetry">
  </a>
  <a href="https://github.com/astral-sh/ruff">
    <img src="https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json" alt="Ruff">
  </a>
  <a href="https://github.com/pre-commit/pre-commit">
    <img src="https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white&style=flat-square" alt="pre-commit">
  </a>
</p>
<p align="center">
  <a href="https://pypi.org/project/mergecal/">
    <img src="https://img.shields.io/pypi/v/mergecal.svg?logo=python&logoColor=fff&style=flat-square" alt="PyPI Version">
  </a>
  <img src="https://img.shields.io/pypi/pyversions/mergecal.svg?style=flat-square&logo=python&amp;logoColor=fff" alt="Supported Python versions">
  <img src="https://img.shields.io/pypi/l/mergecal.svg?style=flat-square" alt="License">
</p>

---

**Documentation**: <a href="https://mergecal.readthedocs.io" target="_blank">https://mergecal.readthedocs.io </a>

**Source Code**: <a href="https://github.com/mergecal/python-mergecal" target="_blank">https://github.com/mergecal/python-mergecal </a>

---

A Python library to merge iCalendar feeds.

## Installation

Install this via pip (or your favorite package manager):

```bash
pip install mergecal
```

## Usage

### Python API

You can use MergeCal in your Python code as follows:

```python
>>> from mergecal import merge_calendars
>>> from icalendar import Calendar

# Load your calendars
# CALENDARS = pathlib.Path("to/your/calendar/directory")
>>> calendar1 = Calendar.from_ical((CALENDARS / "one_event.ics").read_bytes())
>>> calendar2 = Calendar.from_ical((CALENDARS / "another_event.ics").read_bytes())

# Merge the calendars
>>> merged_calendar : Calendar = merge_calendars([calendar1, calendar2])

# Write the merged calendar to a file
>>> with (CALENDARS / "merged_calendar.ics").open("wb") as f:
...     f.write(merged_calendar.to_ical())
559

# The merged calendar will contain all the events of both calendars
>>> [str(event["SUMMARY"]) for event in calendar1.walk("VEVENT")]
['Event 1']
>>> [str(event["SUMMARY"]) for event in calendar2.walk("VEVENT")]
['Event 2']
>>> [str(event["SUMMARY"]) for event in merged_calendar.walk("VEVENT")]
['Event 1', 'Event 2']

```

### Command Line Interface (CLI)

MergeCal also provides a command-line interface for easy merging of calendar files:

```bash
# Basic usage
mergecal calendar1.ics calendar2.ics -o merged_calendar.ics

# Specifying custom PRODID
mergecal calendar1.ics calendar2.ics -o merged_calendar.ics --prodid "-//My Organization//MergeCal 1.0//EN"

```

For more options and information, use the help command:

```bash
mergecal --help
```

## Contributors ✨

Thanks goes to these wonderful people ([emoji key](https://allcontributors.org/docs/en/emoji-key)):

<!-- prettier-ignore-start -->
<!-- ALL-CONTRIBUTORS-LIST:START - Do not remove or modify this section -->
<!-- markdownlint-disable -->
<!-- markdownlint-enable -->
<!-- ALL-CONTRIBUTORS-LIST:END -->
<!-- prettier-ignore-end -->

This project follows the [all-contributors](https://github.com/all-contributors/all-contributors) specification. Contributions of any kind welcome!

## Credits

This package was created with
[Copier](https://copier.readthedocs.io/) and the
[browniebroke/pypackage-template](https://github.com/browniebroke/pypackage-template)
project template.
