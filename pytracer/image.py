from io import StringIO
from typing import Generator, TextIO

from .canvas import Canvas
from .color import Color


class PPM:
    identifier = "P3"
    max_color_val = 255

    @classmethod
    def save(self, canvas: Canvas, destination: TextIO) -> None:

        for line in self.lines(canvas):
            destination.write(line)
            destination.write("\n")

    @classmethod
    def lines(cls, canvas: Canvas) -> Generator[str, None, None]:
        yield from cls.header(canvas)
        yield from cls.pixels(canvas.pixels)

    @classmethod
    def header(cls, canvas: Canvas) -> Generator[str, None, None]:
        yield cls.identifier
        yield f"{canvas.width} {canvas.height}"
        yield str(cls.max_color_val)

    @classmethod
    def pixels(cls, pixels: list[Color]) -> Generator[str, None, None]:
        # limit line length to 70 chars.
        buff = StringIO()
        for pixel in pixels:
            buff.write(f"{cls.pixel_to_color_string(pixel)}")
            # A color string can be ~11 chars, assuming a three digit
            # max color, so stop writing to this line at 59 chars,
            if buff.tell() >= 59:
                yield buff.getvalue()
                buff = StringIO()
            else:
                buff.write(" ")
        yield buff.getvalue().strip()
        yield "\n"

    @classmethod
    def pixel_to_color_string(cls, pixel: Color):
        # clamp colors to 0 - max_color_val
        red = max(0, min(round(pixel.red * cls.max_color_val), cls.max_color_val))
        green = max(0, min(round(pixel.green * cls.max_color_val), cls.max_color_val))
        blue = max(0, min(round(pixel.blue * cls.max_color_val), cls.max_color_val))
        return f"{red} {green} {blue}"
