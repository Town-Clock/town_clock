from datetime import  datetime

class TimezoneFinder:
    def timezone_at(self, *, lng: float, lat: float) -> str: ...

def timezone_finder(
    latitude: float, longitude: float
) -> _UTCclass | StaticTzInfo | DstTzInfo: ...
def find_sunrise_sunset_times(
    latitude: float, longitude: float, altitude: float
) -> dict[int, float]: ...

class TzInfo:
    def localize(self, dt: datetime) -> datetime: ...
    def replace(self, hour, minute, second, microsecond) -> datetime: ...

class _UTCclass(TzInfo): ...
class StaticTzInfo(TzInfo): ...
class DstTzInfo(TzInfo): ...
