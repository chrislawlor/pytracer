import os
from concurrent.futures import ProcessPoolExecutor

from pytracer import Camera, Canvas

# Set this env var to override default process count
NUM_PROCESS_ENV_VAR = "PYTRACER_NUM_PROCESSES"

_camera = None
_world = None


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


def render(camera: Camera, world, num_processes=None) -> Canvas:
    if num_processes is None:
        if NUM_PROCESS_ENV_VAR in os.environ:
            num_processes = int(os.environ[NUM_PROCESS_ENV_VAR])
        else:
            num_processes = os.cpu_count()
    canvas = Canvas(camera.hsize, camera.vsize)
    CHUNKSIZE = 500

    with ProcessPoolExecutor(
        max_workers=num_processes, initializer=init_worker, initargs=(camera, world)
    ) as executor:
        for x, y, color in executor.map(
            worker,
            generate_pixel_coords(canvas.height, canvas.width),
            chunksize=CHUNKSIZE,
        ):
            canvas.write_pixel(x, y, color)

    return canvas
    return canvas
