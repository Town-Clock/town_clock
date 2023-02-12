"""
conftest.py

Configuration for pytest suite.


Author: Zack Hankin
Started: 10/02/2023
"""
from __future__ import annotations

from _pytest.logging import LogCaptureFixture
from loguru import logger
from pytest import fixture


@fixture
def position():
    return NotImplemented


@fixture
def caplog(caplog: LogCaptureFixture):
    handler_id = logger.add(caplog.handler, format="{message}")
    yield caplog
    logger.remove(handler_id)
