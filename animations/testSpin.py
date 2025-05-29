import numpy as np
import scipy.spatial

from neopixel import NeoPixel

from animation import Animation
from lamps import Lamps


class TestSpin(Animation):
    def update(self, lamps: Lamps, pixels: NeoPixel, time: float, delta_time: float):
        r = scipy.spatial.transform.Rotation.from_euler("xyz", [time, 0, 0])
        v = r.apply([0, 0, 1])

        for i, lamp in enumerate(lamps.coords):
            if np.dot(np.array(lamp) - [0, 0, 0.5], v) > 0:
                pixels[i] = (0, 25, 0)
            else:
                pixels[i] = (25, 0, 0)


def instantiate():
    return TestSpin()
