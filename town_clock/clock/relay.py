"""
relay.py

todo: better error handling
"""
import time

from town_clock.util import Mode, CLOCK
from town_clock.util.clock_exceptions import PulseError


class Relay:
    """
    Class for relay.
    todo:
        remember to order of pulses. Alternating between common and clock pin.
    """

    def __init__(self, pin: int, name: str, mode: Mode = Mode.TEST) -> None:
        self.is_on: bool = False
        self.mode = mode
        self.pin = pin
        self.name = name

    def turn_on(self) -> None:
        self.is_on = True

    def turn_off(self) -> None:
        self.is_on = False


class ClockRelay(Relay):
    """Clock Relay Class"""

    def __init__(self, common_pin: int, clock: CLOCK, *args, **kwargs) -> None:
        """
        Init Clock Relay

        args:
            common_pin: int
            clock: CLOCK
            pin: int
            name: str
            mode: Mode = Mode.TEST
        """
        self.common_pin = common_pin
        self.clock: CLOCK = clock
        super().__init__(*args, **kwargs)

    def pulse(self) -> bool:
        """
        Pulse the relay.
        """
        try:
            self.turn_on()
            time.sleep(0.1)
            self.turn_off()
            return True
        except Exception:
            raise PulseError(False, f"Failed to pulse: {self.name}")


class LEDRelay(Relay):
    """LED Relay"""

    ...
