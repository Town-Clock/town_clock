"""
Town-clock

Author: Zack Hankin
Email: zthankin@gmail.com
Version: 1.0.2
"""
import sys
from pathlib import Path

import tomli

from town_clock.controller import Controller
from town_clock.util import convert_position_string_to_number, Mode
from .util import Position

file = Path(__file__, "../../config/config.toml").resolve()

with open(file, "rb") as f:
    config = tomli.load(f)
CONFIG_LOCATION = config["Location"]

latitude = CONFIG_LOCATION["latitude"]
longitude = CONFIG_LOCATION["longitude"]
altitude = CONFIG_LOCATION["altitude"]

latitude = convert_position_string_to_number(latitude)
longitude = convert_position_string_to_number(longitude)

position = Position(latitude=latitude, longitude=longitude, altitude=altitude)

clock_pins = config["Pins"]["clock_pins"]
led_pin = config["Pins"]["led_pin"]
common_pin = config["Pins"]["common_pin"]
mode = Mode(config["Mode"]["mode"])

CONTROLLER = Controller(
    clock_pins=clock_pins,
    led_pin=led_pin,
    common_pin=common_pin,
    position=position,
    mode=mode,
)


def main():
    """
    Function to run project.
    """
    CONTROLLER.run()


if __name__ == "__main__":
    sys.exit(main())
