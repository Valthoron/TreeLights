import numpy as np

from neopixel import NeoPixel

from animation import Animation
from lamps import Lamps


class BarberPole(Animation):
    angle: float

    def initialize(self, lamps: Lamps):
        self.angle = 0.0

    def update(self, lamps: Lamps, pixels: NeoPixel, time: float, delta_time: float):
        self.angle += np.mod(50 * delta_time, 360.0)

        for i, lamp in enumerate(lamps.coords_polar):
            azimuth = np.rad2deg(lamp[0]) + self.angle + (180.0 * lamp[2])
            azimuth = np.mod(azimuth, 360.0)
            frac, intg = np.modf(azimuth / 90.0)

            # https://www.desmos.com/calculator/whyb9zmxxc
            d = 1.0 - ((np.abs(frac - 0.5) - 0.1) / 0.15)
            d = np.clip(d, 0.0, 1.0)

            if intg == 0:
                pixels[i] = (50 * d, 0, 0)
            elif intg == 1:
                pixels[i] = (0, 50 * d, 0)
            elif intg == 2:
                pixels[i] = (0, 0, 50 * d)
            else:
                pixels[i] = (30 * d, 30 * d, 0)


def instantiate():
    return BarberPole()
