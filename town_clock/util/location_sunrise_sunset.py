"""
Calculates sun position.
"""
import time
from datetime import timedelta, datetime

from typing import Any
from pytz import timezone
from skyfield import almanac
from skyfield.api import wgs84, load, Loader
from timezonefinder import TimezoneFinder


def timezone_finder(latitude: float, longitude: float):
    tf = TimezoneFinder()
    tz = str(tf.timezone_at(lng=longitude, lat=latitude))
    return timezone(tz)


def find_sunrise_sunset_times(
    latitude: float, longitude: float, altitude: float
) -> dict[int, float]:
    # Setting up Times
    zone = timezone_finder(latitude, longitude)
    now = zone.localize(datetime.now())
    midnight: Any = now.replace(hour=0, minute=0, second=0, microsecond=0)
    midday: Any = now.replace(hour=12, minute=0, second=0, microsecond=0)
    next_midday: Any = midday + timedelta(days=1)
    ts = load.timescale()
    t0 = ts.from_datetime(midnight)
    t1 = ts.from_datetime(next_midday)

    # Setting up Position and Function
    eph = load("de421.bsp")
    position = wgs84.latlon(
        latitude_degrees=latitude,
        longitude_degrees=longitude,
        elevation_m=altitude,
    )
    f = almanac.dark_twilight_day(eph, position)
    times, events = almanac.find_discrete(t0, t1, f)

    # Running Function
    sunset_sunrise_times = {}
    idx: int = 0
    for t, e in zip(times, events):
        if e in [3, 4]:
            struct_time = t.astimezone(zone).timetuple()
            sunset_sunrise_times[idx] = time.mktime(struct_time)
            idx += 1

    return sunset_sunrise_times
