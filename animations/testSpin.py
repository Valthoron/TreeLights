import numpy as np
import scipy as sp

import scipy.spatial

from animation import Animation


class TestSpin(Animation):
    def update(self, time: float, delta_time: float):
        r = scipy.spatial.transform.Rotation.from_euler("xyz", [time, 0, 0])
        v = r.apply([0, 0, 1])

        for i, lamp in enumerate(self.lamps):
            if np.dot(np.array(lamp) - [0, 0, 0.5], v) > 0:
                self.pixels[i] = (0, 25, 0)
            else:
                self.pixels[i] = (25, 0, 0)


def instantiate():
    return TestSpin()
