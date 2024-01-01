"""
Town-clock

Author: Zack Hankin
Email: zthankin@gmail.com
Version: 1.0.2
"""
from logging import config
import os
import sys
from typing import Any
from loguru import logger

import tomli

from town_clock.controller import Controller
from town_clock.settings import CONFIG_FILE, MODE_DEFAULT
from town_clock.util import convert_position_string_to_number, Mode
from icecream import ic


def read_config() -> dict[str, Any]:
    config = tomli.loads(CONFIG_FILE.read_text())
    return config


def set_mode_in_env(mode: Mode) -> None:
    """
    Set the mode in the environment.

    Args:
        mode (Mode): The mode to set.
    """
    os.environ["CLOCK_MODE"] = mode.value


def setup_controller(config: dict[str, Any]) -> Controller:
    CONFIG_LOCATION = config["Location"]
    return Controller(
        clock_pins=config["Pins"]["clock_pins"],
        led_pin=config["Pins"]["led_pin"],
        common_pin=config["Pins"]["common_pin"],
        lat=CONFIG_LOCATION["latitude"],
        long=CONFIG_LOCATION["longitude"],
        alt=CONFIG_LOCATION["altitude"],
    )


def main():
    """
    Function to run project.
    """
    config = read_config()
    set_mode_in_env(Mode(config["Clock_Mode"]["mode"]))
    controller = setup_controller(config)
    try:
        controller.run()
        return 0
    except Exception as e:
        logger.error(e)
        return 1


if __name__ == "__main__":
    sys.exit(main())
