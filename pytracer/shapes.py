from __future__ import annotations

import abc
from math import sqrt
from typing import Optional

from .materials import Material
from .matrix import Matrix
from .primitives import Point, Vector3
from .ray import Intersection, Ray
from .utils import EPSILON


class Shape(abc.ABC):
    def __init__(self, material: Optional[Material] = None):
        self.transform = Matrix.identity(4)
        self.material = material or Material.default()

    @abc.abstractmethod
    def local_intersect(self, local_ray: Ray) -> list[Intersection]:
        pass

    @abc.abstractmethod
    def normal_at(self, point: Point) -> Vector3:
        pass


class Sphere(Shape):
    def normal_at(self, point: Point) -> Vector3:
        object_point = self.transform.inverse() * point
        object_normal = object_point - Point(0, 0, 0)
        world_normal = self.transform.inverse().transpose() * object_normal
        # translations can mess up w, but it should always be zero.
        # our Vector3 are immutable, so we create a new one.
        world_normal = Vector3(x=world_normal.x, y=world_normal.y, z=world_normal.z)
        return world_normal.normalize()

    def local_intersect(self, ray: "Ray") -> list[Intersection]:
        sphere_to_ray = ray.origin - Point(0, 0, 0)
        a = ray.direction.dot(ray.direction)
        b = 2 * ray.direction.dot(sphere_to_ray)
        c = sphere_to_ray.dot(sphere_to_ray) - 1
        discriminant = b**2 - 4 * a * c
        if discriminant < 0:
            return []
        t1 = (-b - sqrt(discriminant)) / (2 * a)
        t2 = (-b + sqrt(discriminant)) / (2 * a)
        return [Intersection(t=t1, shape=self), Intersection(t=t2, shape=self)]


class Plane(Shape):
    def local_intersect(self, local_ray: Ray) -> list[Intersection]:
        if abs(local_ray.direction.y) < EPSILON:
            return []

        t = -local_ray.origin.y / local_ray.direction.y
        return [Intersection(t, self)]

    def normal_at(self, point: Point) -> Vector3:
        return Vector3(0, 1, 0)
