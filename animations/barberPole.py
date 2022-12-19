import numpy as np

from animation import Animation


class BarberPole(Animation):
    def __init__(self) -> Animation:
        super().__init__()
        self.angle = 0.0

    def update(self, time: float, delta_time: float, lamps: np.ndarray, colors: np.ndarray):
        self.angle += 30 * delta_time

        for i, lamp in enumerate(lamps):
            lamp_azimuth = np.rad2deg(np.arctan2(lamp[1], lamp[0])) + self.angle + (90.0 * lamp[2])
            lamp_mode = np.mod(lamp_azimuth, 90.0) / 90.0
            d = 0.0 if lamp_mode < 0.5 else 1.0
            r = 1.0
            g = d
            b = d
            colors[i] = np.array([r, g, b]) * 0.7


def instantiate():
    return BarberPole()
