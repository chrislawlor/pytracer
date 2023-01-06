import pytest

from pytracer import Matrix, Point, Ray, Sphere, Vector3
from pytracer.ray import Intersection


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
