#!/usr/bin/env python3

from enum import Enum

ANSI_START = "\033["
ANSI_END = "m"
ANSI_RESET = "\033[0m"

class TextColor(Enum):
    BLUE = '34'
    RED = '31'
    YELLOW = '33'
    GREEN = '32'
    MAGENTA = '35'
    CYAN = '36'
    WHITE = '37'
    BLACK = '30'

class BgColor(Enum):
    BG_BLUE = '44'
    BG_RED = '41'
    BG_YELLOW = '43'
    BG_GREEN = '42'
    BG_MAGENTA = '45'
    BG_CYAN = '46'
    BG_WHITE = '47'
    BG_BLACK = '40'

class TextStyle(Enum):
    BOLD = '1'
    BLINK = '5'
    STRIKE = '9'
    ITALIC = '3'
    UNDERLINE = '4'
    INVERSE = '7'
    HIDDEN = '8'
    DOUBLE_UNDERLINE = '21'

class LogLevel(Enum):
    INFO = TextColor.BLUE.value
    WARNING = TextColor.YELLOW.value
    ERROR = TextColor.RED.value
    SUCCESS = TextColor.GREEN.value
    DEBUG = TextColor.MAGENTA.value
    FAIL = TextColor.RED.value

class Icon(Enum):
    INFO = 'ℹ️'
    WARNING = '⚠️'
    ERROR = '❌'
    SUCCESS = '✅'
    DEBUG = '🐞'
    FAIL = '❗'