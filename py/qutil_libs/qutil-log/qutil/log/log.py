from loguru import logger
import sys
import logging
import logging.handlers


def setup_logger(log_file=None, console_log=False, level="DEBUG"):
    """Function to setup a logger with syslog and optional file logging"""
    logger.remove()  # Remove the default logger
    handler = logging.handlers.SysLogHandler(address="/dev/log")
    logger.add(handler, level=level)

    if console_log:
        logger.add(sys.stdout, level=level, colorize=True)

    if log_file:
        logger.add(
            log_file,
            level=level,
            rotation="1 MB",
            retention="10 days",
            compression="zip",
        )
    logger.info(f"Logger  is set up with level {level}")
