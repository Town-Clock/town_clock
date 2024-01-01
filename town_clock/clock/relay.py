"""
relay.py

todo: better error handling
"""
from __future__ import annotations
from enum import Enum
import time
from typing import Self
from town_clock.settings import RELAY_PULSE_DELAY

from town_clock.util import Mode, CLOCK
from town_clock.util.clock_exceptions import PulseError
from town_clock.util.utils import get_mode_from_env


class RelayState(Enum):
    """Relay State"""

    ON = 1
    OFF = 0


class Relay:
    """
    Class for relay.
    """

    def __init__(self, pin: int, name: str) -> None:
        """
        Initialize a Relay object.

        Args:
            pin (int): The pin number to which the relay is connected.
            name (str): The name of the relay.
            mode (Mode, optional): The mode of the relay. Defaults to Mode.TEST.
        """
        self.state: RelayState = RelayState.OFF
        self.mode = get_mode_from_env()
        self.pin = pin
        self.name = name

    @property
    def is_on(self) -> bool:
        """
        Check if the relay is currently turned on.

        Returns:
            bool: True if the relay is on, False otherwise.
        """
        return self.state == RelayState.ON

    def turn_on(self) -> None:
        """
        Turns on the relay.

        This method sets the state of the relay to 'ON'.

        Todo:
            - Control the relay using the GPIO library.
        """
        self.state = RelayState.ON

    def turn_off(self) -> None:
        """
        Turns off the relay.

        This method sets the state of the relay to OFF.

        Todo:
            - Control the relay using the GPIO library.
        """
        self.state = RelayState.OFF


class ClockRelay(Relay):
    """Clock Relay Class"""

    def __init__(self, clock: CLOCK, common_pin: int, pin: int, name: str) -> None:
        super().__init__(pin, name)
        self.common_pin = common_pin
        self.clock: CLOCK = clock

    def pulse(self) -> Self:
        """
        Pulse the relay by turning it on for a short duration and then turning it off.

        Returns:
            Self: The current instance of the Relay class.

        Raises:
            PulseError: If the pulse operation fails.
        """
        try:
            self.turn_on()
            time.sleep(RELAY_PULSE_DELAY)
            self.turn_off()
            return self
        except Exception:
            raise PulseError(False, f"Failed to pulse: {self.name}")


class LEDRelay(Relay):
    """LED Relay"""
