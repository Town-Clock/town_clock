"""
Pulses Class and functionality.

Author: Zack Hankin
Started: 20/02/2023
"""
from __future__ import annotations
from typing import Self, Sequence

# from town_clock.util.number_to_names import number_to_name


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


# class SuperPulses:
#     """Object to control the Pulse amount"""

#     # __slots__ = ["keys"]

#     def __new__(cls, *args, **kwargs):
#         dict_ = {
#             str(number_to_name(idx + 1, "-", False, "")): int(x)
#             for idx, x in enumerate(args)
#         }

#         cls.__slots__ = ["_" + str(x) for x in dict_.keys()]
#         cls.__slots__ += [str(x) for x in dict_.keys()]

#         self = super().__new__(cls)

#         for key, value in dict_.items():
#             self.__setattr__(key, GreaterThanZero())
#         for key, value in dict_.items():
#             self.__setattr__(key, value)
#         # property(, "one")
#         # self.__dict__ = dict_
#         return self

#     def __init__(self, *args, **kwargs) -> None:
#         print("init: ", kwargs)

#     def __eq__(self, o: object) -> bool:
#         """
#         Pulses equality works with both Pulses or Sequences.

#         Args:
#             o (Pulses | Sequence): Pulses or Sequence to compare.

#         Returns:
#             bool: True if equal.
#         """
#         return NotImplemented

#     def __repr__(self) -> str:
#         return f"Pulses({', '.join([str(x) for x in self.__dict__.values()])})"


class Pulses:
    """Object to control the Pulse amount"""

    __slots__ = ["_one", "_two", "keys"]

    one: GreaterThanZero = GreaterThanZero()
    two: GreaterThanZero = GreaterThanZero()

    def __init__(self, one: int = 0, two: int = 0) -> None:
        self.keys = [x[1:] for x in self.__slots__ if x.startswith("_")]
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
