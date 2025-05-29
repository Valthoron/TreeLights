import random
import sys
import time

import board
import neopixel
import yaml

from animation import Animation, load_animations
from lamps import load_lamps


def main():
    print("Hello.")

    # Read lamp coordinates
    lamps = load_lamps("lamps.csv")
    print(f"{lamps.count} lamp coordinates loaded.")

    # Initialize neopixel object
    pixels = neopixel.NeoPixel(board.D12, lamps.count, auto_write=False, pixel_order=neopixel.RGB)
    print("Pixels initialized.")

    # Load all animations in ./animations
    animations = load_animations()

    for _, animation in animations.items():
        animation.initialize(lamps)

    print(f"{len(animations.keys())} animation(s) loaded.")

    # Load configuration
    animation_duration = 60
    animation_list = animations.keys()

    with open("run.yaml", "r", encoding="utf-8") as config_file_stream:
        config = yaml.safe_load(config_file_stream)
        animation_duration = config["Duration"]

        loaded_animations_set = set(animations.keys())
        config_animations_set = set(config["Animations"])

        animations_set = list(config_animations_set.intersection(loaded_animations_set))
        animations_unknown_set = config_animations_set.difference(loaded_animations_set)

        if len(animations_unknown_set) > 0:
            print("Ignoring unknown animations in configuration:")
            print(animations_unknown_set)

        if len(animations_set) > 0:
            animation_list = list(animations_set)
        else:
            print("No animations specified in configuration, playing all loaded animations.")

    # Animate
    animation: Animation
    t_start = time.time()
    t = 0.0
    t_prev = 0.0
    t_next_animation = 0.0

    while True:
        try:
            t_prev = t
            t = time.time() - t_start
            dt = t - t_prev

            if t > t_next_animation:
                # Pick a new animation that is not the current animation
                t_next_animation = t + animation_duration
                choice_set = set(animation_list).difference(set([animation.name]))
                next_animation_name = random.choice(list(choice_set))
                animation = animations[next_animation_name]

            animation.update(lamps, pixels, t, dt)

            pixels.show()

        except KeyboardInterrupt:
            print("Goodbye.")
            sys.exit(0)


if __name__ == "__main__":
    main()
