from math import sqrt

import pytest

from pytracer.primitives import FourTuple, Point, Vector3, approx_equal


def test_point_w_is_one():
    p = Point(1, 2, 3)
    assert p.w == 1.0


def test_vector3_w_is_zero():
    v = Vector3(1, 2, 3)
    assert v.w == 0.0


def test_add_point_and_vector():
    p = Point(3, -2, 5)
    v = Vector3(-2, 3, 1)

    assert p + v == Point(1, 1, 6)


def test_subtracting_two_points():
    p1 = Point(3, 2, 1)
    p2 = Point(5, 6, 7)

    assert p1 - p2 == FourTuple(-2, -4, -6, 0)


def test_subtract_a_vector_from_a_point():
    p = Point(3, 2, 1)
    v = Vector3(5, 6, 7)
    assert p - v == Point(-2, -4, -6)


def test_subtract_two_vectors():
    v1 = Vector3(3, 2, 1)
    v2 = Vector3(5, 6, 7)
    result = v1 - v2
    assert result == Vector3(-2, -4, -6)
    assert isinstance(result, Vector3)


def test_multiply_vector_by_int():
    v = Vector3(3, 2, 1)
    assert v * 2 == Vector3(6, 4, 2)


def test_multiply_tuple_by_float():
    v = Vector3(3, 2, 1)
    assert v * 0.5 == Vector3(1.5, 1, 0.5)


@pytest.mark.parametrize(
    ("x", "y", "z", "expected"),
    # fmt: off
    (
        (1, 0, 0, 1),
        (0, 1, 0, 1),
        (0, 0, 1, 1),
        (1, 2, 3, sqrt(14)),
    )
    # fmt: on
)
def test_vector_magnitude(x, y, z, expected):
    v = Vector3(x, y, z)
    assert v.magnitude == expected


@pytest.mark.parametrize(
    ("x", "y", "z", "expected"),
    # fmt: off
    (
        (4, 0, 0, Vector3(1, 0, 0)),
        (1, 2, 3, Vector3(0.26726, 0.53452, 0.80178)),
    )
    # fmt: on
)
def test_normalize(x, y, z, expected):
    v = Vector3(x, y, z)
    result = v.normalize()
    assert all(
        [
            approx_equal(result.x, expected.x),
            approx_equal(result.y, expected.y),
            approx_equal(result.z, expected.z),
            approx_equal(result.w, expected.w),
        ]
    )


def test_dot_product():
    v1 = Vector3(1, 2, 3)
    v2 = Vector3(2, 3, 4)
    assert v1.dot(v2) == 20


def test_cross_product():
    v1 = Vector3(1, 2, 3)
    v2 = Vector3(2, 3, 4)
    assert v1.cross_product(v2) == Vector3(-1, 2, -1)