#!/usr/bin/env python3

from .constants import LogLevel, Icon, ANSI_RESET, TextColor, BgColor, TextStyle
from .ansi_escape import AnsiEscape
from .log import setup_logger
from loguru import logger

class ColorPrint:
    """
    A utility class for printing colored and styled messages to the console.
    Supports logging and configurable use of icons, background colors, and text styles.
    """

    def __init__(self, use_icons=True, bg_color=None, style=None, prefix_log_level=False):
        """
        Initialize the ColorPrint instance.

        :param logger: Optional logger instance for logging messages.
        :param use_icons: Whether to include icons in the output.
        :param bg_color: Default background color for messages.
        :param style: Default text style for messages.
        :param prefix_log_level: Whether to prefix messages with the log level.
        """
        self.set(use_icons, bg_color, style, prefix_log_level)

    def set(self, use_icons=True, bg_color=None, style=None, prefix_log_level=False):
        """
        Configure the ColorPrint instance.

        :param use_icons: Whether to include icons in the output.
        :param bg_color: Default background color for messages.
        :param style: Default text style for messages.
        :param prefix_log_level: Whether to prefix messages with the log level.
        """
        self.use_icons = use_icons
        self.bg_color = bg_color
        self.style = style 
        self.prefix_log_level = prefix_log_level

    def reset(self):
        """
        Reset the configuration to default values.
        """
        self.set(use_icons=True, bg_color=None, style=None)

    def log_message(self, level, message):
        """
        Log and print a message with the specified log level.

        :param level: Log level (e.g., 'info', 'warning', 'error').
        :param message: The message to log and print.
        """
        message = message.to_string() if hasattr(message, 'to_string') else str(message)
        text_color = LogLevel[level.upper()]
        icon = Icon[level.upper()].value if self.use_icons else ''
        ansi_escape = AnsiEscape(text_color=text_color, bg_color=self.bg_color, style=self.style)
        if self.prefix_log_level:
            formatted_message = f"{ansi_escape.ansi_wrap(icon + ' ' + level.upper() + ': ' + message)}"
        else:
            formatted_message = f"{ansi_escape.ansi_wrap(icon + ' ' + message)}"
        print(formatted_message)

        if level.lower() == "success":
            level = "info"
        if level.lower() == "fail":
            level = "error"
        logger.log(level.upper(), message)

    def info(self, message):
        """
        Log and print an info-level message.
        """
        self.log_message('info', message)

    def warning(self, message):
        """
        Log and print a warning-level message.
        """
        self.log_message('warning', message)

    def error(self, message):
        """
        Log and print an error-level message.
        """
        self.log_message('error', message)

    def debug(self, message):
        """
        Log and print a debug-level message.
        """
        self.log_message('debug', message)

    def success(self, message):
        """
        Log and print a success-level message.
        """
        self.log_message('success', message)

    def fail(self, message):
        """
        Log and print a failure-level message.
        """
        self.log_message('fail', message)

    def print(self, message, text_color=None):
        """
        Print a message with the specified text color, using the default background color and style.

        :param message: The message to print.
        :param text_color: The text color to use.
        """
        ansi_escape = AnsiEscape(text_color=text_color, bg_color=self.bg_color, style=self.style)
        formatted_message = f"{ansi_escape.ansi_wrap(message)}"
        print(formatted_message)
        logger.log("INFO", message)

# Example usage
if __name__ == "__main__":
    setup_logger()
    cp = ColorPrint(use_icons=True, bg_color=BgColor.BG_BLUE, style=TextStyle.BOLD)
    cp.print("This is a message with white text and blue background.", TextColor.WHITE)

    cp.reset()
    cp.info("This is an info message.")
    cp.warning("This is a warning message.")
    cp.error("This is an error message.")
    cp.success("This is a success message.")
    cp.debug("This is a debug message.")
    cp.fail("This is a failure message.")
    cp.print("This is a bold red text with black background.", TextColor.RED)