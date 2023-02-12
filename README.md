# pytracer

Ray tracing in Python. My implementation of [The Ray Tracer Challenge](https://pragprog.com/titles/jbtracer/the-ray-tracer-challenge/) by [Jamis Buck](https://twitter.com/jamis).

![3d spheroid](examples/screenshots/sample.png)

## Examples

Examples assume [iTerm](https://iterm2.com/) with [imgcat](https://pypi.org/project/imgcat/) installed.

If imagecat is not installed, pipe output to a .ppm file instead of into imgcat, and open with macos Preview, or another program that supports PPM files (try [IrfanView](https://www.irfanview.com/)).

Before running examples, be sure to install the project:

```bash
$ poetry install
```

### Render a scene from a YAML file

```bash
pytracer examples/scene_reflection.yaml --width 1600 --height 800 |imgcat
```

![multiple reflective spheres example](examples/screenshots/reflection.png)

### Transparency

```bash
pytracer examples/transparency.yaml --width 1000 --height 500 | imgcat
```

![transparency example](examples/screenshots/transparency.png)

### World and Camera

```bash
$ poetry run python examples/world_and_camera.py | imgcat
```
![world and camera example](examples/screenshots/world_and_camera.png)

### Creating a PPM image from a pytracer Canvas

```bash
$ poetry run python examples/canvas_to_ppm.py | imgcat
```

![canvas to ppm example](examples/screenshots/canvas_to_ppm.png)


## Acknowledgements

* Ray Tracer Challenge book:<br><a href="https://pragprog.com/titles/jbtracer/the-ray-tracer-challenge/"><img src="https://pragprog.com/titles/jbtracer/the-ray-tracer-challenge/jbtracer_hu6d5b8b63a4954cb696e89b39f929331b_958829_500x0_resize_q75_box.jpg" width="200"></a>

* Color palette for sample image:<br><a href="https://www.colourlovers.com/palette/1930/cheer_up_emo_kid" target="_blank"><img src="https://www.colourlovers.com/images/badges/p/1/1930_cheer_up_emo_kid.png" style="width: 240px; height: 120px; border: 0 none;" alt="cheer_up_emo_kid" /></a>
