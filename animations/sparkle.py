import random

import numpy as np
import scipy as sp

from animation import Animation
from tools import tools


class Sparkle(Animation):
    def initialize(self):
        self.new_flares = 0.0

    def update(self, time: float, delta_time: float):
        # Update flare spawn rate
        self.new_flares += 60 * delta_time

        # Decay
        for i, lamp in enumerate(self.lamps):
            pr, pg, pb = self.pixels[i]
            r = int(0.9 * pr)
            g = int(0.9 * pg)
            b = int(0.9 * pb)
            self.pixels[i] = (r, g, b)

        # Paint flares
        nf_frac, nf_intg = np.modf(self.new_flares)
        self.new_flares = nf_frac
        for i in random.choices(range(0, len(self.lamps)), k=int(nf_intg)):
            r = random.randrange(25, 50)
            g = random.randrange(25, 50)
            b = random.randrange(25, 50)
            self.pixels[i] = (r, g, b)


def instantiate():
    return Sparkle()
