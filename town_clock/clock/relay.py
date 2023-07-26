"""
relay.py

todo: better error handling
"""
from __future__ import annotations

from town_clock.util import Mode, CLOCK
from loguru import logger


class Relay:
    """
    Class for relay.
    """

    def __init__(self, pin: int, name: str, pulse_length = 0.2, mode: Mode = Mode.DEV) -> None:
        self.is_on: bool = False
        self.mode: Mode = mode
        self.name: str = name
        self.pin: int = pin
        self.pulse_length: float = pulse_length
        # if self.mode != Mode.ACTIVE:
        #     import ...

    def turn_on(self) -> None:
        self.is_on = True
        ...

    def turn_off(self) -> None:
        self.is_on = False
        ...
    

class CommonRelay(Relay):
    common_relay = None
    
    def __new__(cls, *args, **kwargs):
        if cls.common_relay == None:
            cls.common_relay = super().__new__(cls)
        return cls.common_relay
    
    def __init__(
        self, 
        pin: int, 
        name: str = 'Common Relay', 
        pulse_length=0.2, 
        mode: Mode = Mode.DEV
        ) -> None:
        
        super().__init__(pin, name, pulse_length, mode)


class ClockRelay(Relay):
    """Clock Relay Class"""

    def __init__(
        self, 
        pin: int, 
        name: str,
        clock: CLOCK,
        pulse_length = 0.2,
        mode: Mode = Mode.DEV,
        ) -> None:
        """
        Init Clock Relay

        args:
            common_pin: int
            clock: CLOCK
            pin: int
            name: str
            mode: Mode = Mode.DEV
        """
        super().__init__(pin, name, pulse_length, mode)
        self.clock: CLOCK = clock
        self.direction = 0

  

class LEDRelay(Relay):
    """LED Relay"""

    def __init__(self, pin: int, name: str, pulse_length=0.2, mode: Mode = Mode.DEV) -> None:
        super().__init__(pin, name, pulse_length, mode)
    
    @property
    def lights_on(self) -> bool:
        return self.is_on
    
    @lights_on.setter
    def lights_on(self, is_night) -> None:
        is_on = self.is_on
        if is_night & (not is_on):
            self.turn_on()
            logger.log('INFO', 'Lights on')
        elif not is_night & is_on:
            self.turn_off
            logger.log('INFO', 'Lights off')
            
