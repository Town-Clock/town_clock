"""
Test clock_tower.py
"""
from __future__ import annotations

import pytest
from icecream import ic

from town_clock import Clock, ClockTower, Time, Pulses
from town_clock.util import CLOCK, Mode


class MOCK_LEDRELAY:
    def turn_on(self):
        ...

    def turn_off(self):
        ...


class MOCK_ClockRelay:
    count: int = 0

    def pulse(self):
        self.count += 1
        ic(self.count)
        return self


MOCK_TIME = Time()
MOCK_POS: dict[str, float] = dict()

ONE = CLOCK.ONE
TWO = CLOCK.TWO


@pytest.fixture
def mock_clock_dict() -> dict[CLOCK, Clock]:
    return {
        ONE: Clock(
            ONE, relay=MOCK_ClockRelay(), time_on_clock=0, sleep_time=0.01
        ),
        TWO: Clock(
            TWO, relay=MOCK_ClockRelay(), time_on_clock=0, sleep_time=0.01
        ),
    }


@pytest.fixture
def default_town_clock(mock_clock_dict) -> ClockTower:
    return ClockTower(
        running=True,
        time=MOCK_TIME,
        mode=Mode.TEST,
        led=MOCK_LEDRELAY(),  # type: ignore
        clock=mock_clock_dict,
        position=MOCK_POS,
        pulse_interval=0.1,
    )


def test_clock_tower_instantiation(default_town_clock: ClockTower) -> None:
    assert isinstance(default_town_clock, ClockTower)


@pytest.mark.parametrize(
    "c1, c2, expected",
    ((5, 5, [5, 5]), (1, 5, [1, 5]), (0, -1, [0, 0])),
)
def test_clock_tower_slow_property(
        c1: int,
        c2: int,
        expected,
        default_town_clock: ClockTower,
) -> None:
    default_town_clock.clock[ONE].slow = c1
    default_town_clock.clock[TWO].slow = c2
    assert default_town_clock.slow == expected


@pytest.mark.parametrize(
    "c1, c2, expected",
    (
            (5, 5, [5, 5]),
            (1, 5, [1, 5]),
            (0, -1, [0, 0]),
    ),
)
def test_clock_tower_pulse(
        c1, c2, expected, default_town_clock: ClockTower
) -> None:
    default_town_clock.clock[ONE].slow = c1
    default_town_clock.clock[TWO].slow = c2
    default_town_clock.pulse()
    relay_clock_1 = default_town_clock.clock[ONE].relay.count  # type: ignore
    relay_clock_2 = default_town_clock.clock[TWO].relay.count  # type: ignore
    assert [relay_clock_1, relay_clock_2] == expected
