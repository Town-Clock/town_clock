"""
test for _time.py

Author: Zack Hankin
Started: 12/02/2023
"""
from __future__ import annotations

import pendulum
import pytest
from pendulum import DateTime

from town_clock.clock import Time

TZ = pendulum.timezone("Australia/Sydney")

TEST_DEFAULT_TIME: DateTime = pendulum.DateTime(
    year=2013, month=3, day=31, hour=12, minute=0, second=0, microsecond=0, tzinfo=TZ
)

MIDNIGHT_MIDDAY: list[DateTime] = [
    pendulum.DateTime(
        year=2013,
        month=3,
        day=31,
        hour=12,
        minute=0,
        second=0,
        microsecond=0,
        tzinfo=TZ,
    ),
    pendulum.DateTime(
        year=2013, month=3, day=31, hour=0, minute=0, second=0, microsecond=0, tzinfo=TZ
    ),
]

DAYLIGHT_SAVING_ENDING_TIME: DateTime = pendulum.DateTime(
    year=2023,
    month=4,
    day=2,
    hour=2,
    minute=59,
    second=0,
    microsecond=0,
    tzinfo=TZ,
)

DAYLIGHT_SAVING_STARTING_TIME: DateTime = pendulum.DateTime(
    year=2023,
    month=10,
    day=1,
    hour=1,
    minute=59,
    second=0,
    microsecond=0,
    tzinfo=TZ,
)


def test_time_instantiation() -> None:
    t = Time(MIDNIGHT_MIDDAY[0])
    assert isinstance(t, Time)


@pytest.mark.parametrize(("test_input", "expected"), [(t, 0) for t in MIDNIGHT_MIDDAY])
def test_time_clock_time_equals_zero(test_input, expected) -> None:
    t = Time(test_input)
    t.set_clock_time(t.now)
    assert t.clock_time == expected


@pytest.mark.parametrize(
    ("hour", "minute", "expected"),
    (
            (1, 0, 60),
            (2, 0, 120),
            (13, 0, 60),
            (14, 0, 120),
            (11, 0, 660),
            (0, 45, 45),
            (23, 59, 719),
            (11, 59, 719),
    ),
)
def test_time_clock_time_equals(hour, minute, expected) -> None:
    t = Time(pendulum.DateTime(2013, 3, 31, hour, minute, tzinfo=TZ))
    t.set_clock_time(t.now)
    assert t.clock_time == expected


@pytest.mark.parametrize(
    ("second", "microsecond", "expected"),
    (
            (0, 0, True),
            (0, 999999, True),
            (1, 0, False),
            (59, 999999, False),
            (30, 8319, False),
    ),
)
def test_time_is_on_minute(second, microsecond, expected) -> None:
    temp_time = pendulum.DateTime(2013, 3, 31, 0, 0, second, microsecond, tzinfo=TZ)
    t = Time(TEST_DEFAULT_TIME)
    on_minute = t(temp_time)
    assert t.now == temp_time
    assert on_minute == expected


def test_time_daylight_savings_ending() -> None:
    t = Time(DAYLIGHT_SAVING_ENDING_TIME)
    assert t.now.is_dst()
    clock_time = t.clock_time
    t(t.now.add(minutes=1))
    assert not t.now.is_dst()
    assert clock_time - t.clock_time == 59


def test_time_daylight_savings_starting() -> None:
    t = Time(DAYLIGHT_SAVING_STARTING_TIME)
    assert not t.now.is_dst()
    clock_time = t.clock_time
    t(t.now.add(minutes=1))
    assert t.now.is_dst()
    assert t.clock_time - clock_time == 61
