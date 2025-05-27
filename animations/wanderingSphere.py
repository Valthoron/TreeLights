import random

import numpy as np

from animation import Animation
from tools import tools

NUM_SPHERES = 3
TARGET_THRESHOLD = 0.01
SPEED = 0.2


class WanderingSphere(Animation):
    positions: np.typing.NDArray
    targets: np.typing.NDArray

    def initialize(self):
        self.positions = np.tile(np.array([0.0, 0.0, 0.0]), (NUM_SPHERES, 1))
        self.targets = np.tile(np.array([0.0, 0.0, 0.0]), (NUM_SPHERES, 1))

    def update(self, time: float, delta_time: float):
        for i in range(0, NUM_SPHERES):
            delta = self.targets[i] - self.positions[i]
            delta_norm = tools.saturate(np.linalg.norm(delta), 0.001, 100.0)

            if delta_norm < (SPEED * delta_time):
                self.targets[i] = random.choice(self.lamps)

            velocity = SPEED * delta / delta_norm
            self.positions[i] += velocity * delta_time

        all_distances_r = np.sum(np.subtract(self.lamps, self.positions[0])**2, axis=-1)**0.5
        all_distances_g = np.sum(np.subtract(self.lamps, self.positions[1])**2, axis=-1)**0.5
        all_distances_b = np.sum(np.subtract(self.lamps, self.positions[2])**2, axis=-1)**0.5

        for i, _ in enumerate(self.lamps):
            r = 50 * (tools.saturate(1.0 - (all_distances_r[i] / 0.2), 0.0, 1.0))
            g = 50 * (tools.saturate(1.0 - (all_distances_g[i] / 0.2), 0.0, 1.0))
            b = 50 * (tools.saturate(1.0 - (all_distances_b[i] / 0.2), 0.0, 1.0))
            self.pixels[i] = (r, g, b)


def instantiate():
    return WanderingSphere()
