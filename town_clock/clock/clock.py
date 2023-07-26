"""
clock.py

"""
from __future__ import annotations

import time
from dataclasses import dataclass, field
from typing import Protocol

from loguru import logger

from town_clock.util import CLOCK, clock_logging


# Constants
twelve_hours = 720


class ClockRelay(Protocol):
    """Clock Relay Protocol"""

    def turn_on(self):
        ...
    
    def turn_off(self):
        ...

class CommonRelay(ClockRelay, Protocol):
    """Common Relay Protocol"""
    ...


@dataclass
class Clock:
    """
    Class Clock

    Parameters:
        name (CLOCK): The name of the clock in enum form.
        clock_relay (ClockRelay): The relay that this Clock controls.
        clock_relay (ClockRelay): The relay that this Clock controls.
        clock_relay (ClockRelay): The relay that this Clock controls.
        time_on_clock (int): minutes past 12 AM/PM (0-719)
        slow (int): Minutes slow, fast is negative.
        cutoff (int): Value is used to work out how long the
                      clock will sleep for. Default is 30.
    """
    name: CLOCK
    clock_relay: ClockRelay
    common_relay: CommonRelay
    other_clock_relay: ClockRelay
    time_on_clock: int 
    slow: int = field(default=0)
    cutoff: int = field(default=30)
    sleep_time: float = field(default=0.5)

  
    def compare(self, clock_time: int) -> Clock:
        """
        Compares the time on the clock with the given time and
        works out how slow or fast it is.
        
        Slow is positive.

        The 'self.cutoff' value is used to work out
        how long the clock will sleep for.

        Args:
            clock_time: int: Time.clock_time, minutes after 12 AM/PM.

        Returns:
            self
        """

        difference: int = clock_time - self.time_on_clock
        
        # 1. Ensure that the difference is less than 12 hours in either direction.
        while difference >= twelve_hours:
            logger.error(f"Clock {self.name.name} Difference: {difference}")
            difference -= twelve_hours
        while difference <= -twelve_hours:
            logger.error(f"Clock {self.name.name} Difference: {difference}")
            difference += twelve_hours
        
        # 2. Make the difference positive. Pulse multi-hour rather than wait.
        if difference < 0:
            difference += twelve_hours

        # 3. Check if the difference is smaller than the cutoff. If so, let the clock sleep.
        if (twelve_hours - self.cutoff) <= difference < twelve_hours:
            difference -= twelve_hours

        # 4. If the difference is equal to twelve hours, set it to 0. 
        if difference == twelve_hours:
            difference = 0

        # Finally set self.slow to the difference then return self.
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
            # self.clock_relay.pulse() # Todo: Add pulse logic here.
            self.slow -= 1
            if num_pulses > 1:
                time.sleep(self.sleep_time)
            else:
                break
        return self
