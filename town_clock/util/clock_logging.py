"""
Todo: Ensure file location in exception logs point to the correct place.
"""
from __future__ import annotations

import os
import sys
from logging.handlers import TimedRotatingFileHandler
from pathlib import Path
import time

from loguru import logger


logger.remove(0)
loglevel = os.getenv("Town_Clock_Log_Level", default="INFO")
loglevel = "DEBUG"
logger.add(sink=sys.stdout, level=loglevel, colorize=True)
logger.level(name="PULSE", no=45, color="<blue><bold>")

resource_folder = Path(__file__).joinpath("../../../resources/logs").resolve()

pulse_handler_file = resource_folder.joinpath("pulse.log")
pulse_handler_file.touch()
handler_file = resource_folder.joinpath("clock.log")
handler_file.touch()

pulse_handler = TimedRotatingFileHandler(
    filename=pulse_handler_file,
    when="W0",
    interval=1,
    backupCount=3,
    encoding=None,
    delay=False,
    utc=False,
    atTime=None,
    errors=None,
)

# Todo: Review impact on time and resources that loguru takes.

logger.add(
    pulse_handler,
    format=f"{{time}},{{message}}",  # Todo: Add csv formating.
    level="PULSE",
    colorize=False,
    filter=(lambda record: record["level"].name == "PULSE"),
    serialize=False,
)

everything_handler = TimedRotatingFileHandler(
    filename=resource_folder.joinpath("clock.log"),
    when="W0",
    interval=1,
    backupCount=8,
    encoding=None,
    delay=False,
    utc=False,
    atTime=None,
    errors=None,
)

logger.add(
    everything_handler,
    level=loglevel,
    colorize=False,
    filter=(lambda record: record["level"].name != "PULSE"),
    serialize=False,
)
