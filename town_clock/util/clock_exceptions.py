"""
exceptions.py



Author: Zack Hankin
Started: 10/02/2023
"""
from __future__ import annotations

from loguru import logger


class BaseClockException(Exception):
    def __init__(self, *args) -> None:
        super().__init__(*args)
        logger.error(repr(self))


class ClockGroupError(ExceptionGroup):
    def __init__(self, *args) -> None:
        super().__init__(*args)
        logger.error(repr(self))


class PulseError(BaseClockException):
    def __init__(self, pulse=False, *args):
        logger.error(f"Pulsed: {pulse}")
        super().__init__(*args)

    def __repr__(self) -> str:
        message: str = type(self).__name__
        if self.args:
            message += ": "
            message += f"{self.args[0]}"
            try:
                for arg in self.args[1:]:
                    message += ", "
                    message += arg
            except IndexError:
                ...
        return message

    def __str__(self) -> str:
        return repr(self)


class NoValidTimeFromFileError(BaseClockException):
    ...

class ButtonError(BaseClockException):
    ...