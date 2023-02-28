from __future__ import annotations
from enum import Enum
from typing import Any, Literal, Optional


class Log_Level(Enum):
    """Log Levels:
    CRITICAL: 50
    EXCEPTION = 40
    ERROR: 40
    WARNING: 30
    INFO: 20
    DEBUG: 10
    NOTSET: 0
    """

    CRITICAL = 50
    PULSE = 45
    ERROR = 40
    EXCEPTION = 40
    WARNING = 30
    SUCCESS = 25
    INFO = 20
    DEBUG = 10
    NOTSET = 0


class Mode(Enum):
    """Either Test or Active\n
    DEV = 'dev'
    TEST = 'test'
    ACTIVE = 'active'
    """

    DEV = "dev"
    TEST = "test"
    ACTIVE = "active"


class CLOCK(Enum):
    """CLOCK Names
    A enum used for controlling and altering the clock times independently.
    todo: Use enum with objects..
    """

    ALL = 0
    ONE = 1
    TWO = 2

    @classmethod
    def values(cls) -> tuple[Literal[0], Literal[1], Literal[2]]:
        return 0, 1, 2


def convert_position_string_to_number(position_str: str) -> float:
    """
    Converts a position string to a number.

    args:
        position_str: str: Position in the form of a string. eg "30.3402W"
    """
    if isinstance(position_str, int | float):
        return position_str
    elif not isinstance(position_str, str):
        raise TypeError()
    pos_list = list(position_str)
    direction: int = int()
    match pos_list.pop().upper():
        case "N" | "E":
            direction = 1
        case "S" | "W":
            direction = -1
    return float("".join(pos_list)) * direction


class PositionError(Exception):
    """Error with the Position Object of any kind."""

    pass


class PositionValue:
    """
    PositionValues Descriptor

    Ensures that there is only one value stored and never changed.

    Parameters:
        name (str): Name of the value set in the instance.

    Raises:
        PositionError: If there is no attribute by that name or when it is
                       set, and it is assigned to again.
    """

    def __init__(self):
        self.name: str = ""
        self._name: str = ""

    def __set_name__(self, owner: object, name: str) -> None:
        self.name = name
        self._name = "_" + name

    def __get__(self, instance: object, owner: type[object]) -> Any:
        try:
            return getattr(instance, self._name)
        except AttributeError:
            raise PositionError(f"Position has no attribute: " f"{self.name}")

    def __set__(self, instance: object, value: Any) -> None:
        try:
            getattr(instance, self._name)
        except AttributeError:
            setattr(instance, self._name, value)
        else:
            error_str = f"Try to set {self.name} when it is already set."
            raise PositionError(error_str)


class Position:
    """
    Singleton Position

    Parameters:
        latitude (float): Degrees north from the equator in decimal degrees.
                          South is negative.
        longitude (float): Degrees east from the prime meridian in decimal
                           degrees. West is negative.
        altitude (float): Metres above mean sea level(MSL).
    """

    longitude: PositionValue = PositionValue()
    latitude: PositionValue = PositionValue()
    altitude: PositionValue = PositionValue()

    __current_position__: Optional[Position] = None

    def __new__(cls, *args, **kwargs):
        if not isinstance(cls.__current_position__, Position):
            cls.__current_position__ = super().__new__(cls)
        return cls.__current_position__

    def __init__(
        self,
        latitude: float = 0,
        longitude: float = 0,
        altitude: float = 0,
    ) -> None:
        self.latitude = latitude  # type: ignore
        self.longitude = longitude  # type: ignore
        self.altitude = altitude  # type: ignore

    def __repr__(self) -> str:
        return f"Position({self.latitude}, {self.longitude}, {self.altitude})"
