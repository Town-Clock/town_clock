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
from pendulum import DateTime
from pendulum.tz.timezone import Timezone

from town_clock.util import find_sunrise_sunset_times, TimeOfDay, Position


@dataclass
class Time:
    """
    Parameters:
        now (pendulum.DateTime):
        clock_time (int): minutes from 12 AM/PM
        timezone (Timezone | str): Timezone of the clock.
                                   Default is "Australia/Sydney".
    """

    now: DateTime = field(default=pendulum.from_timestamp(0))
    clock_time: int = field(default=-1)
    timezone: Optional[Timezone | str] = "Australia/Sydney"
    sun_events: dict[TimeOfDay, float] = field(default_factory=dict)
    position: Position = Position()

    def __post_init__(self):
        """
        todo: Get time from file here or in Clock

        Returns:

        """
        if self.now == pendulum.from_timestamp(0):
            self.now = self.get_time_from_file()
        else:
            self.set_clock_time(self.now)
        logger.info("Time Object initialised.")
        logger.debug(f"Timezone: {self.timezone}")

    def __iter__(self):
        return NotImplemented

    def get_time_from_file(self) -> DateTime:
        return NotImplemented

    def set_sun_events(self) -> Time:
        """
        Sets the upcomming last light, sunset, first light and sunrise.

        Returns:
            Time: self
        """
        self.sun_events = find_sunrise_sunset_times(self.position)
        return self

    def set_clock_time(self, tm: int | DateTime) -> Time:
        """
        Converts from time | DateTime to minutes since 12 AM/PM
        and sets clock_time.
        Always rounds down to the nearest minute.

        Args:
            tm (int): seconds since epoch.

        Returns:
            Time: self
        """
        dt: DateTime
        if isinstance(tm, int):
            dt = pendulum.from_timestamp(tm)
        elif isinstance(tm, DateTime):
            dt = tm
        else:
            raise TypeError("Must be int or DateTime")
        dt.subtract(seconds=dt.second, microseconds=dt.microsecond)
        clock_time: int
        if 12 <= dt.hour < 24:
            clock_time = (dt.hour - 12) * 60 + dt.minute
        elif 0 <= dt.hour < 12:
            clock_time = dt.hour * 60 + dt.minute
        elif dt.hour == 24:
            clock_time = dt.minute
        else:
            raise ValueError("dt.hour must be between 0 and 24")
        self.clock_time = clock_time
        return self

    def __call__(self, time: Optional[DateTime] = None) -> bool:
        """
        Sets now and sets clock_time if on the minute.

        Returns:
            Returns True if on the minute.
        """
        if time is None:
            self.now = pendulum.now(self.timezone)
        elif isinstance(time, DateTime):
            self.now = time
        else:
            raise TypeError(f"Unexpected type for time: {type(time).__name__}")
        if changed_time := self.is_on_minute(self.now):
            self.set_clock_time(self.now)
        elif time is not None:
            self.set_clock_time(self.now)
        return changed_time

    def is_on_minute(self, time: DateTime) -> bool:
        """
        Is the time on the minute?

        Returns:
            bool: True if successful.
        """
        if 0 >= time.second < 1:
            return True
        else:
            return False

    def add_minute(self, minute: int = 1) -> Time:
        self(self.now.add(minutes=minute))
        return self

    def is_night(self) -> bool:
        """Is it nighttime?"""
        raise NotImplementedError

    def log_time(self) -> str:
        raise NotImplementedError
