from qutil.console.color_print import ColorPrint, BgColor, TextColor, TextStyle 


def main():
    cp = ColorPrint(
        use_icons=True, bg_color=BgColor.BG_BLUE, style=TextStyle.BOLD
    )
    cp.print(
        "This is a message with white text and blue background.",
        TextColor.WHITE,
    )

    cp.reset()
    cp.info("This is an info message.")
    cp.warning("This is a warning message.")
    cp.error("This is an error message.")
    cp.success("This is a success message.")
    cp.debug("This is a debug message.")
    cp.fail("This is a failure message.")
    cp.print("This is a bold red text with black background.", TextColor.RED)
# Example usage
if __name__ == "__main__":
    main()