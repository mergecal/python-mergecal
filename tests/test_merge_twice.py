"""Tests that CalendarMerger.merge() follows the Method Object pattern."""

import pytest

from mergecal import CalendarMerger


def test_merge_called_twice_raises(calendars):
    merger = CalendarMerger(calendars.one_event.stream)
    merger.merge()
    with pytest.raises(RuntimeError, match="merge\\(\\) can only be called once"):
        merger.merge()
