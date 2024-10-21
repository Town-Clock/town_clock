"""
pulses_test.py



Author: Zack Hankin
Started: 21/02/2023
"""

from __future__ import annotations
import pytest
from town_clock.clock import Pulses


@pytest.mark.parametrize(
    "pulses, expected", (((), (0, 0)), ((1, 1), (1, 1)), ((-10, -10), (0, 0)))
)
def test_Pulse_Class(pulses, expected):
    assert Pulses(*pulses) == expected


@pytest.mark.parametrize(
    "pulses, adder, expected",
    (
        ((), 0, (0, 0)),
        ((1, 1), 0, (1, 1)),
        ((-10, -10), 5, (5, 5)),
        ((10, 10), -3, (7, 7)),
        ((2, 2), -10, (0, 0)),
    ),
)
def test_Pulse_Class_addition(pulses, adder, expected):
    pulses = Pulses(*pulses)
    pulses.one += adder
    pulses.two += adder
    assert pulses == expected
