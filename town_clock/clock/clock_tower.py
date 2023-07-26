"""
ClockTower module.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from time import sleep
from typing import Protocol
from loguru import logger

from town_clock.clock import Clock, Time
from town_clock.util import CLOCK, Mode, clock_logging
from town_clock.util.clock_exceptions import PulseError
from town_clock.clock.pulses import Pulses

ONE = CLOCK.ONE
TWO = CLOCK.TWO
file_name = clock_logging.pulse_handler_file


class Relay(Protocol):
    """
    Relay Protocol
    """
    
    lights_on: bool

    def turn_on(self) -> Relay:
        ...

    def turn_off(self) -> Relay:
        ...


@dataclass(slots=True)
class ClockTower:
    """
    Controls the flow of information between the ui and the clocks.

    Parameters:
        running (bool): If the system is on.
        time (Time): The time logic.
        mode (Mode): Mode that the system is in.
        led (LEDRelay): Clock Lights.
        clock (dict[CLOCK, Clock]): Clock Face.
        position (dict[str, float]):
        pulse_interval (float): Interval between pulses in seconds. Default is 0.5.

    """

    running: bool
    time: Time
    mode: Mode
    led: Relay
    clock: dict[CLOCK, Clock]
    position: dict[str, float]
    pulse_interval: float = field(default=0.5)

    def __post_init__(self):
        clock_times = self.get_time_from_file()
        for clock in self.clock.values():
            clock.time_on_clock = clock_times[clock.name.value - 1]
        logger.log('INFO', self.print_clocks())
    
    def print_clocks(self) -> str:
        return f'Clock 1: {self.clock[ONE].time_on_clock}, Clock 2: {self.clock[TWO].time_on_clock}'
        
    def get_time_from_file(self) -> list[int]:
        clock_time = self.time.clock_time
        ret_tm: list[int] = [clock_time, clock_time]
        
        try: 
            with open(file_name, "r") as f:
                last_lines = f.readlines()[-3:]
        except FileNotFoundError:
            with open(file_name, "w"):
                ...
            return ret_tm
                
        for line in last_lines[::-1]:
            try:
                ret_tm = [int(time) for time in line.split(',')[3:5]]
                break
            except KeyError:
                continue
        return ret_tm

    @property
    def slow(self) -> Pulses:
        """
        How many minutes slow is the clock? If the clock is fast that clock
        will return 0.

        Returns:
            Pulses: How many pulses required to bring the clock back to
                    current time.
        """
        return Pulses(
            one=self.clock[ONE].slow,
            two=self.clock[TWO].slow
            )

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
                        False,
                        f"Pulse count exceeded limit: {count}, {clock_pulses}",
                    )
        except Exception as err:
            logger.exception(err)

    @property
    def is_night(self) -> bool:
        """
        Is it Night time.

        Returns:
            bool: True if nighttime.
        """
        return self.time.is_night

    def run(self):
        while self.running:
            if self.time():
                # Todo: Add in compare.
                self.pulse_clocks()
                self.led.lights_on = self.is_night

if __name__ == '__main__':
    ...
    # tower = ClockTower(
    #     True,
    #     Time(),
    #     Mode.DEV,
    #     {
    #         ONE: Clock(ONE, ClockRelay(), ClockRelay(), ClockRelay(),0),
    #         TWO: Clock(TWO, ClockRelay(), ClockRelay(), ClockRelay(),0)
    #     },
    #     position
    # )
