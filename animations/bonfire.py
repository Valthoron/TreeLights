import random

import numpy as np

from neopixel import NeoPixel

from animation import Animation
from lamps import Lamps


class Bonfire(Animation):
    lamps_polar_sorted: list
    next_randomize: float
    new_flares: float
    c0: float
    c1: float
    c2: float
    c3: float
    c0_t: float
    c1_t: float
    c2_t: float
    c3_t: float

    def initialize(self, lamps: Lamps):
        lamps_polar = np.copy(lamps.coords_polar)
        indices = np.reshape(np.array(range(0, lamps.count)), (lamps.count, 1))
        lamps_polar = np.concatenate((lamps_polar, indices), axis=1)
        self.lamps_polar_sorted = sorted(lamps_polar, key=lambda p: p[2])

        self.new_flares = 0.0
        self.next_randomize = random.uniform(0.15, 0.3)

        self.randomize_coefficient_targets()
        self.c0 = self.c0_t
        self.c1 = self.c1_t
        self.c2 = self.c2_t
        self.c3 = self.c3_t

    def randomize_coefficient_targets(self):
        self.c0_t = random.uniform(0.3, 0.6)
        self.c1_t = random.uniform(-0.2, 0.2)
        self.c2_t = random.uniform(-0.2, 0.2)
        self.c3_t = random.uniform(-0.3, 0.3)

    def update(self, lamps: Lamps, pixels: NeoPixel, time: float, delta_time: float):
        # Update fire line coefficients
        self.next_randomize -= delta_time

        if self.next_randomize <= 0.0:
            self.randomize_coefficient_targets()

        self.c0 = 0.5 * self.c0_t + 0.5 * self.c0
        self.c1 = 0.5 * self.c1_t + 0.5 * self.c1
        self.c2 = 0.5 * self.c2_t + 0.5 * self.c2
        self.c3 = 0.5 * self.c3_t + 0.5 * self.c3

        # Update flare spawn rate
        self.new_flares += 35 * delta_time

        # Paint fire line
        for _, lamp in enumerate(self.lamps_polar_sorted):
            i = int(lamp[3])
            z = self.c0 + self.c1 * np.sin(1.0 * lamp[0]) + self.c2 * np.sin(2.0 * lamp[0]) + self.c3 * np.sin(3.0 * lamp[0])

            if lamp[2] < z:
                r = 50
                g = int(25 - (20 * (z - lamp[2])))
                b = 5
                pixels[i] = (r, g, b)
            else:
                pr, pg, pb = pixels[i]
                r = int(0.6 * pr)
                g = int(0.3 * pg)
                b = int(0.2 * pb)
                pixels[i] = (r, g, b)

        # Paint flares
        nf_frac, nf_intg = np.modf(self.new_flares)
        self.new_flares = nf_frac
        for lamp in random.choices(self.lamps_polar_sorted, k=int(nf_intg)):
            i = int(lamp[3])
            pixels[i] = (50, 20, 20)


def instantiate():
    return Bonfire()
