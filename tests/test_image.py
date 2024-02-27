from io import StringIO
from textwrap import dedent

from pytracer.canvas import Canvas
from pytracer.color import Color
from pytracer.image import PPM


def test_defaults():
    assert PPM.identifier == "P3"
    assert PPM.max_color_val == 255


def test_ppm_header():
    c = Canvas(5, 3)
    ppm_lines = list(PPM.lines(c))
    assert ppm_lines[0] == PPM.identifier
    assert ppm_lines[1] == "5 3"
    assert ppm_lines[2] == str(PPM.max_color_val)


def test_ppm_pixel_data():
    c = Canvas(5, 3)
    c.write_pixel(0, 0, Color(1.5, 0, 0))
    c.write_pixel(2, 1, Color(0, 0.5, 0))
    c.write_pixel(4, 2, Color(-0.5, 0, 1))

    ppm_lines = list(PPM.lines(c))

    assert (
        ppm_lines[3]
        == "255 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 128 0 0 0 0 0 0 0"
    )
    assert ppm_lines[4] == "0 0 0 0 0 0 0 0 0 0 0 0 0 0 255"
    assert ppm_lines[5] == "\n"


# def test_save():
#     c = Canvas(2, 2)
#     c.write_pixel(0, 0, Color(0.5, 0.5, 0.5))
#     c.write_pixel(1, 1, Color(1, 1, 1))
#     dest = StringIO()

#     PPM.save(c, dest)

#     print(dest.getvalue())

#     expected = dedent(
#         """
#         P3
#         2 2
#         255
#         128 128 128 0 0 0 0 0 0 255 255 255


#         """
#     ).lstrip()  # removes leading whitespace for nicer formatting here

#     assert dest.getvalue() == expected
