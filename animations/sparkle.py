import random

import numpy as np

from neopixel import NeoPixel

from animation import Animation
from lamps import Lamps


class Sparkle(Animation):
    new_flares = 0.0

    def initialize(self, lamps: Lamps):
        self.new_flares = 0.0

    def update(self, lamps: Lamps, pixels: NeoPixel, time: float, delta_time: float):
        # Update flare spawn rate
        self.new_flares += 60 * delta_time

        # Decay
        for i, _ in enumerate(lamps.coords):
            pr, pg, pb = pixels[i]
            r = int(0.9 * pr)
            g = int(0.9 * pg)
            b = int(0.9 * pb)
            pixels[i] = (r, g, b)

        # Paint flares
        nf_frac, nf_intg = np.modf(self.new_flares)
        self.new_flares = nf_frac
        for i in random.choices(range(0, lamps.count), k=int(nf_intg)):
            r = random.randrange(25, 50)
            g = random.randrange(25, 50)
            b = random.randrange(25, 50)
            pixels[i] = (r, g, b)


def instantiate():
    return Sparkle()
