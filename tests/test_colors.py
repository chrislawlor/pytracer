import pytest

from pytracer.color import Color
from pytracer.utils import approx_equal


def assert_color_approx_equal(c1, c2):
    assert approx_equal(c1.red, c2.red)
    assert approx_equal(c1.green, c2.green)
    assert approx_equal(c1.blue, c2.blue)


@pytest.mark.parametrize(
    ["color1", "color2", "expected"],
    ((Color(0, 0.5, 0), Color(0, 0.5, 0), Color(0, 1, 0)),),
)
def test_add_two_colors(color1, color2, expected):
    result = color1 + color2
    assert_color_approx_equal(result, expected)


def test_subtract_two_colors():
    c1 = Color(0.9, 0.6, 0.75)
    c2 = Color(0.7, 0.1, 0.25)
    result = c1 - c2
    assert_color_approx_equal(result, Color(0.2, 0.5, 0.5))


def test_multiply_color_by_scalar():
    c = Color(0.2, 0.3, 0.4)
    result = c * 2
    assert result == Color(0.4, 0.6, 0.8)


def test_hadamard_product():
    # multiply color * color
    c1 = Color(1, 0.2, 0.4)
    c2 = Color(0.9, 1, 0.1)
    result = c1 * c2
    assert_color_approx_equal(result, Color(0.9, 0.2, 0.04))


@pytest.mark.parametrize(
    ("r", "g", "b", "expected"),
    # fmt: off
    (
        (255, 255, 255, Color(1, 1, 1)),
        (0, 0, 0, Color(0, 0, 0)),
        (128, 128, 128, Color(0.502, 0.502, 0.502)),
    ),
    # fmt: on
)
def test_from_rgb(r, g, b, expected):
    c = Color.from_rgb(r, g, b)
    assert_color_approx_equal(c, expected)


@pytest.mark.parametrize(
    ("hex", "expected"),
    (
        # fmt: off
        ("ff00ff", Color(1, 0, 1)),
        ("112233", Color.from_rgb(17, 34, 51)),
        # fmt: on
    ),
)
def test_from_hex(hex, expected):
    assert_color_approx_equal(Color.from_hex(hex), expected)
