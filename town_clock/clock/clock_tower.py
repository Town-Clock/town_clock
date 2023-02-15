"""
ClockTower module.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from time import sleep
from typing import Protocol, Sequence

from loguru import logger

from town_clock.clock import Clock, Time
from town_clock.util import CLOCK, Mode

ONE = CLOCK.ONE
TWO = CLOCK.TWO


@dataclass(slots=True)
class Pulses:
    """Object to control the Pulse amount"""

    __one: int
    __two: int

    def __post_init__(self):
        self.one = self.__one
        self.two = self.__two

    @property
    def one(self) -> int:
        """
        Pulses needed for clock one.

        Returns:
            Number of pulses required for clock one.
        """
        return self.__one

    @one.setter
    def one(self, value):
        self.__one = value if value > 0 else 0

    @property
    def two(self):
        """
        Pulses needed for clock two.

        Returns:
            Number of pulses required for clock two.
        """
        return self.__two

    @two.setter
    def two(self, value):
        self.__two = value if value > 0 else 0

    def __eq__(self, o: object) -> bool:
        if isinstance(o, Pulses):
            return self == o
        elif isinstance(o, Sequence):
            return (self.one == o[0]) and (self.two == o[1])
        else:
            raise TypeError("Other not Pulses or a sequence for equality.")

    def __repr__(self):
        return f"Pulses({self.one, self.two})"


class LEDRelay(Protocol):
    """LED Relay Protocol"""

    def turn_on(self) -> LEDRelay:
        ...

    def turn_off(self) -> LEDRelay:
        ...


@dataclass(slots=True)
class ClockTower:
    """
    Controls the flow of information between the ui and the clocks.
    """

    running: bool
    time: Time
    mode: Mode
    led: LEDRelay
    clock: dict[CLOCK, Clock]
    position: dict[str, float]
    pulse_interval: float = field(default=0.5)

    @property
    def slow(self):
        return Pulses(*(clock.slow for clock in self.clock.values()))

    @property
    def is_night(self):
        return NotImplemented

    def pulse(self) -> None:
        """
        Handles both slow and fast cases using the max of "Clock.slow"
        and 0. Fast is < 0.
        """
        count = 0
        try:
            while (clock_pulses := self.slow) != [0, 0] or count > 60:
    if (clock_pulses.one > 0) and (clock_pulses.two > 0):
        self.clock[ONE].pulse()
        self.clock[TWO].pulse()

    elif clock_pulses.two == 0:
        self.clock[ONE].pulse(clock_pulses.one)

    elif clock_pulses.one == 0:
        self.clock[TWO].pulse(clock_pulses.two)

    sleep(self.pulse_interval)
    count += 1
        except Exception as err:
            logger.exception(err)

    def run(self):
        while self.running:
            raise NotImplementedError

    def check_if_night(self) -> None:
        """
        Todo: change from int to dict of the time of day list.
        """
        if self.time.is_night():
            raise NotImplementedError
