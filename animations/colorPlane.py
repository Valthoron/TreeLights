import numpy as np

from neopixel import NeoPixel

from animation import Animation
from lamps import Lamps


class TestPlane(Animation):
    def update(self, lamps: Lamps, pixels: NeoPixel, time: float, delta_time: float):
        zp = 0.35 * np.sin(time / 2.0)

        r = int(75 * (0.5 + 0.5 * np.sin(time / 4.0)))
        g = int(75 * (0.5 + 0.5 * np.sin(time / 5.0)))
        b = int(75 * (0.5 + 0.5 * np.sin(time / 6.0)))

        a_s = np.sin(time / 7.0)
        a_c = np.cos(time / 7.0)
        b_s = np.sin(time / 8.0)
        b_c = np.sin(time / 8.0)

        for i, lamp in enumerate(lamps.coords):
            z = (lamp[0] * a_s) + (lamp[1] * b_s) + (lamp[2] * a_c * b_c)
            d = np.abs(z - zp)
            if d < 0.1:
                k = (0.1 - d) / 0.1
                pixels[i] = (r * k, g * k, b * k)
            else:
                pixels[i] = (0, 0, 0)


def instantiate():
    return TestPlane()
