from __future__ import annotations

from dataclasses import dataclass
from math import sqrt
from typing import Optional

from .primitives import Point, Vector3
from .sphere import Shape, Sphere


@dataclass(slots=True)
class Intersection:
    t: float
    shape: Shape

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
        sphere_to_ray = self.origin - Point(0, 0, 0)
        a = self.direction.dot(self.direction)
        b = 2 * self.direction.dot(sphere_to_ray)
        c = sphere_to_ray.dot(sphere_to_ray) - 1
        discriminant = b**2 - 4 * a * c
        if discriminant < 0:
            return []
        t1 = (-b - sqrt(discriminant)) / (2 * a)
        t2 = (-b + sqrt(discriminant)) / (2 * a)
        return [Intersection(t=t1, shape=sphere), Intersection(t=t2, shape=sphere)]