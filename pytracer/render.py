import os
import sys
from concurrent.futures import ProcessPoolExecutor
from functools import partial
from typing import Callable

from pytracer import Camera, Canvas

# Set this env var to override default process count
NUM_PROCESS_ENV_VAR = "PYTRACER_NUM_PROCESSES"

_camera = None
_world = None


def render(camera: Camera, world, num_processes=None, show_progress=True) -> Canvas:
    if num_processes is None:
        if NUM_PROCESS_ENV_VAR in os.environ:
            num_processes = int(os.environ[NUM_PROCESS_ENV_VAR])
        else:
            num_processes = os.cpu_count()
    canvas = Canvas(camera.hsize, camera.vsize)
    CHUNKSIZE = 500

    tracking_function = get_tracking_function(show_progress)

    if num_processes == 1:
        init_worker(camera, world)
        for x, y, color in tracking_function(
            map(worker, generate_pixel_coords(canvas.height, canvas.width)),
            total=camera.hsize + camera.vsize,
            transient=True,
        ):
            canvas.write_pixel(x, y, color)
    else:

        with ProcessPoolExecutor(
            max_workers=num_processes, initializer=init_worker, initargs=(camera, world)
        ) as executor:
            for x, y, color in tracking_function(
                executor.map(
                    worker,
                    generate_pixel_coords(canvas.height, canvas.width),
                    chunksize=CHUNKSIZE,
                ),
                total=camera.hsize * camera.vsize,
                transient=True,
            ):
                canvas.write_pixel(x, y, color)

    return canvas


def worker(args):
    x, y = args
    color = _world.color_at(_camera.ray_for_pixel(x, y))
    return (x, y, color)


def init_worker(camera, world):
    global _camera
    global _world
    _camera = camera
    _world = world


def generate_pixel_coords(vsize, hsize):
    for y in range(vsize):
        for x in range(hsize):
            yield (x, y)


def _null_tracker(iter, **kwargs):
    yield from iter


def get_tracking_function(show_progress: bool) -> Callable:
    if show_progress is False:
        return _null_tracker

    try:
        from rich.console import Console
        from rich.progress import track

    except ImportError:
        print(
            "pytracer CLI dependencies missing. Did you install with -E cli ?",
            file=sys.stderr,
        )
        return _null_tracker

    return partial(track, console=Console(file=sys.stderr))
