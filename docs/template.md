(template)=

# Template

Mergecal allows changing the events and calendars that are in use.
We use [Jinja] for this.

Calendars are merged component by component.
So, the templating looks like this:

```yaml
# change each calendar
VCALENDAR:
  attributes:
    # set the X-MERGED to value
    X-MERGED: "true"
    # use the RFC 7986
    NAME: '{{ VCALENDAR.get("NAME", VCALENDAR.get("X-WR-CALNAME")) }}'
    DESCRIPTION: '{{ VCALENDAR.get("DESCRIPTION", VCALENDAR.get("X-WR-CALDESC")) }}'

VEVENT:
  attributes:
    # set the color according to RFC 7986
    # we can use VCALENDAR here because we are inside the calendar
    COLOR: '{{ VEVENT.get("COLOR", VCALENDAR.get("X-APPLE-CALENDAR-COLOR")) }}'
```

[Jinja]: https://jinja.palletsprojects.com/
