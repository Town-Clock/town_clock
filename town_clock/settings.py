from dataclasses import dataclass
import os
from pathlib import Path

LOCATION = {
    "latitude": "30.3402S",
    "longitude": "152.7124E",
    "altitude": 741,
}

PINS = {
    "clock_pins": [24, 25],
    "led_pin": 22,
    "common_pin": 23,
}

MODE = "dev"

SETTING_FILE = Path(__file__)
BASE_DIRECTORY = SETTING_FILE.parent.parent.resolve()
TESTS_DIRECTORY = BASE_DIRECTORY / "tests"

MODULE_DIRECTORY = BASE_DIRECTORY / "town_clock"
CLOCK_DIRECTORY = MODULE_DIRECTORY / "clock"
UI_DIRECTORY = MODULE_DIRECTORY / "ui"
UTIL_DIRECTORY = MODULE_DIRECTORY / "util"

RESOURCE_DIRECTORY = BASE_DIRECTORY / "resources"
LOGGING_DIRECTORY = RESOURCE_DIRECTORY / "logs"


DIRECTORY = {
    "BASE_DIRECTORY": BASE_DIRECTORY,
    "TESTS_DIRECTORY": TESTS_DIRECTORY,
    "RESOURCE_DIRECTORY": RESOURCE_DIRECTORY,
    "MODULE_DIRECTORY": MODULE_DIRECTORY,
    "CLOCK_DIRECTORY": CLOCK_DIRECTORY,
    "UI_DIRECTORY": UI_DIRECTORY,
    "UTIL_DIRECTORY": UTIL_DIRECTORY,
}

FILES = {
    "SETTING_FILE": SETTING_FILE,
}

LCD_CONFIG = {
    "lcd_rows": 2,
    "lcd_columns": 16,
    "debounce_sleep": 0.001,
}

RELAY_PULSE_DELAY = 0.1

CLOCK_CUTOFF = 30
CLOCK_SLEEP_TIME = 0.5


@dataclass(
    init=True, eq=False, order=False, match_args=False, unsafe_hash=False, repr=False
)
class Settings:
    def __post_init__(self):
        self.__dict__ = {k: v for k, v in globals().items() if k.isupper()}

    def __str__(self):
        return str(self.__dict__)


settings = Settings()
print(SETTING_FILE.)
