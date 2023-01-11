import pytest

from pytracer import Color, Matrix, Pattern, Point, Sphere

BLACK = Color(0, 0, 0)
WHITE = Color(1, 1, 1)


@pytest.fixture
def pattern() -> Pattern:
    return Pattern.stripes(WHITE, BLACK)


@pytest.mark.parametrize(
    ("x", "y", "z", "expected"),
    (
        (0, 0, 0, WHITE),
        (0, 1, 0, WHITE),
        (0, 2, 0, WHITE),
    ),
)
def test_stripe_pattern_constant_in_y(pattern: Pattern, x, y, z, expected: Color):
    point = Point(x, y, z)
    assert pattern.color_at_world_coords(point) == expected


@pytest.mark.parametrize(
    ("x", "y", "z", "expected"),
    (
        (0, 0, 0, WHITE),
        (0, 0, 1, WHITE),
        (0, 0, 2, WHITE),
    ),
)
def test_stripe_pattern_constant_in_z(pattern: Pattern, x, y, z, expected: Color):
    point = Point(x, y, z)
    assert pattern.color_at_world_coords(point) == expected


@pytest.mark.parametrize(
    ("x", "y", "z", "expected"),
    (
        (0, 0, 0, WHITE),
        (0.9, 0, 0, WHITE),
        (1, 0, 0, BLACK),
        (-0.1, 0, 0, BLACK),
        (-1, 0, 0, BLACK),
        (-1.1, 0, 0, WHITE),
    ),
)
def test_stripe_pattern_alternates_in_x(pattern: Pattern, x, y, z, expected: Color):
    point = Point(x, y, z)
    assert pattern.color_at_world_coords(point) == expected


def test_pattern_with_object_transformation(pattern: Pattern):
    shape = Sphere()
    shape.transform = Matrix.scaling(2, 2, 2)

    c1 = pattern.color_at_local_transform(shape.transform, Point(1.5, 0, 0))
    c2 = pattern.color_at_local_transform(shape.transform, Point(2, 0, 0))

    assert c1 == WHITE
    assert c2 == BLACK


def test_pattern_with_transformation(pattern: Pattern):
    shape = Sphere()
    pattern.transform = Matrix.scaling(2, 2, 2)

    c1 = pattern.color_at_local_transform(shape.transform, Point(1.5, 0, 0))
    c2 = pattern.color_at_local_transform(shape.transform, Point(2, 0, 0))

    assert c1 == WHITE
    assert c2 == BLACK


def test_pattern_with_pattern_and_object_transform(pattern: Pattern):
    shape = Sphere()
    shape.transform = Matrix.scaling(2, 2, 2)
    pattern.transform = Matrix.translation(0.5, 0, 0)

    c1 = pattern.color_at_local_transform(shape.transform, Point(2.5, 0, 0))
    c2 = pattern.color_at_local_transform(shape.transform, Point(0, 0, 0))

    assert c1 == WHITE
    assert c2 == BLACK
