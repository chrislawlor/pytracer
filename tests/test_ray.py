from math import sqrt

import pytest

from pytracer import Color, Material, Matrix, Point, Ray, Sphere, Vector3, World
from pytracer.ray import Intersection
from pytracer.utils import EPSILON

from .utils import approx


def glass_sphere(refractive_index=1.5) -> Sphere:
    material = Material(
        color=Color(1, 1, 1),
        ambient=0.1,
        diffuse=0.9,
        specular=0.9,
        shininess=200,
        transparency=1.0,
        refractive_index=refractive_index,
    )
    return Sphere(material=material)


def test_creating_and_querying_a_ray():
    origin = Point(1, 2, 3)
    direction = Vector3(4, 5, 6)
    ray = Ray(origin, direction)
    assert ray.origin == origin
    assert ray.direction == direction


@pytest.mark.parametrize(
    ("t", "expected"),
    (
        (0, Point(2, 3, 4)),
        (1, Point(3, 3, 4)),
        (-1, Point(1, 3, 4)),
        (2.5, Point(4.5, 3, 4)),
    ),
)
def test_computing_a_point_from_a_distance(t, expected):
    r = Ray(Point(2, 3, 4), Vector3(1, 0, 0))
    assert r.position(t) == expected
    r = Ray(Point(2, 3, 4), Vector3(1, 0, 0))
    assert r.position(t) == expected


def test_intersect_sets_the_object_on_the_intersection():
    r = Ray(Point(0, 0, -5), Vector3(0, 0, 1))
    s = Sphere()
    xs = r.intersects(s)
    assert len(xs) == 2
    assert xs[0].shape == s


def test_a_ray_intersects_a_sphere_at_two_points():
    r = Ray(Point(0, 0, -5), Vector3(0, 0, 1))
    s = Sphere()
    xs = r.intersects(s)
    assert len(xs) == 2
    assert xs[0].t == 4.0
    assert xs[1].t == 6.0


def test_a_ray_intersects_a_sphere_at_a_tangent():
    r = Ray(Point(0, 1, -5), Vector3(0, 0, 1))
    s = Sphere()
    xs = r.intersects(s)
    assert len(xs) == 2
    assert xs[0].t == xs[1].t == 5.0


def test_a_ray_misses_a_sphere():
    r = Ray(Point(0, 2, -5), Vector3(0, 0, 1))
    s = Sphere()
    xs = r.intersects(s)
    assert len(xs) == 0


def test_a_ray_originates_inside_a_sphere():
    # intersections can occur at negative t!
    r = Ray(Point(0, 0, 0), Vector3(0, 0, 1))
    s = Sphere()
    xs = r.intersects(s)
    assert len(xs) == 2
    assert xs[0].t == -1.0
    assert xs[1].t == 1.0


def test_a_sphere_is_behind_a_ray():
    r = Ray(Point(0, 0, 5), Vector3(0, 0, 1))
    s = Sphere()
    xs = r.intersects(s)
    assert len(xs) == 2
    assert xs[0].t == -6.0
    assert xs[1].t == -4.0


def test_hit_when_all_intersections_have_positive_t():
    s = Sphere()
    i1 = Intersection(t=1, shape=s)
    i2 = Intersection(t=2, shape=s)
    i = Intersection.hit([i1, i2])
    assert i == i1


def test_hit_when_some_intersections_have_negative_t():
    s = Sphere()
    i1 = Intersection(t=-1, shape=s)
    i2 = Intersection(t=1, shape=s)
    i = Intersection.hit([i1, i2])
    assert i == i2


def test_hit_is_always_lowest_non_negative_intersection():
    s = Sphere()
    xs = [Intersection(t=t, shape=s) for t in (5, 7, -3, 2)]
    hit = Intersection.hit(xs)
    assert hit.t == 2


def test_intersecting_a_scaled_sphere_with_a_ray():
    r = Ray(Point(0, 0, -5), Vector3(0, 0, 1))
    s = Sphere()
    s.transform = Matrix.scaling(2, 2, 2)
    xs = r.intersects(s)
    assert len(xs) == 2
    assert xs[0].t == 3
    assert xs[1].t == 7


def test_intersecting_a_translated_sphere_with_a_ray():
    r = Ray(Point(0, 0, -5), Vector3(0, 0, 1))
    s = Sphere()
    s.transform = Matrix.translation(5, 0, 0)
    xs = r.intersects(s)
    assert len(xs) == 0


def test_the_hit_should_offset_the_point(sphere):
    r = Ray(Point(0, 0, -5), Vector3(0, 0, 1))
    sphere.transform = Matrix.translation(0, 0, 1)
    i = Intersection(5, sphere)
    comps = World.prepare_computations(i, r)
    assert comps.over_point.z < -EPSILON / 2
    assert comps.position.z > comps.over_point.z


def test_under_point_is_offset_below_the_surface():
    r = Ray(Point(0, 0, -5), Vector3(0, 0, 1))
    shape = glass_sphere()
    shape.transform = Matrix.translation(0, 0, 1)
    i = Intersection(5, shape)
    xs = [i]

    comps = World.prepare_computations(i, r, xs)

    assert comps.under_point.z > EPSILON / 2
    assert comps.position.z < comps.under_point.z


@pytest.mark.parametrize(
    ("intersection_idx", "n1", "n2"),
    (
        (0, 1.0, 1.5),
        (1, 1.5, 2.0),
        (2, 2.0, 2.5),
        (3, 2.5, 2.5),
        (4, 2.5, 1.5),
        (5, 1.5, 1.0),
    ),
)
def test_finding_n1_and_n2_at_various_intersections(intersection_idx, n1, n2):
    A = glass_sphere(refractive_index=1.5)
    A.transform = Matrix.scaling(2, 2, 2)

    B = glass_sphere(refractive_index=2.0)
    B.transform = Matrix.translation(0, 0, -0.25)

    C = glass_sphere(refractive_index=2.5)
    C.transform = Matrix.translation(0, 0, 0.25)

    r = Ray(Point(0, 0, -4), Vector3(0, 0, 1))
    xs = [
        Intersection(2, A),
        Intersection(2.75, B),
        Intersection(3.25, C),
        Intersection(4.75, B),
        Intersection(5.25, C),
        Intersection(6, A),
    ]

    comps = World.prepare_computations(xs[intersection_idx], r, xs)

    assert comps.n1 == n1
    assert comps.n2 == n2


def test_the_schlick_approximation_under_total_internal_reflaction():
    shape = glass_sphere()
    r = Ray(Point(0, 0, sqrt(2) / 2), Vector3(0, 1, 0))
    xs = [Intersection(-sqrt(2) / 2, shape), Intersection(sqrt(2) / 2, shape)]
    comps = World.prepare_computations(xs[1], r, xs)
    reflectance = World.schlick(comps)
    assert reflectance == 1.0


def test_the_schlick_approximation_with_a_perpendicular_viewing_angle():
    shape = glass_sphere()
    r = Ray(Point(0, 0, 0), Vector3(0, 1, 0))
    xs = [Intersection(-1, shape), Intersection(1, shape)]
    comps = World.prepare_computations(xs[1], r, xs)
    reflectance = World.schlick(comps)
    assert reflectance == approx(0.04)


def test_the_schick_approximation_with_small_angle_and_n2_gt_n1():
    shape = glass_sphere()
    r = Ray(Point(0, 0.99, -2), Vector3(0, 0, 1))
    xs = [Intersection(1.8589, shape)]
    comps = World.prepare_computations(xs[0], r, xs)
    reflectance = World.schlick(comps)
    assert reflectance == approx(0.48873)
