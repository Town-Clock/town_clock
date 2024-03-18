"""
test init.py

"""

from loguru import logger

try:
    logger.remove(0)
except TypeError as error:
    logger.exception(error)
