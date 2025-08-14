#!/usr/bin/env python3

from enum import Enum


# Use rich's style strings directly for color and style, e.g.:
#   "red", "bold yellow", "on blue", "#ff8800", "italic underline green", etc.
INFO_STYLE="white"
WARN_STYLE="bold yellow"
ERROR_STYLE="bold red on black blink"
SUCCESS_STYLE="green"
DEBUG_STYLE="magenta"
FAIL_STYLE="bold red on black blink"

class LogLevel(Enum):
    INFO = "white"
    WARNING = "yellow"
    ERROR = "red"
    SUCCESS = "green"
    DEBUG = "magenta"
    FAIL = "red"


class Icon(Enum):
    INFO = ":information_source:"
    WARNING = ":warning:"
    ERROR = ":x:"
    SUCCESS = ":white_check_mark:"
    DEBUG = ":bug:"
    FAIL = ":exclamation:"
