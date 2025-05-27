import random

import numpy as np
import scipy as sp

from animation import Animation
from tools import tools

SHUFFLE_PERIOD = 0.5
FILTER_COEFFICIENT = 0.1

class Shuffle(Animation):
    def initialize(self):
        self.pixel_targets = np.tile(np.array([0.0, 0.0, 0.0]), (self.num_lamps, 1))
        self.next_shuffle = SHUFFLE_PERIOD

    def update(self, time: float, delta_time: float):
        # Shuffle
        self.next_shuffle -= delta_time
        if (self.next_shuffle < 0.0):
            self.next_shuffle = SHUFFLE_PERIOD
            n = random.randrange(int(self.num_lamps * 0.2), int(self.num_lamps * 0.4))
            for i in random.choices(range(0, self.num_lamps), k=n):
                if (random.randrange(0, 100) > 35):
                    self.pixel_targets[i] = np.random.rand(1, 3) * 50
                else:
                    self.pixel_targets[i] = (0, 0, 0)
        
        for i in range(0, self.num_lamps):
            c = np.array(self.pixels[i])
            self.pixels[i] = (c * (1.0 - FILTER_COEFFICIENT)) + (self.pixel_targets[i] * FILTER_COEFFICIENT)


def instantiate():
    return Shuffle()
