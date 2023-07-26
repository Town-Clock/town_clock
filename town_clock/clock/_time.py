"""
_time.py

Time logic.

Author: Zack Hankin
Started: 12/02/2023
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

import pendulum
from loguru import logger
from pendulum.datetime import DateTime
from pendulum.tz.timezone import Timezone

from town_clock.util import location_sunrise_sunset as lss
from town_clock.util import clock_logging
from pathlib import Path

file_name = clock_logging.pulse_handler_file

@dataclass
class Time:
    """
    Controls the time logic.
    
    now: pendulum.DateTime:
    clock_time: int: minutes from 12 AM/PM
    timezone: Timezone | str: Timezone of the clock. Default is "Australia/Sydney".
    """

    position: dict[str, float] = field(default_factory=dict)
    now: DateTime = field(default=pendulum.from_timestamp(0))
    clock_time: int = field(default=-1)
    timezone: Timezone | str = field(default="Australia/Sydney")
    prev_sunrise: float = field(default=-1)
    sunset: float = field(default=-1)
    next_sunrise: float = field(default=-1)

    def __post_init__(self):
        """
        todo: Get time from file here or in Clock

        Returns:

        """
        if self.now == pendulum.from_timestamp(0):
            self.now = self.get_time_from_file()
        self.set_clock_time(self.now)

        logger.info(f"Time Object initialised at {self.now}.")
        logger.debug(f"Timezone: {self.timezone}")

    def __iter__(self):
        """WHY??
        
        TODO: Remove if unnessary. 

        Returns:
            NotImplemented: Not Implemented
        """
        return NotImplementedError

    def get_time_from_file(self) -> DateTime:
        ret_dt = pendulum.now()
        try: 
            with open(file_name, "r") as f:
                last_lines = f.readlines()[-3:]
        except FileNotFoundError:
            with open(file_name, "w"):
                ...
            return ret_dt
                
        for line in last_lines[::-1]:
            try:
                line_list = line.split(',')
                self.clock_time = int(line_list[2])
                break
            except KeyError:
                continue
        return ret_dt
        

    def set_clock_time(self, tm: int | DateTime) -> Time:
        """
        Converts from time | DateTime to minutes since 12 AM/PM
        and sets clock_time.
        Always rounds down to the nearest minute.

        Args:
            tm: int | DateTime: seconds since epoch or valid DateTime.

        Returns:
            self
        """
        dt: DateTime
        if isinstance(tm, int):
            dt = pendulum.from_timestamp(tm)
        elif isinstance(tm, DateTime):
            dt = tm
        else:
            raise TypeError(f"Must be of type int or DateTime. Recieved type: {type(tm)}")
        
        self.clock_time = (dt.hour % 12) * 60 + dt.minute

        return self

    def __call__(self, time: Optional[DateTime] = None) -> bool:
        """
        Check if the time is on the minute. If on the minute updates the clock_time. 
        If a time is passed in, it will set the clock_time to that time and returns true. 

        Returns:
            Bool: Returns True if on the minute.
        """
        changed_clock_time: bool = False
        
        if time is None:
            self.now = pendulum.now(self.timezone)
            if changed_clock_time := self.is_on_minute(self.now):
                self.set_clock_time(self.now)
            
        elif isinstance(time, DateTime):
            self.now = time
            self.set_clock_time(time)
            return True

        else:
            raise TypeError(f"Unexpected type for time: {type(time).__name__}")
        
        return changed_clock_time

    def is_on_minute(self, time: DateTime) -> bool:
        """
        Is the given time on the minute?

        Returns:
            bool: True if successful.
        """
        if 0 >= time.second < 1:
            return True
        else:
            return False

    def add_minute(self, minute: int = 1) -> Time:
        """Adds x minutes

        Todo: Why does this exist with self.now, should it be to clock_time? For testing?
        
        Args:
            minute (int, optional): Number of minutes to add. Defaults to 1.

        Returns:
            Time: self
        """
        self(self.now.add(minutes=minute))
        return self

    def set_sunrise_sunset(self) -> Time:
        """Sets the Sunrise and Sunset times.
        
        Sets:
            - prev_sunrise
            - sunset            
            - next_sunrise

        Returns:
            Time: self
        """
        times = lss.find_sunrise_sunset_times(**self.position)
        self.prev_sunrise = times[0]
        self.sunset = times[2]
        self.next_sunrise = times[3]
        return self

    @property
    def is_night(self) -> bool:
        """Is it nighttime?
        
        Returns:
            bool: True if nightime."""
        now = self.now.timestamp()
        
        if now < self.prev_sunrise or now > self.next_sunrise:
            self.set_sunrise_sunset()
        
        if self.sunset < now < self.next_sunrise:
            return True
        return False
        

    def log_time(self, lvl: int | str, msg: str): # -> str:
        logger.log(lvl, msg)

if __name__ == '__main__':
    position = { 'latitude': -33.86785,'longitude': 151.20732,'altitude': 0 }
    dt = pendulum.datetime(2023,7,27,6,26,tz="Australia/Sydney")
    t = Time(position)
    # t(dt)
    # print(Time(position).is_night)
    t.log_time('PULSE',f'{int(t.now.timestamp())},{t.clock_time},385,381')
    