import argparse
import sys

from pytracer import PPM, Canvas, Color


def fill_block(
    canvas: Canvas, start_x: int, start_y: int, width: int, height: int, color: Color
):
    for y in range(height):
        for x in range(width):
            canvas.write_pixel(x + start_x, y + start_y, color)


def generate_canvas() -> Canvas:
    canvas = Canvas(200, 200)
    aoi = Color.from_rgb(105, 210, 231)
    pondwater = Color.from_rgb(167, 219, 216)
    beach_storm = Color.from_rgb(224, 228, 204)
    giant_goldfish = Color.from_rgb(243, 134, 48)

    fill_block(canvas, 0, 0, 50, 200, aoi)
    fill_block(canvas, 50, 0, 50, 200, pondwater)
    fill_block(canvas, 100, 0, 50, 200, beach_storm)
    fill_block(canvas, 150, 0, 50, 200, giant_goldfish)

    return canvas


def write(destination):
    canvas = generate_canvas()
    PPM.save(canvas, destination)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-o", "--output", help="output file path. Should have .ppm extension"
    )

    args = parser.parse_args()
    if args.output:
        with open(args.output, "w") as destination:
            write(destination)
    else:
        write(sys.stdout)
