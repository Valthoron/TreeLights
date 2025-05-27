import numpy as np

from animation import Animation


class TestPlane(Animation):
    def update(self, time: float, delta_time: float):
        a = 0.5 + 0.5 * np.sin(time / 2.0)
        r = int(25 * (0.5 + 0.5 * np.sin(time / 4.0)))
        g = int(25 * (0.5 + 0.5 * np.sin(time / 5.0)))
        b = int(25 * (0.5 + 0.5 * np.sin(time / 6.0)))

        for i, lamp in enumerate(self.lamps):
            d = np.abs(lamp[2] - a)
            if d < 0.05:
                self.pixels[i] = (r, g, b)
            else:
                self.pixels[i] = (0, 0, 0)


def instantiate():
    return TestPlane()
