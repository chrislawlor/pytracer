from __future__ import annotations

from dataclasses import dataclass
from math import sqrt

from .utils import approx_equal

number = int | float


@dataclass(slots=True, frozen=True)
class FourTuple:
    x: float
    y: float
    z: float
    w: float

    @property
    def magnitude(self):
        return sqrt(self.x**2 + self.y**2 + self.z**2 + self.w**2)

    def dot(self, other: FourTuple) -> number:
        return self.x * other.x + self.y * other.y + self.z * other.z + self.w * other.w

    def cross_product(self, other: FourTuple) -> Vector3:
        """Cross product returns a vector which is perpendicular to the input vectors"""
        if self.w != 0 or other.w != 0:
            raise NotImplementedError(
                "Cross product of non-Vector objects is not supported"
            )
        return Vector3(
            x=self.y * other.z - self.z * other.y,
            y=self.z * other.x - self.x * other.z,
            z=self.x * other.y - self.y * other.x,
        )

    def normalize(self):
        magnitude = self.magnitude
        return FourTuple(
            x=self.x / magnitude,
            y=self.y / magnitude,
            z=self.z / magnitude,
            w=self.w / magnitude,
        )

    def reflect(self, normal: Vector3) -> Vector3:
        return self - normal * 2 * self.dot(normal)

    def __sub__(self, other: FourTuple) -> FourTuple:
        return self.__class__(
            self.x - other.x, self.y - other.y, self.z - other.z, self.w - other.w
        )

    def __eq__(self, other) -> bool:
        return isinstance(other, FourTuple) and all(
            [
                approx_equal(self.x, other.x),
                approx_equal(self.y, other.y),
                approx_equal(self.z, other.z),
                self.w == other.w,
            ]
        )

    def __mul__(self, scalar: number):
        return self.__class__(
            x=self.x * scalar, y=self.y * scalar, z=self.z * scalar, w=self.w * scalar
        )

    def __add__(self, other: FourTuple):
        return FourTuple(
            x=self.x + other.x,
            y=self.y + other.y,
            z=self.z + other.z,
            w=self.w + other.w,
        )

    def __div__(self, scalar: number):
        return FourTuple(
            x=self.x / scalar, y=self.y / scalar, z=self.z / scalar, w=self.w / scalar
        )


@dataclass(slots=True, frozen=True, order=False)
class Point(FourTuple):
    x: float
    y: float
    z: float
    w: float = 1.0

    def __eq__(self, other) -> bool:
        return super(Point, self).__eq__(other)


@dataclass(slots=True, frozen=True)
class Vector3(FourTuple):
    x: float
    y: float
    z: float
    w: float = 0.0

    def __neg__(self) -> Vector3:
        return Vector3(x=-self.x, y=-self.y, z=-self.z)

    def __eq__(self, other) -> bool:
        return super(Vector3, self).__eq__(other)
