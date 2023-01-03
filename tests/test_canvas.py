import pytest

from pytracer.canvas import Canvas
from pytracer.color import Color


def test_init_all_black():
    c = Canvas(10, 20)
    assert c.width == 10
    assert c.height == 20
    assert all([p == Color(0, 0, 0) for p in c])


def test_write_pixel_to_canvas():
    c = Canvas(10, 20)
    red = Color(1, 0, 0)
    c.write_pixel(2, 3, red)
    assert c.pixel_at(2, 3) == red


def test_bounds():
    c = Canvas(5, 5)
    with pytest.raises(IndexError):
        c.pixel_at(5, 0)
    with pytest.raises(IndexError):
        c.pixel_at(0, 5)


@pytest.mark.parametrize(
    ("x", "y", "expected"),
    (
        (0, 0, 0),
        (1, 0, 1),
        (4, 0, 4),
        (0, 1, 5),
        (1, 1, 6),
    ),
)
def test_index_for_coords(x, y, expected):
    """
    x x x x x
    x x x x x
    x x x x x
    x x x x x
    x x x x x
    """
    c = Canvas(5, 5)
    assert c._index_for_coords(x, y) == expected
