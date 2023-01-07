from __future__ import annotations

from dataclasses import dataclass
from functools import total_ordering
from math import sqrt
from typing import Optional

from .matrix import Matrix
from .primitives import Point, Vector3
from .sphere import Sphere


@total_ordering
@dataclass(slots=True)
class Intersection:
    t: float
    shape: Sphere

    @staticmethod
    def hit(intersections: list[Intersection]) -> Optional[Intersection]:
        """
        Return the intersection with the lowest,
        but non-negative, t

        """
        if intersections == []:
            return None
        hit = None
        for i in intersections:
            if i.t > 0:
                if hit is not None:
                    if i.t < hit.t:
                        hit = i
                else:
                    hit = i
        return hit

    def __gt__(self, other) -> bool:
        return self.t > other.t

    def __eq__(self, other) -> bool:
        return (
            isinstance(other, Intersection)
            and self.t == other.t
            and self.shape == other.shape
        )


class Ray:
    def __init__(self, origin: Point, direction: Vector3):
        self.origin = origin
        self.direction = direction

    def position(self, t: float):
        """
        Return position of ray at time t
        """
        return self.origin + self.direction * t

    def intersects(self, sphere: Sphere) -> list[Intersection]:
        """
        Returns a list of two points t when ray intersects the
        given sphere.

        If ray is tangent to sphere, will still return two (equal)
        points.

        If ray does not intersect the sphere, an empty list is
        returned.
        """
        # We assume our sphere is centered at the origin
        ray = self.transform(sphere.transform.inverse())
        sphere_to_ray = ray.origin - Point(0, 0, 0)
        a = ray.direction.dot(ray.direction)
        b = 2 * ray.direction.dot(sphere_to_ray)
        c = sphere_to_ray.dot(sphere_to_ray) - 1
        discriminant = b**2 - 4 * a * c
        if discriminant < 0:
            return []
        t1 = (-b - sqrt(discriminant)) / (2 * a)
        t2 = (-b + sqrt(discriminant)) / (2 * a)
        return [Intersection(t=t1, shape=sphere), Intersection(t=t2, shape=sphere)]

    def transform(self, transformation: Matrix) -> Ray:
        """
        Transform by the given transformation matrix.
        Returns a new Ray.
        """
        return Ray(
            origin=transformation * self.origin,
            direction=transformation * self.direction,
        )
