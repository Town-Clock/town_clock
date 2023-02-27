"""
Pulses Class and functionality.

Author: Zack Hankin
Started: 20/02/2023
"""
from __future__ import annotations
from typing import Sequence


class GreaterThanZero:
    """Class descriptor that ensures the value is greater zero."""

    __slots__ = ["name"]

    def __init__(self) -> None:
        self.name: str = ""

    def __set_name__(self, owner, name):
        self.name = f"_{name}"

    def __get__(self, instance, owner=None) -> int:
        ret_value: int = getattr(instance, self.name)
        if isinstance(ret_value, int | float):
            return max(0, ret_value)
        elif ret_value is None:
            return 0
        else:
            return NotImplemented

    def __set__(self, instance, value) -> None:
        if value is None:
            value = 0
        value = max(value, 0)
        setattr(instance, self.name, value)


class Pulses:
    """Object to control the Pulse amount"""

    __slots__ = ["_one", "_two"]

    one = GreaterThanZero()
    two = GreaterThanZero()

    def __init__(self, one: int = 0, two: int = 0) -> None:
        self.one = one
        self.two = two

    def __eq__(self, o: object) -> bool:
        """
        Pulses equality works with both Pulses or Sequences.

        Args:
            o (Pulses | Sequence): Pulses or Sequence to compare.

        Returns:
            bool: True if equal.
        """
        if isinstance(o, Pulses):
            return self == o
        elif isinstance(o, Sequence):
            return (self.one == o[0]) and (self.two == o[1])
        else:
            return NotImplemented

    def __repr__(self) -> str:
        return f"Pulses({self.one}, {self.two})"
