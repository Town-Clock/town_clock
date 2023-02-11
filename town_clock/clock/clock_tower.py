"""
ClockTower module.
"""
from __future__ import annotations
import time
from dataclasses import dataclass
from typing import NamedTuple, Protocol, Sequence

from town_clock.clock.relay import Relay
from town_clock.util import Mode
from .clock import Clock
from loguru import logger

from util import CLOCK

ONE = CLOCK.ONE
TWO = CLOCK.TWO


@dataclass(slots=True)
class Pulses:
    """Class to control the Pulse amount"""

    one: int
    two: int

    def __eq__(self, other: Pulses | Sequence) -> bool:
        if isinstance(other, Pulses):
            return self == other
        else:
            return (self.one == other[0]) and (self.two == other[1])


class LEDRelay(Protocol):
    """LED Relay Protocol"""

    ...


@dataclass(slots=True)
class ClockTower:
    """
    Controls the flow of information between the ui and the clocks.
    """

    def __init__(
        self,
        led: LEDRelay,
        position: dict[str, float],
        clock_dict: dict[CLOCK, Clock],
        mode: Mode = Mode.ACTIVE,
        pulse_interval: float = 0.5,
    ) -> None:
        self.mode = mode
        self.led: LEDRelay = led
        self.pulse_interval = pulse_interval
        self.clock: dict[CLOCK, Clock] = clock_dict
        self.position: dict[str, float] = position

    def pulse(self, clock_pulses: list[int] | None = None) -> None:
        """
        Handles both slow and fast cases using the max of "Clock.slow" and 0. Fast is < 0.
        """
        if clock_pulses is None:
            c1_slow = max(0, self.clock[ONE].slow)
            c2_slow = max(0, self.clock[TWO].slow)
            clock_pulses = Pulses(c1_slow, c2_slow)
        try:
            while clock_pulses != [0, 0]:
                if (clock_pulses.one > 0) and (clock_pulses.two > 0):
                    self.clock[ONE].pulse()
                    self.clock[TWO].pulse()
                    clock_pulses.one -= 1
                    clock_pulses.two -= 1

                elif clock_pulses.two == 0:
                    self.clock[ONE].pulse()
                    clock_pulses.one -= 1

                elif clock_pulses.one == 0:
                    self.clock[TWO].pulse()
                    clock_pulses.two -= 1

                time.sleep(self.pulse_interval)
        except Exception as err:
            logger.exception(err)

    def check_if_night(self, tm: float) -> None:
        """
        Todo: change from int to dict of the time of day list.
        """
        if self.is_night:
            self
