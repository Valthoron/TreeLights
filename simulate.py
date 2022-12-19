import csv
import importlib
import os
import sys
import time

import matplotlib.pyplot as plot
import numpy as np

animations = {}


def files_in(path):
    for name in os.listdir(path):
        if os.path.isfile(os.path.join(path, name)):
            yield name


def load_animation(name: str) -> None:
    full_name = f"animations.{name}"
    resolved_name = importlib.util.resolve_name(full_name, None)
    spec = importlib.util.find_spec(resolved_name)
    lib = importlib.util.module_from_spec(spec)
    sys.modules[resolved_name] = lib
    spec.loader.exec_module(lib)

    instantiate = getattr(lib, 'instantiate')
    return instantiate()


# Load all animations in ./animations
for file_name in files_in("animations"):
    if not file_name.endswith(".py"):
        continue

    name = file_name.replace(".py", "")
    animations[name] = load_animation(name)

# Load lamp data
data_file_name = "data.csv"

lamps = []

# Read coordinates
with open(data_file_name, "r", newline="") as file_handle:
    reader = csv.reader(file_handle)
    for row in reader:
        lamps.append(np.array(np.double(row)))

lamps = np.array(lamps)
colors = np.full([lamps.shape[0], 3], np.array([1.0, 1.0, 1.0]), dtype=np.ndarray)

# Plot
xs = lamps[:, 0]
ys = lamps[:, 1]
zs = lamps[:, 2]

figure = plot.figure()
figure.set_facecolor((0, 0, 0))

axes = figure.add_subplot(projection="3d")
axes.set_box_aspect((np.ptp(xs), np.ptp(ys), np.ptp(zs)))
axes.set_facecolor((0, 0, 0))
axes.xaxis.pane.fill = False
axes.yaxis.pane.fill = False
axes.grid(False)

figure.tight_layout(pad=0.0)

points = axes.scatter(xs, ys, zs, s=50, c=colors)

plot.show(block=False)

# Load animation
anim = animations["wanderingSphere"]

# Animate
t_start = time.time()
t = 0.0
t_prev = 0.0

while True:
    t_prev = t
    t = time.time() - t_start
    dt = t - t_prev

    anim.update(t, dt, lamps, colors)

    points.set_facecolors(colors)
    plot.pause(1.0 / 60.0)

    if not plot.fignum_exists(figure.number):
        break
