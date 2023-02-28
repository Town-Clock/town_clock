"""
Calculates sun position.
"""
import time
from datetime import datetime, timedelta
from enum import Enum
from typing import Any, Sequence

import skyfield.timelib
from pytz import timezone
from pytz.tzinfo import DstTzInfo, StaticTzInfo
from skyfield import almanac
from skyfield.api import load, Loader, wgs84
from timezonefinder import TimezoneFinder

from .utils import Position


class TimeOfDay(Enum):
    """
    Enum of time of day.

    Enums:
        LASTLIGHT (int): 0
        FIRSTLIGHT (int): 1
        SUNRISE (int): 2
        SUNSET (int): 3
    """

    FIRSTLIGHT = 1
    SUNRISE = 2
    SUNSET = 3
    LASTLIGHT = 0


def timezone_finder(
    latitude: float,
    longitude: float,
) -> StaticTzInfo | DstTzInfo:
    """
    Gets the correct timezone for the given location.

    Args:
        latitude (float): Degrees north from the equator in decimal degrees.
                          South is negative.
        longitude (float): Degrees east from the prime meridian in decimal
                           degrees. West is negative.

    Returns:
        Timezone: Return a datetime.tzinfo implementation for the given
                  timezone from pytz.
    """
    tf = TimezoneFinder()
    tz_str: str = tf.timezone_at(lng=longitude, lat=latitude)
    return timezone(tz_str)


def find_sunrise_sunset_times(position: Position) -> dict[TimeOfDay, float]:
    """
    Generates a dictionary mapping representing the Enum value and
    time of that occurrences.

    Args:
        position (Position): Position of the clock.

    Returns:
        dict[TimeOfDay, float]: TimeOfDay Enum and the time of that
                                occurrence.
    """
    # Setting up Times
    latitude = position.latitude
    longitude = position.longitude
    altitude = position.altitude
    zone = timezone_finder(latitude, longitude)
    now = zone.localize(datetime.now())
    # midnight: Any = now.replace(hour=0, minute=0, second=0, microsecond=0)
    midday: Any = now.replace(hour=12, minute=0, second=0, microsecond=0)
    next_midday: Any = midday + timedelta(days=1)
    ts = load.timescale()
    t0 = ts.from_datetime(midday)
    t1 = ts.from_datetime(next_midday)

    # Setting up Position and Function
    eph: Loader = load("de421.bsp")
    position_skyfield = wgs84.latlon(
        latitude_degrees=latitude,
        longitude_degrees=longitude,
        elevation_m=altitude,
    )
    f = almanac.dark_twilight_day(eph, position_skyfield)
    times, events = almanac.find_discrete(t0, t1, f)

    return _create_return_dict(events, times, zone)


def _create_return_dict(
    events: Sequence[int],
    times: Sequence[skyfield.timelib.Time],
    zone: StaticTzInfo | DstTzInfo,
) -> dict[TimeOfDay, float]:
    """
    Creates the return dict for find_sunrise_sunset_times.

    Args:
        events (Sequence[int]): A sequence of event represented by integers.
        times (Sequence[float]): A sequence of time values.
        zone (StaticTzInfo | DstTzInfo): The time zone.

    Returns:
        dict[TimeOfDay, float]: TimeOfDay Enum and the time of that
                                occurrence.
    """
    sunset_sunrise_times = {}
    idx: TimeOfDay = TimeOfDay.SUNRISE
    for the_time, event in zip(times, events):
        struct_time = the_time.astimezone(zone).timetuple()
        match event:
            case 0:
                continue
            case 1:
                continue
            case 2:  # Last light
                if 12 <= struct_time.tm_hour < 24:
                    idx = TimeOfDay.LASTLIGHT
                else:
                    continue
            case 3:  # First Light | Sunset
                idx = (
                    TimeOfDay.SUNSET
                    if 12 <= struct_time.tm_hour < 24
                    else TimeOfDay.FIRSTLIGHT
                )
            case 4:  # Sunrise
                idx = TimeOfDay.SUNRISE
        sunset_sunrise_times[idx] = time.mktime(struct_time)
    return sunset_sunrise_times
