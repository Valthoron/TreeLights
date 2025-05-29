import random

import numpy as np

from neopixel import NeoPixel

from animation import Animation
from lamps import Lamps

SHUFFLE_PERIOD = 0.5
FILTER_COEFFICIENT = 0.1


class Shuffle(Animation):
    next_shuffle: float

    def __init__(self):
        super().__init__()
        self.pixel_targets = np.array([])

    def initialize(self, lamps: Lamps):
        self.pixel_targets = np.tile(np.array([0.0, 0.0, 0.0]), (lamps.count, 1))
        self.next_shuffle = SHUFFLE_PERIOD

    def update(self, lamps: Lamps, pixels: NeoPixel, time: float, delta_time: float):
        # Shuffle
        self.next_shuffle -= delta_time
        if self.next_shuffle < 0.0:
            self.next_shuffle = SHUFFLE_PERIOD
            n = random.randrange(int(lamps.count * 0.2), int(lamps.count * 0.4))
            for i in random.choices(range(0, lamps.count), k=n):
                if random.randrange(0, 100) > 35:
                    self.pixel_targets[i] = np.random.rand(1, 3) * 50
                else:
                    self.pixel_targets[i] = (0, 0, 0)

        for i in range(0, lamps.count):
            c = np.array(pixels[i])
            pixels[i] = (c * (1.0 - FILTER_COEFFICIENT)) + (self.pixel_targets[i] * FILTER_COEFFICIENT)


def instantiate():
    return Shuffle()
