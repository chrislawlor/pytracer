import argparse
import sys

from pytracer import PPM, Canvas, Color, Point, Vector3

DEFAULT_TRACER_COLOR = Color.from_rgb(243, 134, 48)


class Tracer:
    def __init__(
        self,
        velocity: Vector3,
        initial_position: Point = Point(0, 0, 0),
        color: Color = Color(1, 1, 1),
    ):
        """
        Parameters:
            velocity (Vector3): Velocity in meters per second.
            initial_position (Point): Starting position.
        """
        self.position = initial_position
        self.velocity = velocity
        self.color = color


class Environment:
    gravity = 9.80665  # m/s²

    def __init__(self, wind: Vector3 = Vector3(0, 0, 0)):
        self.gravity_vector = Vector3(0, -self.gravity, 0)
        self.wind_vector = wind


class Run:
    tick_seconds = 0.1

    def __init__(self, tracer: Tracer, env: Environment):
        self.tracers = [tracer]
        self.gravity_vector = Vector3(0, -env.gravity, 0) * self.tick_seconds
        self.wind_vector = env.wind_vector
        # Record tracer positions to put on the canvas later
        self.tracer_coords: list[tuple[float, float]] = []

    def tick(self):
        for tracer in self.tracers:
            if tracer.position.y > 0 or tracer.velocity.y > 0:
                self.update_tracer(tracer)
                self.tracer_coords.append((tracer.position.x, tracer.position.y))

    def update_tracer(self, tracer: Tracer):
        tracer.position = tracer.position + tracer.velocity
        tracer.velocity = tracer.velocity + self.gravity_vector + self.wind_vector
        if tracer.position.y < 0:
            tracer.position = Point(tracer.position.x, 0, 0)

    def to_canvas(self, canvas: Canvas, scale_width: int, scale_height: int) -> None:
        y_meters_per_pixel = scale_height / canvas.height
        x_meters_per_pixel = scale_width / canvas.width

        for x_m, y_m in self.tracer_coords:
            # invert y coords
            y_inv = scale_height - y_m
            y_scaled = round(y_inv / y_meters_per_pixel)
            x_scaled = round(x_m / x_meters_per_pixel)
            self.fill_canvas_at_point(canvas, x_scaled, y_scaled)

    def fill_canvas_at_point(
        self, canvas: Canvas, x: int, y: int, color: Color = DEFAULT_TRACER_COLOR
    ):
        # we add a 9x9 square centered around the point
        for y in range(y - 1, y + 1, 1):
            for x in range(x - 1, x + 1, 1):
                if x > 0 and x < canvas.width - 1 and y > 0 and y < canvas.height - 1:
                    canvas.write_pixel(x, y, color)


def run_simulation(
    output: str,
    x_velocity,
    y_velocity,
    wind,
    width: int,
    height: int,
    scale_width: int,
    scale_height: int,
):
    tracer = Tracer(velocity=Vector3(x_velocity, y_velocity, 0))
    env = Environment(wind=Vector3(wind, 0, 0))
    run = Run(tracer=tracer, env=env)

    RUN_SECONDS = 9
    RUN_TICKS = RUN_SECONDS / run.tick_seconds

    for tick in range(int(RUN_TICKS)):
        time = tick * run.tick_seconds
        run.tick()
        if output == "text":
            print(f"time={time:0.1f}\tX: {tracer.position.x}\tY: {tracer.position.y}")
    if output == "image":
        canvas = Canvas(width, height)
        run.to_canvas(canvas, scale_width=scale_width, scale_height=scale_height)
        PPM.save(canvas, sys.stdout)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-x", "--x-velocity", type=int, default=30)
    parser.add_argument("-y", "--y-velocity", type=int, default=40)
    parser.add_argument("--wind", type=float, default=-0.3)
    parser.add_argument("-o", "--output", default="image", choices=["image", "text"])
    parser.add_argument("-w", "--width", default=600, type=int)
    parser.add_argument("--height", default=400, type=int)
    parser.add_argument("--scale-width", default=1800, type=int)
    parser.add_argument("--scale-height", default=1200, type=int)
    args = parser.parse_args()
    run_simulation(**args.__dict__)
