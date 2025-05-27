import numpy as np
import scipy as sp

import scipy.spatial

from animation import Animation


class TestPlane(Animation):
    def update(self, time: float, delta_time: float):
        zp = 0.35 * np.sin(time / 2.0)

        r = int(75 * (0.5 + 0.5 * np.sin(time / 4.0)))
        g = int(75 * (0.5 + 0.5 * np.sin(time / 5.0)))
        b = int(75 * (0.5 + 0.5 * np.sin(time / 6.0)))

        a_s = np.sin(time / 7.0)
        a_c = np.cos(time / 7.0)
        b_s = np.sin(time / 8.0)
        b_c = np.sin(time / 8.0)

        for i, lamp in enumerate(self.lamps):
            z = (lamp[0] * a_s) + (lamp[1] * b_s) + (lamp[2] * a_c * b_c)
            d = np.abs(z - zp)
            if d < 0.1:
                k = (0.1 - d) / 0.1
                self.pixels[i] = (r * k, g * k, b * k)
            else:
                self.pixels[i] = (0, 0, 0)


def instantiate():
    return TestPlane()
