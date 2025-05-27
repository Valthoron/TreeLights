import numpy as np
import neopixel


class Animation():
    num_lamps = 0
    lamps = np.array([])
    lamps_polar = np.array([])
    pixels: neopixel.NeoPixel

    def initialize(self):
        pass

    def update(self, time: float, delta_time: float):
        pass
