"""
2D ray casting
"""
import sys

from pytracer import PPM, Canvas, Color, Intersection, Matrix, Point, Ray, Sphere

ray_origin = Point(0, 0, -5)

wall_z = 10
wall_size = 7.0
canvas_pixels = 200

pixel_size = wall_size / canvas_pixels  # size of a pixel in world space units

half = wall_size / 2


def cast() -> Canvas:
    canvas = Canvas(canvas_pixels, canvas_pixels)
    color = Color(1, 0, 0)
    shape = Sphere()
    shape.transform = Matrix.scaling(1, 0.7, 1)

    for y in range(canvas_pixels):
        # compute y world coords
        world_y = half - pixel_size * y

        for x in range(canvas_pixels):
            # compute x world coords
            world_x = -half + pixel_size * x

            # describe the point on the wall that the ray will target
            target = Point(world_x, world_y, wall_z)
            r = Ray(ray_origin, (target - ray_origin).normalize())
            xs = r.intersects(shape)

            if Intersection.hit(xs) is not None:
                canvas.write_pixel(x, y, color)
    return canvas


def main():
    canvas = cast()
    PPM.save(canvas, sys.stdout)


if __name__ == "__main__":
    main()
    main()
