from __future__ import annotations
import numpy as np


class Animation():
    def __init__(self) -> Animation:
        self.num_lamps = 0
        self.lamps = np.array([])
        self.lamps_polar = np.array([])
        self.pixels = None

    def initialize(self):
        pass

    def update(self, time: float, delta_time: float):
        pass
