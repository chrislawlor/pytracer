"""
Create points for a clock face using matrix transformations
"""
import sys
from math import pi

from pytracer import PPM, Canvas, Color, Matrix, Point

RADIUS = 100  # in pixels
IMG_SIZE = 300  # in pixels
POINT_COLOR = Color.from_hex("BBFF28")
FACE_COLOR = Color.from_hex("101626")


def make_points() -> list[Point]:
    """
    Create a point for each numeral, centered around 0, 0, 0
    """

    points = []
    # There are 2π radians in a circle
    radians_per_point = 2 * pi / 12
    for i in range(12):
        point = Point(0, 1, 0)
        scale = Matrix.scaling(0, RADIUS, 0)
        rotate = Matrix.rotation_z(i * radians_per_point)
        transform = rotate * scale  # apply transformations in reverse
        transformed = transform * point
        points.append(transformed)
    return points


def convert_point_to_image_coords(points) -> list[Point]:
    # Clock face is centered around 0, 0, 0,
    #  but image coords have 0, 0 in upper left
    transform = Matrix.translation(IMG_SIZE / 2, IMG_SIZE / 2, 0)
    result = []
    for point in points:
        result.append(transform * point)
    return result


def draw_point_on_canvas(canvas: Canvas, point: Point):
    """
    Draw a shape centered around point:

          x
         xxx
        xxPxx
         xxx
          x

    """
    # normalize point
    x, y = int(round(point.x)), int(round(point.y))
    color = POINT_COLOR
    darker = color - Color(0.4, 0.4, 0.4)

    # simulate a light at the upper left, so lower right
    # edge is darker. Points are darker to simulate
    # anti-aliasing
    canvas.write_pixel(x, y - 2, darker)
    canvas.write_pixel(x - 1, y - 1, color)
    canvas.write_pixel(x, y - 1, color)
    canvas.write_pixel(x + 1, y - 1, color)
    canvas.write_pixel(x - 2, y, darker)
    canvas.write_pixel(x - 1, y, color)
    canvas.write_pixel(x, y, color)
    canvas.write_pixel(x + 1, y, color)
    canvas.write_pixel(x + 2, y, darker)
    canvas.write_pixel(x, y + 1, color)
    canvas.write_pixel(x - 1, y + 1, color)
    canvas.write_pixel(x + 1, y + 1, darker)
    canvas.write_pixel(x, y + 2, darker)


def create_canvas():
    points = convert_point_to_image_coords(make_points())
    canvas = Canvas(IMG_SIZE, IMG_SIZE, fill=FACE_COLOR)
    for point in points:
        draw_point_on_canvas(canvas, point)
    return canvas


if __name__ == "__main__":
    canvas = create_canvas()
    PPM.save(canvas, sys.stdout)
