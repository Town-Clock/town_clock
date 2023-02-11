"""
clock.py

"""
from __future__ import annotations
import time
import datetime
from dataclasses import dataclass, field
from typing import NoReturn, Protocol

from loguru import logger

from town_clock.util import CLOCK


class ClockRelay(Protocol):
    """Relay Protocol"""

    def pulse(self):
        """pulse method"""
        ...


def to_from_iso_format(time_stamp: float) -> datetime.datetime:
    """
    This function gets around daylight savings issue.

    Args:
        time_stamp: float: seconds since epoch.

    Returns:
        datetime.datetime
    """
    it = time.strftime("%Y-%m-%dT%H:%M:%S", time.localtime(time_stamp))
    return datetime.datetime.fromisoformat(it)


@dataclass
class Clock:
    """
    Class Clock

    params:
        name: CLOCK
        time_on_clock: int: seconds since epoch.
        slow: int: Minutes slow, fast is negative.
    """

    name: CLOCK
    relay: ClockRelay
    time_on_clock: int
    pulse_frequency: int = 60
    slow: int = field(default=0)

    def compare(self, other) -> NoReturn:
        """todo: Sets the slow parameter"""
        ...

    @property
    def mod_time(self) -> int:
        """
        Mods the seconds to minutes when storing the time.
        """
        return self.time_on_clock

    @mod_time.setter
    def mod_time(self, value):
        self.time_on_clock = self.mod_freq(value, self.pulse_frequency)

    @staticmethod
    def mod_freq(tm: float | int, freq: float = 60) -> float | int:
        """
        Mod Time to show clean minutes

        Args:
            tm (float): Input time in seconds.
            freq (float, optional): Frequency of pulses. Defaults to 0.

        Raises:
            ValueError: When a given variable is not a number.
            ValueError: When freq is less than 0.

        Returns:
            float: Seconds rounded to the nearest minute. Unless freq is set.
        """
        if type(tm) not in (float, int):
            raise TypeError("Not a Number.")

        if freq <= 0:
            logger.error("Freq must be greater than 0")
            raise ValueError("Freq must be greater that 0.")
        tm_mod = tm % freq

        if tm_mod >= freq / 2:
            return tm + (freq - tm_mod)
        else:
            return tm - tm_mod

    def pulse(self, num_pulses: int = 1) -> Clock:
        """Pulse the clock"""
        for _ in range(num_pulses):
            self.relay.pulse()
            self.slow -= 1
            if num_pulses > 1:
                time.sleep(0.5)
        return self
