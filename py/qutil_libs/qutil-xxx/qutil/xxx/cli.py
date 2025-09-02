from qutil.console.color_print import ColorPrint 
from qutil.log.log import setup_logger 


def main():
    setup_logger(console_log=False, level="DEBUG")
    cp = ColorPrint(
        use_icons=True, style="bold white on blue blink"
    )
    cp.print(
        "This is a message with bold white text on blue background and blinking.",
    )

    cp.reset()
    cp.info("This is an info message.")
    cp.warn("This is a warning message.")
    cp.error("This is an error message.")
    cp.success("This is a success message.")
    cp.debug("This is a debug message.")
    cp.fail("This is a failure message.")
    cp.print("This is a bold red text with black background.", style="bold red on black")

    cp.set(prefix_log_level=True)
    cp.info("This is an info message.")
    cp.warn("This is a warning message.")
    cp.error("This is an error message.")
    cp.success("This is a success message.")
    cp.debug("This is a debug message.")
    cp.fail("This is a failure message.")
    cp.print("This is a bold red text with black background.", style="bold red on black")

# Example usage
if __name__ == "__main__":
    main()