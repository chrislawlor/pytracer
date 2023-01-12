import argparse
import sys

from pytracer.camera import Camera
from pytracer.image import PPM
from pytracer.render import render
from pytracer.serialization import load_yaml
from pytracer.world import World


def load_scene_file(filename) -> tuple[Camera, World]:
    with open(filename) as f:
        return load_yaml(f.read())


def main(filename, output, num_processes, width, height):

    camera, world = load_scene_file(filename)
    if width:
        camera.hsize = width
    if height:
        camera.vsize = height

    canvas = render(camera, world, num_processes=num_processes, show_progress=True)
    try:
        if output is None:
            output = sys.stdout
        else:
            output = open(output, "w")
        PPM.save(canvas, output)
    finally:
        if output is not None:
            if hasattr(output, "close"):
                output.close()


def cli():
    parser = argparse.ArgumentParser(
        prog="pytracer",
        description="Python raytracer. Renders YAML scene files to PPM images.",
    )
    parser.add_argument("filename")
    parser.add_argument(
        "-o",
        "--output",
        help="PPM image filename. If not specified, will output PPM data to stdout",
    )
    parser.add_argument(
        "-n",
        "--num-processes",
        help="Number of processes to use for rendering. Defaults to CPU count",
    )
    parser.add_argument(
        "--width", type=int, help="Image width in pixels. Overrides scene settings."
    )
    parser.add_argument(
        "--height", type=int, help="Image height in pixels. Overrides scene settings"
    )

    args = parser.parse_args()
    main(**args.__dict__)


if __name__ == "__main__":
    cli()
