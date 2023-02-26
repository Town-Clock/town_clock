"""
Todo: Check out loguru
"""
from __future__ import annotations

import os
import sys
from logging.handlers import TimedRotatingFileHandler
from pathlib import Path

from loguru import logger

logger.remove(0)
loglevel = os.getenv("Town_Clock_Log_Level", default="INFO")
logger.add(sink=sys.stdout, level=loglevel, colorize=True)
logger.level(name="Pulse", no=45, color="<blue><bold>")

pulse_handler = TimedRotatingFileHandler(
    filename=Path(__file__ + "../resources/pule.log"),
    when="W0",
    interval=1,
    backupCount=14,
    encoding=None,
    delay=False,
    utc=False,
    atTime=None,
    errors=None,
)

logger.add(
    pulse_handler,
    level="INFO",
    colorize=False,
    # filter=...,
    serialize=False,
)

everything_handler = TimedRotatingFileHandler(
    filename=Path(__file__ + "../resources/clock.log"),
    when="W0",
    interval=1,
    backupCount=14,
    encoding=None,
    delay=False,
    utc=False,
    atTime=None,
    errors=None,
)
