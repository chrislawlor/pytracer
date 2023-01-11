"""
3D ray casting
"""

import argparse
import concurrent.futures
import sys
from typing import Generator, Optional

from pytracer import (
    PPM,
    Canvas,
    Color,
    Intersection,
    Material,
    Point,
    PointLight,
    Ray,
    Sphere,
)

ray_origin = Point(0, 0, -5)
wall_size = 7.0


# Multiprocessing state

wall_z = 10
shape = None
light = None


def init_worker(sphere_color, ambient, diffuse, specular, shininess):
    global shape
    global light
    shape = Sphere()
    shape.material = Material(
        color=Color.from_hex(sphere_color),
        ambient=ambient,
        diffuse=diffuse,
        specular=specular,
        shininess=shininess,
    )
    light = PointLight(Point(-10, 10, -10), Color(1, 1, 1))


def calculate_pixel_at_world_coords(args) -> tuple[int, int, Optional[Color]]:
    x, y, world_x, world_y = args
    if shape is None:
        return (x, y, Color(0, 0, 0))
    # describe the point on the wall that the ray will target
    target = Point(world_x, world_y, wall_z)
    r = Ray(ray_origin, (target - ray_origin).normalize())
    xs = r.intersects(shape)
    hit = Intersection.hit(xs)
    if hit is not None:
        position = r.position(hit.t)
        normalv = hit.shape.normal_at(position)
        eyev = -r.direction
        color = shape.material.lighting(
            light, position, eyev, normalv, local_transform=shape.transform
        )
    else:
        color = None
    return (x, y, color)


def generate_worker_args(
    width: int,
    height: int,
) -> Generator[tuple[int, int, float, float], None, None]:
    pixel_size = wall_size / width  # size of a pixel in world space units
    half = wall_size / 2
    # shape.transform = Matrix.scaling(1, 0.5, 1)

    for y in range(height):
        # compute y world coords
        world_y = half - pixel_size * y

        for x in range(width):
            # compute x world coords
            world_x = -half + pixel_size * x

            yield x, y, world_x, world_y


def main(
    canvas_size: int,
    canvas_color: str,
    sphere_color: str,
    ambient: float,
    diffuse: float,
    specular: float,
    shininess: float,
    max_workers=8,
    chunksize=500,
):
    canvas = Canvas(canvas_size, canvas_size, fill=Color.from_hex(canvas_color))

    with concurrent.futures.ProcessPoolExecutor(
        max_workers=max_workers,
        initializer=init_worker,
        initargs=(sphere_color, ambient, diffuse, specular, shininess),
    ) as executor:
        for x, y, color in executor.map(
            calculate_pixel_at_world_coords,
            generate_worker_args(canvas.height, canvas.width),
            chunksize=chunksize,
        ):
            if color is not None:
                canvas.write_pixel(x, y, color)

    PPM.save(canvas, sys.stdout)


if __name__ == "__main__":
    DEFAULT_CANVAS_COLOR = "556270"
    DEFAULT_SPHERE_COLOR = "FF0066"

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-s", "--canvas-size", default=200, type=int, help="Canvas size (pixels)"
    )
    parser.add_argument(
        "--canvas-color", default=DEFAULT_CANVAS_COLOR, help="Canvas color (hex)"
    )
    parser.add_argument(
        "--sphere-color", default=DEFAULT_SPHERE_COLOR, help="Sphere color (hex)"
    )
    parser.add_argument(
        "--ambient", default=0.1, type=float, help="Sphere material ambience (0-1)"
    )
    parser.add_argument(
        "--diffuse", default=0.9, type=float, help="Sphere material diffuse (0-1)"
    )
    parser.add_argument(
        "--specular", default=0.9, type=float, help="Sphere material specular (0-1)"
    )
    parser.add_argument(
        "--shininess",
        default=50,
        type=float,
        help="Sphere shininess (50-200 work well)",
    )
    parser.add_argument("--max-workers", type=int, help="Number of Python processes")
    parser.add_argument(
        "--chunksize",
        type=int,
        default=500,
        help="Python process executor task chunksize",
    )

    args = parser.parse_args()
    main(**args.__dict__)
