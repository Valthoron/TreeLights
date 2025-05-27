import random
import csv
import importlib.util
import os
import sys
import time

import board
import neopixel
import numpy as np

from animation import Animation

def files_in(path):
    for name in os.listdir(path):
        if os.path.isfile(os.path.join(path, name)):
            yield name

def load_animation(name: str) -> Animation:
    full_name = f"animations.{name}"
    resolved_name = importlib.util.resolve_name(full_name, None)
    spec = importlib.util.find_spec(resolved_name)
    lib = importlib.util.module_from_spec(spec)
    sys.modules[resolved_name] = lib
    spec.loader.exec_module(lib)

    instantiate = getattr(lib, 'instantiate')
    return instantiate()

print("Hello.")

# Initialize neopixel object
pixels = neopixel.NeoPixel(board.D12, 498, auto_write=False, pixel_order=neopixel.RGB)
print("Pixels initialized.")

# Read lamp coordinates
data_file_name = "data.csv"
lamps = []
lamps_polar = []

with open(data_file_name, "r", newline="") as file_handle:
    reader = csv.reader(file_handle)
    for row in reader:
        x = float(row[0])
        y = float(row[1])
        z = float(row[2])
        t = np.arctan2(y, x)
        r = np.sqrt(x**2 + y**2)
        lamps.append((x, y, z))
        lamps_polar.append((t, r, z))

lamps = np.array(lamps)
lamps_polar = np.array(lamps_polar)
print("Lamp coordinates loaded.")

# Load all animations in ./animations
animations = {}

for file_name in files_in("animations"):
    if not file_name.endswith(".py"):
        continue

    name = file_name.replace(".py", "")

    animation = load_animation(name)
    animation.num_lamps = len(lamps)
    animation.lamps = lamps
    animation.lamps_polar = lamps_polar
    animation.pixels = pixels
    animation.initialize()

    animations[name] = animation
    print(f">\t{name}")

print(f"{len(animations.keys())} animation(s) loaded.")

# Animation loop
animation_list = [
    "barberPole",
    "bonfire",
    "colorPlane",
    "matrix",
    "sparkle",
    "wanderingSphere",
    "shuffle"
]

do_animation_loop = False

# Load specified animation
if not len(sys.argv) > 1:
    do_animation_loop = True
    animation_name = ""
    print(f"Running preselected animations...")
else:
    animation_name = sys.argv[1]

    if animation_name not in animations:
        print(f"Animation named \"{animation_name}\" not found.")
        exit()

    animation = animations[animation_name]
    print(f"Running animation \"{animation_name}\"...")

# Animate
t_start = time.time()
t = 0.0
t_prev = 0.0
t_next_animation = 0.0

while True:
    try:
        t_prev = t
        t = time.time() - t_start
        dt = t - t_prev

        if do_animation_loop:
            if t > t_next_animation:
                t_next_animation = t + 60.0
                choice_set = set(animation_list).difference(set([animation_name]))
                animation_name = random.choice(list(choice_set))
                animation = animations[animation_name]

        animation.update(t, dt)

        pixels.show()

    except KeyboardInterrupt:
        print("Goodbye.")
        exit()
