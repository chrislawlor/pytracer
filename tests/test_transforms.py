from math import pi, sqrt

from pytracer import Matrix, Point, Vector3

from .utils import approx, assert_fourtuple_approx_equal


def test_multiply_by_a_translation_matrix():
    transform = Matrix.translation(5, -3, 2)
    point = Point(-3, 4, 5)
    assert transform * point == Point(2, 1, 7)


def test_multiply_by_inverse_of_a_translation_matrix():
    transform = Matrix.translation(5, -3, 2)
    point = Point(-3, 4, 5)
    inverse = transform.inverse()
    assert inverse * point == Point(-8, 7, 3)


def test_translation_does_not_affect_vectors():
    transform = Matrix.translation(5, -3, 2)
    vec = Vector3(-3, 4, 5)
    assert transform * vec == vec


def test_a_scaling_matrix_applied_to_a_point():
    transform = Matrix.scaling(2, 3, 4)
    point = Point(-4, 6, 8)
    assert transform * point == Point(-8, 18, 32)


def test_a_scaling_matrix_applied_to_a_vector():
    transform = Matrix.scaling(2, 3, 4)
    vec = Vector3(-4, 6, 8)
    assert transform * vec == Vector3(-8, 18, 32)


def test_multiplying_by_the_inverse_of_a_scaling_matrix():
    transform = Matrix.scaling(2, 3, 4)
    inv = transform.inverse()
    vec = Vector3(-4, 6, 8)
    assert inv * vec == Vector3(-2, 2, 2)


def test_create_rotation_x_matrix():
    m = Matrix.rotation_x(pi / 2)
    assert m[0, 0] == 1
    assert m[1, 1] == approx(0)
    assert m[1, 2] == -1
    assert m[2, 1] == 1
    assert m[2, 2] == approx(0)


def test_rotatating_a_point_around_the_x_axis():
    point = Point(0, 1, 0)
    half_quarter = Matrix.rotation_x(pi / 4)
    full_quarter = Matrix.rotation_x(pi / 2)
    assert_fourtuple_approx_equal(
        half_quarter * point, Point(0, sqrt(2) / 2, sqrt(2) / 2)
    )
    result = full_quarter * point
    assert_fourtuple_approx_equal(result, Point(0, 0, 1))
