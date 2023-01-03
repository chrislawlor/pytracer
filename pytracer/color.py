from __future__ import annotations

from dataclasses import dataclass

number = int | float


@dataclass(slots=True)
class Color:
    red: float
    green: float
    blue: float

    @classmethod
    def from_hex(cls, hexcode: str):
        return cls.from_rgb(
            red=int(hexcode[:2], 16),
            green=int(hexcode[2:4], 16),
            blue=int(hexcode[4:6], 16),
        )

    @classmethod
    def from_rgb(cls, red: int, green: int, blue: int):
        return cls(red=red / 255, green=green / 255, blue=blue / 255)

    def __eq__(self, other) -> bool:
        return isinstance(other, Color) and all(
            [self.red == other.red, self.green == other.green, self.blue == other.blue]
        )

    def __add__(self, other: Color) -> Color:
        return Color(
            red=self.red + other.red,
            green=self.green + other.green,
            blue=self.blue + other.blue,
        )

    def __sub__(self, other: Color) -> Color:
        return Color(
            red=self.red - other.red,
            green=self.green - other.green,
            blue=self.blue - other.blue,
        )

    def __mul__(self, other: number) -> Color:
        if isinstance(other, float | int):
            return Color(
                red=self.red * other, blue=self.blue * other, green=self.green * other
            )
        if isinstance(other, Color):
            return Color(
                red=self.red * other.red,
                blue=self.blue * other.blue,
                green=self.green * other.green,
            )
