import random
import sys
import time

import board
import neopixel

from animation import Animation, load_animations
from lamps import load_lamps
from configuration import load_configuration


def main():
    print("Hello.")

    # Load configuration
    configuration = load_configuration("run.yaml")

    # Read lamp coordinates
    lamps = load_lamps("lamps.csv")
    print(f"{lamps.count} lamp coordinates loaded.")

    # Initialize neopixel object
    pin = getattr(board, configuration.pin)
    pixels = neopixel.NeoPixel(pin, lamps.count, auto_write=False, pixel_order=configuration.pixel_order)
    print("Pixels initialized.")

    # Load all animations in ./animations
    animations = load_animations()

    for _, animation in animations.items():
        animation.initialize(lamps)

    print(f"{len(animations.keys())} animation(s) loaded.")

    # Prepare playlist
    playlist = set(animations.keys())

    # Reject non-existing animations in the configuration
    unknown_animations = configuration.playlist.difference(playlist)

    if len(unknown_animations) > 0:
        print("Ignoring unknown animations in configuration:")
        for u in unknown_animations:
            print(f"x  {u}")

    if len(unknown_animations) == len(configuration.playlist):
        print("No animations specified in configuration, playing all loaded animations.")
    else:
        playlist = playlist.intersection(configuration.playlist)

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
                t_next_animation = t + configuration.animation_duration
                choice_set = playlist.difference(set([animation.name]))
                next_animation_name = random.choice(list(choice_set))
                animation = animations[next_animation_name]

            animation.update(lamps, pixels, t, dt)

            pixels.show()

        except KeyboardInterrupt:
            print("Goodbye.")
            sys.exit(0)


if __name__ == "__main__":
    main()
