import sys

from loguru import logger


def configure_logger():
    logger.remove(0)

    format = "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <magenta>{level}</magenta>:\t{message}"
    logger.add(sys.stderr, level="INFO", format=format)
    logger.add("app.log", level="INFO", format=format)
