import numpy as np

from neopixel import NeoPixel

from animation import Animation
from lamps import Lamps


class TestPlane(Animation):
    def update(self, lamps: Lamps, pixels: NeoPixel, time: float, delta_time: float):
        a = 0.5 + 0.5 * np.sin(time / 2.0)
        r = int(25 * (0.5 + 0.5 * np.sin(time / 4.0)))
        g = int(25 * (0.5 + 0.5 * np.sin(time / 5.0)))
        b = int(25 * (0.5 + 0.5 * np.sin(time / 6.0)))

        for i, lamp in enumerate(lamps.coords):
            d = np.abs(lamp[2] - a)
            if d < 0.05:
                pixels[i] = (r, g, b)
            else:
                pixels[i] = (0, 0, 0)


def instantiate():
    return TestPlane()
