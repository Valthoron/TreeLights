import numpy as np
import scipy as sp

from animation import Animation


class TestSpin(Animation):
    def __init__(self) -> Animation:
        super().__init__()

    def update(self, time: float, delta_time: float, lamps: np.ndarray, colors: np.ndarray):
        r = sp.spatial.transform.Rotation.from_euler("xyz", [time, 0, 0])
        v = r.apply([0, 0, 1])

        for i, lamp in enumerate(lamps):
            if np.dot(lamp - [0, 0, 0.5], v) > 0:
                colors[i] = [0, 1, 0]
            else:
                colors[i] = [1, 0, 0]


def instantiate():
    return TestSpin()
