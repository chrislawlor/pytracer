from .color import Color


class DummyPoint:
    """
    Adding this to see how Coveralls reports on new, untested code.
    """

    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y


class Canvas:
    def __init__(self, width: int, height: int, fill=Color(0, 0, 0)):
        self.width = width
        self.height = height
        self.pixels: list[Color] = [fill for _ in range(width * height)]

    def write_pixel(self, x: int, y: int, color: Color) -> None:
        self.pixels[self._index_for_coords(x, y)] = color

    def pixel_at(self, x: int, y: int) -> Color:
        return self.pixels[self._index_for_coords(x, y)]

    def _index_for_coords(self, x, y) -> int:
        # x is width, y is height
        # bounds are [0, width-1], [0, height-1]
        if x < 0 or x >= self.width:
            raise IndexError(f"x out of bounds: {x}")
        if y < 0 or y >= self.height:
            raise IndexError(f"y out of bounds: {y}")
        return self.width * y + x

    def __iter__(self):
        return self.pixels.__iter__()
