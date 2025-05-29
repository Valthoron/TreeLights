import csv

import numpy as np


class Lamps:
    count: int
    coords: np.typing.NDArray
    coords_polar: np.typing.NDArray


def load_lamps(csv_file_name: str) -> Lamps:
    coords = []
    coords_polar = []

    with open(csv_file_name, "r", newline="", encoding="utf-8") as file_stream:
        reader = csv.reader(file_stream)
        for row in reader:
            x = float(row[0])
            y = float(row[1])
            z = float(row[2])
            t = np.arctan2(y, x)
            r = np.sqrt(x**2 + y**2)
            coords.append((x, y, z))
            coords_polar.append((t, r, z))

    lamps = Lamps()
    lamps.count = len(coords)
    lamps.coords = np.array(coords)
    lamps.coords_polar = np.array(coords_polar)
    return lamps
