#!/usr/bin/env python3


from .constants import (Icon, 
                        ERROR_STYLE, 
                        INFO_STYLE, 
                        WARN_STYLE, 
                        SUCCESS_STYLE, 
                        DEBUG_STYLE, 
                        FAIL_STYLE)

from loguru import logger
from rich.console import Console
from rich.text import Text
from rich.table import Table


class ColorPrint:
    """
    A utility class for printing colored and styled messages to the console.
    Now uses the rich library for output.
    """


    def __init__(self, 
                 use_icons=True, 
                 style=None, 
                 prefix_log_level=False):
        self.console = Console()
        self.set(use_icons, style, prefix_log_level)

    def set(self, use_icons=True, style=None, prefix_log_level=False):
        self.use_icons = use_icons
        self.style = style  # rich style string, e.g. 'bold red on yellow'
        self.prefix_log_level = prefix_log_level

    def reset(self):
        self.set(use_icons=True, style=None)


    def log_message(self, level, message, use_icon=None, style=None, prefix_log_level=None):
        message = message.to_string() if hasattr(message, "to_string") else str(message)
        if use_icon is None:
            use_icon = self.use_icons
        icon = Icon[level.upper()].value if use_icon else ""
        style_to_use = style if style is not None else self.style
        prefix_log_level_to_use = prefix_log_level if prefix_log_level is not None else self.prefix_log_level
        # Compose the message as a string with emoji shortcodes
        if prefix_log_level_to_use:
            msg = f"{icon} {level.upper()}: {message}"
        else:
            msg = f"{icon} {message}"
        self.console.print(msg, style=style_to_use, emoji=True)

        # Map 'success' and 'fail' to loguru levels
        log_level = level
        if level.lower() == "success":
            log_level = "info"
        if level.lower() == "fail":
            log_level = "error"
        logger.log(log_level.upper(), message)


    def info(self, message):
        self.log_message("info", message, style=INFO_STYLE)

    def warn(self, message):
        self.log_message("warning", message, style=WARN_STYLE)

    def error(self, message):
        self.log_message("error", message, style=ERROR_STYLE)

    def debug(self, message):
        self.log_message("debug", message, style=DEBUG_STYLE)

    def success(self, message):
        self.log_message("success", message, style=SUCCESS_STYLE)

    def fail(self, message):
        self.log_message("fail", message, style=FAIL_STYLE)

    def print(self, message, style=None):
        self.log_message("info", message, use_icon=False, style=style, prefix_log_level=False)


def to_rich_table(headers, rows, column_colors=None, title=None):
    """
    Create a rich Table with colored columns.
    Args:
        headers (list[str]): Column headers.
        rows (list[list]): Rows of data.
        column_colors (list[str|None]): List of rich style strings for each column, or None.
        title (str|None): Optional table title.
    Returns:
        Table: rich Table object ready to print.
    """
    table = Table(title=title)
    if column_colors is None:
        column_colors = [None] * len(headers)
    for header, color in zip(headers, column_colors):
        table.add_column(str(header), style=color if color else None)
    for row in rows:
        str_row = [str(cell) for cell in row]
        table.add_row(*str_row)
    return table