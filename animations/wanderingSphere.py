import random

import numpy as np
import scipy as sp

from animation import Animation

NUM_SPHERES = 3
TARGET_THRESHOLD = 0.01
SPEED = 0.4


class WanderingSphere(Animation):
    def __init__(self) -> Animation:
        super().__init__()
        self.positions = np.tile(np.array([0.0, 0.0, 0.0]), (NUM_SPHERES, 1))
        self.targets = np.tile(np.array([0.0, 0.0, 0.0]), (NUM_SPHERES, 1))

    def update(self, time: float, delta_time: float, lamps: np.ndarray, colors: np.ndarray):
        for i in range(0, NUM_SPHERES):
            if np.linalg.norm(self.targets[i] - self.positions[i]) < TARGET_THRESHOLD:
                self.targets[i] = random.choice(lamps)

            delta = self.targets[i] - self.positions[i]
            delta_norm = np.clip(np.linalg.norm(delta), 0.001, np.inf)
            velocity = SPEED * delta / delta_norm
            self.positions[i] += velocity * delta_time

        for i, lamp in enumerate(lamps):
            distance_r = 3.0 * np.linalg.norm(lamp - self.positions[0]) - 0.3
            distance_g = 3.0 * np.linalg.norm(lamp - self.positions[1]) - 0.3
            distance_b = 3.0 * np.linalg.norm(lamp - self.positions[2]) - 0.3
            r = 1.0 - np.clip(distance_r, 0.0, 1.0)
            g = 1.0 - np.clip(distance_g, 0.0, 1.0)
            b = 1.0 - np.clip(distance_b, 0.0, 1.0)
            colors[i] = [r, g, b]


def instantiate():
    return WanderingSphere()
