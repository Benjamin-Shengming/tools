#!/usr/bin/env python3

from constants import COLORS, ICONS
from log import setup_logger
import logging

class ColorPrint:
    def __init__(self, logger=None):
        self.logger = logger

    def log_message(self, level, message):
        formatted_message = f"{COLORS[level]}{ICONS[level]} {level.upper()}: {message}{COLORS['endc']}"
        print(formatted_message)
        if self.logger:
            if level.lower() == "success":
                level = "info"
            if level.lower() == "failure":
                level = "error"
            self.logger.log(getattr(logging, level.upper()), message)

    def info(self, message):
        self.log_message('info', message)

    def warning(self, message):
        self.log_message('warning', message)

    def error(self, message):
        self.log_message('error', message)

    def success(self, message):
        self.log_message('success', message)

    def debug(self, message):
        self.log_message('debug', message)

    def failure(self, message):
        self.log_message('failure', message)

# Example usage
if __name__ == "__main__":
    logger = setup_logger('color_print_logger', 'color_print.log')
    cp = ColorPrint(logger)
    cp.info("This is an info message.")
    cp.warning("This is a warning message.")
    cp.error("This is an error message.")
    cp.success("This is a success message.")
    cp.debug("This is a debug message.")
    cp.failure("This is a failure message.")