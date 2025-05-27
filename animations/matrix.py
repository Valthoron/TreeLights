import random

import numpy as np

from animation import Animation
from tools import tools

NUM_CURSORS = 6
FALL_SPEED = 0.5
CURSOR_SIZE = 0.04


class Matrix(Animation):
    cursor_azimuth = [0.0] * NUM_CURSORS
    cursor_height = [0.0] * NUM_CURSORS
    cursor_position = np.tile(np.array([0.0, 0.0, 0.0]), (NUM_CURSORS, 1))

    def update(self, time: float, delta_time: float):
        for i in range(0, NUM_CURSORS):
            if self.cursor_height[i] <= 0.0:
                self.cursor_azimuth[i] = random.uniform(0.0, 360.0)
                self.cursor_height[i] = random.uniform(0.5, 1.2)

            self.cursor_height[i] -= FALL_SPEED * delta_time
            cursor_radius = 0.3 * tools.saturate(1.0 - self.cursor_height[i], 0.0, 1.0)

            self.cursor_position[i][0] = cursor_radius * np.cos(self.cursor_azimuth[i])
            self.cursor_position[i][1] = cursor_radius * np.sin(self.cursor_azimuth[i])
            self.cursor_position[i][2] = self.cursor_height[i]

        all_distances = [np.sum(np.subtract(self.lamps, self.cursor_position[i])**2, axis=-1)**0.5 for i in range(0, NUM_CURSORS)]
        all_distances = np.min(all_distances, axis=-2)

        for i, _ in enumerate(self.lamps):
            if all_distances[i] < CURSOR_SIZE:
                self.pixels[i] = (40, 40, 40)
            else:
                pr, pg, pb = self.pixels[i]
                r = int(0.3 * pr)
                g = int(0.96 * pg)
                b = int(0.3 * pb)
                self.pixels[i] = (r, g, b)


def instantiate():
    return Matrix()
