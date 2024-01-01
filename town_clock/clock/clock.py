"""
clock.py

"""
from __future__ import annotations

import time
from dataclasses import dataclass, field
from typing import Protocol, Self

from loguru import logger
from town_clock.settings import CLOCK_CUTOFF, CLOCK_SLEEP_TIME

from town_clock.util import CLOCK
from town_clock.util.constants import HOURS


class ClockRelay(Protocol):
    """Relay Protocol"""

    def pulse(self) -> Self:
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
        cutoff (int): The maximum amount of minutes the
            clock will sleep for. Default is 30.
    """

    name: CLOCK
    relay: ClockRelay
    time_on_clock: int
    slow: int = field(default=0)
    cutoff: int = field(default=CLOCK_CUTOFF)
    sleep_time: float = field(default=CLOCK_SLEEP_TIME)

    def compare(self, clock_time: int) -> Self:
        """
        Compares the current clock time with the given clock time and calculates the difference.

        Args:
            clock_time (int): The clock time to compare with.

        Returns:
            Self: The updated clock object with the calculated difference.
        """

        difference: int = clock_time - self.time_on_clock

        while difference >= HOURS[12]:
            logger.error(f"Clock {self.name.name} Difference: {difference}")
            difference -= HOURS[12]
        while difference <= -HOURS[12]:
            logger.error(f"Clock {self.name.name} Difference: {difference}")
            difference += HOURS[12]

        # Makes sure the difference is positive.
        if difference < 0:
            difference += HOURS[12]

        # If the difference is greater than the cutoff value
        if (HOURS[12] - self.cutoff) <= difference < HOURS[12]:
            difference -= HOURS[12]

        # If the difference is a modulus of 12 hours the diffence is 0.
        if (difference % HOURS[12]) == 0:
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

        for pulse in range(num_pulses):
            self.relay.pulse()
            self.slow -= 1
            if (num_pulses - (pulse + 1)) > 0:
                time.sleep(self.sleep_time)
        return self
