"""
test clock.py

"""
import pytest

from town_clock.clock import Clock
from town_clock.clock.clock import ClockRelay
from town_clock.util import CLOCK


# logger.remove(0)
# logger.add(sys.stdout, level="INFO")


class MockRelay:
    pulse_count = 0

    def pulse(self):
        self.pulse_count += 1


@pytest.fixture
def default_clock():
    return Clock(
        name=CLOCK.ONE,
        relay=MockRelay(),
        time_on_clock=0,
        cutoff=30,
        sleep_time=0.01,
    )


def test_clock_instantiation(default_clock):
    assert default_clock.relay.pulse_count == 0  # type: ignore
    assert isinstance(default_clock, Clock)


def test_clock_pulse(default_clock):
    default_clock.pulse()
    assert default_clock.relay.pulse_count == 1  # type: ignore
    default_clock.pulse(9)
    assert default_clock.relay.pulse_count == 10  # type: ignore


def test_clock_pulse_error(default_clock):
    with pytest.raises(TypeError):
        default_clock.pulse("Fail")  # type: ignore


@pytest.mark.parametrize(
    "clock_time, time_on_clock, expected",
    (
        (0, 0, 0),
        (1, 0, 1),
        (700, 0, -20),
        (1440, 0, 0),
        (0, 1440, 0),
        (-1440, 1440, 0),
        (10, 0, 10),
        (0, 10, -10),
        (100, 130, -30),
        (0, 719, 1),
        (30, 690, 60),
    ),
)
def test_clock_compare(default_clock, clock_time, time_on_clock, expected):
    default_clock.time_on_clock = time_on_clock
    default_clock.compare(clock_time)
    assert default_clock.slow == expected


def test_clock_clockrelay_protocol():
    assert hasattr(ClockRelay, "pulse")
    with pytest.raises(TypeError):
        ClockRelay()
