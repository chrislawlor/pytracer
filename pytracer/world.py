from __future__ import annotations

from dataclasses import dataclass, field
from math import sqrt
from typing import Optional

from .color import Color
from .light import PointLight
from .matrix import Matrix
from .primitives import Point, Vector3
from .ray import Intersection, Ray
from .shapes import Shape
from .utils import EPSILON

MAX_REFLECTIONS = 5


@dataclass
class World:
    shapes: list[Shape] = field(default_factory=list)
    lights: list[PointLight] = field(default_factory=list)

    def color_at(self, ray, remaining=MAX_REFLECTIONS) -> Color:
        if remaining == 0:
            return Color(0, 0, 0)
        intersections = self.intersect(ray)
        hit = Intersection.hit(intersections)
        if hit is None:
            return Color(0, 0, 0)
        comps = self.prepare_computations(hit, ray, intersections)
        return self.shade_hit(comps, remaining=remaining)

    def is_shadowed(self, point: Point, light: PointLight) -> bool:
        v = light.position - point
        distance = v.magnitude
        direction = v.normalize()

        r = Ray(point, direction)
        intersections = self.intersect(r)
        h = Intersection.hit(intersections)
        if h and h.t < distance:
            return True
        return False

    def intersect(self, ray: Ray) -> list[Intersection]:
        """Returns list of Intersections sorted by t"""
        intersections = []
        for sphere in self.shapes:
            intersections += ray.intersects(sphere)
        intersections.sort(key=lambda i: i.t)
        return intersections

    @staticmethod
    def prepare_computations(
        intersection: Intersection,
        ray: Ray,
        intersections: Optional[list[Intersection]] = None,
    ) -> Comps:
        if intersections is None:
            intersections = [intersection]

        n1, n2 = World._find_n1_and_n2(intersection, intersections)

        position = ray.position(intersection.t)
        eyev = -ray.direction
        normalv = intersection.shape.normal_at(position)
        inside = False

        if normalv.dot(eyev) < 0:
            inside = True
            normalv = -normalv
        return Comps(
            t=intersection.t,
            shape=intersection.shape,
            position=position,
            over_point=position + normalv * EPSILON,
            under_point=position - normalv * EPSILON,
            eyev=eyev,
            normalv=normalv,
            reflectv=ray.direction.reflect(normalv),
            inside=inside,
            n1=n1,
            n2=n2,
        )

    def shade_hit(self, comps: Comps, remaining=MAX_REFLECTIONS) -> Color:
        """Computes color for each light and return the sum"""
        color = Color(0, 0, 0)
        for light in self.lights:
            is_shadowed = self.is_shadowed(comps.over_point, light)

            surface = comps.shape.material.lighting(
                light,
                comps.position,
                comps.eyev,
                comps.normalv,
                in_shadow=is_shadowed,
                local_transform=comps.shape.transform,
            )

            reflected = self.reflected_color(comps, remaining=remaining)
            refracted = self.refracted_color(comps, remaining=remaining)

            material = comps.shape.material
            if material.reflective > 0 and material.transparency > 0:
                reflectance = self.schlick(comps)
                color += (
                    surface + reflected * reflectance + refracted * (1 - reflectance)
                )
            else:
                color += surface + reflected + refracted
        return color

    def reflected_color(self, comps: Comps, remaining=MAX_REFLECTIONS) -> Color:
        if comps.shape.material.reflective == 0:
            return Color(0, 0, 0)

        reflect_ray = Ray(comps.over_point, comps.reflectv)
        color = self.color_at(reflect_ray, remaining=remaining - 1)
        return color * comps.shape.material.reflective

    def refracted_color(self, comps: Comps, remaining=MAX_REFLECTIONS) -> Color:

        if comps.shape.material.transparency == 0 or remaining == 0:
            return Color(0, 0, 0)

        # Check for total internal reflection.
        # Find the ratio of the first index of refraction to the second
        # (inverse of Snell's Law)
        n_ratio = comps.n1 / comps.n2

        # cos(theta_i) is the same as the dot product of these vectors:
        cos_i = comps.eyev.dot(comps.normalv)

        # Find sin(theta_t) ** 2 via trigometric identity
        sin2_t = n_ratio**2 * (1 - cos_i**2)

        if sin2_t > 1:
            # Total internal reflection
            return Color(0, 0, 0)

        # Find cos(theta_t) via trigometric identity
        cos_t = sqrt(1.0 - sin2_t)

        # Compute the direction of the refracted ray
        direction = comps.normalv * (n_ratio * cos_i - cos_t) - comps.eyev * n_ratio

        # Create the refracted ray
        refract_ray = Ray(comps.under_point, direction)

        # Find the color of the refracted ray, multiplying by transparency
        # value to account for any opacity
        return (
            self.color_at(refract_ray, remaining=remaining - 1)
            * comps.shape.material.transparency
        )

    @classmethod
    def view_transform(cls, from_: Point, to: Point, up: Vector3):
        forward = (to - from_).normalize()
        up = up.normalize()
        left = forward.cross_product(up)
        true_up = left.cross_product(forward)
        orientation = Matrix(
            [
                [left.x, left.y, left.z, 0],
                [true_up.x, true_up.y, true_up.z, 0],
                [-forward.x, -forward.y, -forward.z, 0],
                [0, 0, 0, 1],
            ]
        )
        return orientation * Matrix.translation(-from_.x, -from_.y, -from_.z)

    @staticmethod
    def schlick(comps: Comps) -> float:
        cos = comps.eyev.dot(comps.normalv)

        # total internal reflection can only occur if n1 > n2
        if comps.n1 > comps.n2:
            n = comps.n1 / comps.n2
            sin2_t = n**2 * (1 - cos**2)

            if sin2_t > 1:
                return 1.0

            # compute cos(theta_t) using trigometric identity
            cos_t = sqrt(1.0 - sin2_t)

            # when n1 > n2, use cos(theta_t) instead
            cos = cos_t

        r0 = ((comps.n1 - comps.n2) / (comps.n1 + comps.n2)) ** 2
        return r0 + (1 - r0) * (1 - cos) ** 5

    @staticmethod
    def _find_n1_and_n2(
        hit: Intersection, intersections: list[Intersection]
    ) -> tuple[float, float]:
        # TODO: Find a more efficient algorithm
        n1 = 1.0  # refractive index of material being exited
        n2 = 1.0  # refractive index of material being entered

        containers: list[Shape] = []
        for intersection in intersections:
            if intersection == hit:
                if len(containers) == 0:
                    n1 = 1.0
                else:
                    # this intersection must be exiting the object
                    n1 = containers[-1].material.refractive_index

            if intersection.shape in containers:
                containers.remove(intersection.shape)
            else:
                containers.append(intersection.shape)

            if intersection == hit:
                if len(containers) == 0:
                    n2 = 1.0
                else:
                    n2 = containers[-1].material.refractive_index

        return n1, n2


@dataclass(slots=True)
class Comps:
    t: float
    shape: Shape
    position: Point
    over_point: Point
    under_point: Point
    eyev: Vector3
    normalv: Vector3
    reflectv: Vector3
    n1: float = 1.0
    n2: float = 1.0
    inside: bool = False
