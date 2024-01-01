"""
ClockTower module.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from time import sleep
from typing import Protocol
from loguru import logger
from requests import get

from town_clock.clock import Clock, Time, Pulses
from town_clock.util import CLOCK, Mode, get_mode_from_env
from town_clock.util.clock_exceptions import PulseError

ONE = CLOCK.ONE
TWO = CLOCK.TWO


class LEDRelay(Protocol):
    """
    LED Relay Protocol
    :NoIndex:
    """

    def turn_on(self) -> LEDRelay:
        ...

    def turn_off(self) -> LEDRelay:
        ...


@dataclass(slots=True)
class Tower:
    """
    Controls the flow of information between the ui and the clocks.

    Parameters:
        running (bool):
        time (Time):
        mode (Mode):
        led (LEDRelay):
        clock (dict[CLOCK, Clock]):
        position (dict[str, float]):
        pulse_interval (float): Default is 0.5.

    """

    running: bool
    time: Time
    led: LEDRelay
    clock: dict[CLOCK, Clock]
    position: dict[str, float]=field(default=)
    mode: Mode = field(default=get_mode_from_env())
    pulse_interval: float = field(default=0.5)

    @property
    def slow(self) -> Pulses:
        """
        How many minutes slow is the clock? If the clock is fast that clock
        will return 0.

        Returns:
            Pulses: How many pulses required to bring the clock back to
                    current time.
        """
        return Pulses(*(clock.slow for clock in self.clock.values()))

    @property
    def is_night(self) -> bool:
        """
        Is it Night time.

        Returns:
            bool: True if nighttime.
        """
        return NotImplemented

    def pulse_clocks(self) -> None:
        """
        Pulse the clocks using the Pulse class.

        Raises:
            PulseError: When count goes beyond the max limit
                        (self.slow.one + 1) * (self.slow.two + 1).

        Todo:
            Work on exception handling.
        """
        count = 0
        max_count = (self.slow.one + 1) * (self.slow.two + 1)
        try:
            while (clock_pulses := self.slow) != [0, 0]:
                if (clock_pulses.one > 0) and (clock_pulses.two > 0):
                    self.clock[ONE].pulse()
                    self.clock[TWO].pulse()

                elif clock_pulses.two == 0:
                    self.clock[ONE].pulse(clock_pulses.one)

                elif clock_pulses.one == 0:
                    self.clock[TWO].pulse(clock_pulses.two)

                sleep(self.pulse_interval)
                count += 1
                if count > max_count:
                    raise PulseError(
                        f"Pulse count exceeded limit: {count}, {clock_pulses}"
                    )
        except Exception as err:
            logger.exception(err)

    def run(self):
        while self.running:
            raise NotImplementedError

    def check_if_night(self) -> None:
        """
        Todo:
            change from int to dict of the time of day list.
        """
        if self.time.is_night():
            raise NotImplementedError
