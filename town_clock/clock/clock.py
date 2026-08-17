"""
clock.py

"""

from __future__ import annotations

import time
from dataclasses import dataclass, field
from typing import Protocol

from loguru import logger

from town_clock.util import CLOCK


class ClockRelay(Protocol):
    """Relay Protocol"""

    def pulse(self):
        """pulse method"""
        ...


@dataclass
class Clock:
    """
    Class Clock

    Parameters:
        name (CLOCK): The name of the clock in enum form.
        relay (ClockRelay): The relay that this Clock controls.
        time_on_clock (int): minutes past 12 AM/PM (0-719)
        slow (int): Minutes slow, fast is negative.
        cutoff (int): Value is used to work out how long the
                      clock will sleep for. Default is 30.
    """

    name: CLOCK
    relay: ClockRelay
    time_on_clock: int
    slow: int = field(default=0)
    cutoff: int = field(default=30)
    sleep_time: float = field(default=0.5)

    def compare(self, clock_time: int) -> Clock:
        """
        Compares the time on the clock with the given time and
        works out how slow or fast it is.

        The 'self.cutoff' value is used to work out
        how long the clock will sleep for.

        Args:
            clock_time: int: Time.clock_time, minutes after 12 AM/PM.

        Returns:
            self
        """

        difference: int = clock_time - self.time_on_clock

        while difference >= 720:
            logger.error(f"Clock {self.name.name} Difference: {difference}")
            difference -= 720
        while difference <= -720:
            logger.error(f"Clock {self.name.name} Difference: {difference}")
            difference += 720

        if difference < 0:  # Difference is negative.
            difference += 720

        if (720 - self.cutoff) <= difference < 720:
            difference -= 720

        if difference == 720:
            difference = 0

        self.slow = difference
        return self

    def pulse(self, num_pulses: int = 1) -> Clock:
        """Pulse the clock"""
        if not isinstance(num_pulses, int):
            raise TypeError(
                f"Clock pulse args must be of type int, got: "
                f"{type(num_pulses).__name__}"
            )
        for _ in range(int(num_pulses)):
            self.relay.pulse()
            self.slow -= 1
            if num_pulses > 1:
                time.sleep(self.sleep_time)
        return self
