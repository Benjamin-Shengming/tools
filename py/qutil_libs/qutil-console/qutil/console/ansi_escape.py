#!/usr/bin/env python3

from .constants import (
    ANSI_START,
    ANSI_END,
    ANSI_RESET,
    TextColor,
    BgColor,
    TextStyle,
)


class AnsiEscape:
    def __init__(self, text_color=None, bg_color=None, style=None):
        self._text_color_code = text_color.value if text_color else None
        self._bg_color_code = bg_color.value if bg_color else None
        self._style_code = style.value if style else None

    @property
    def text_color(self):
        return self._text_color_code

    @text_color.setter
    def text_color(self, text_color):
        self._text_color_code = text_color.value if text_color else None

    @property
    def bg_color(self):
        return self._bg_color_code

    @bg_color.setter
    def bg_color(self, bg_color):
        self._bg_color_code = bg_color.value if bg_color else None

    @property
    def style(self):
        return self._style_code

    @style.setter
    def style(self, style):
        self._style_code = style.value if style else None

    def set_text_color(self, text_color):
        self.text_color = text_color
        return self

    def set_bg_color(self, bg_color):
        self.bg_color = bg_color
        return self

    def set_style(self, style):
        self.style = style
        return self

    def ansi_wrap(self, text):
        codes = []
        if self._style_code:
            codes.append(self._style_code)
        if self._text_color_code:
            codes.append(str(self._text_color_code))
        if self._bg_color_code:
            codes.append(str(self._bg_color_code))

        ansi_sequence = ANSI_START + ";".join(codes) + ANSI_END
        return f"{ansi_sequence}{text}{ANSI_RESET}"


if __name__ == "__main__":
    ta = (
        AnsiEscape()
        .set_text_color(TextColor.CYAN)
        .set_bg_color(BgColor.BG_MAGENTA)
        .set_style(TextStyle.BLINK)
    )

    print(ta.ansi_wrap("This is blinking cyan text with magenta background."))
    print("This is not colored text.")
    ta.set_text_color(TextColor.RED).set_style(TextStyle.BLINK).set_bg_color(
        None
    )
    print(ta.ansi_wrap("This is red and blink text."))

    ta.set_text_color(TextColor.RED).set_style(TextStyle.BOLD)
    print(ta.ansi_wrap("This is red and bold text."))

    ta.text_color = TextColor.GREEN
    ta.bg_color = BgColor.BG_BLACK
    ta.style = TextStyle.UNDERLINE
    print(ta.ansi_wrap("This is green underlined text with black background."))
