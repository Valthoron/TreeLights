import csv
import os

import cv2
import matplotlib.pyplot as plt
import numpy as np

from scipy.optimize import curve_fit

SOURCE_DIR = "./capture"
OUT_DIR = "./processed"
DATA_FILE = "data.csv"

WRITE_OUT = False

IMAGE_W = 1920
IMAGE_H = 1080
IMAGE_W_CROPPED = 1450
IMAGE_H_CROPPED = 1080

NUM_LAMPS = 500
ANGLES = [0, 45, 90, 135, 180, 225, 270, 315]

adjust = {}
adjust[0] = {"y0": 504}
adjust[45] = {"y0": 539}
adjust[90] = {"y0": 552}
adjust[135] = {"y0": 554}
adjust[180] = {"y0": 548}
adjust[225] = {"y0": 548}
adjust[270] = {"y0": 550}
adjust[315] = {"y0": 549}

fitting_xdata = np.radians(ANGLES)

lamp_coordinates = []


def lamp_position(x, theta, radius):
    return radius * np.cos(theta + x)


# Process each lamp
for lamp in range(0, NUM_LAMPS):
    xn = []
    yn = []

    for angle in ANGLES:
        file_name = f"{lamp}_{angle}.jpg"

        # Open, crop and blur image for brightest spot detection
        image = cv2.imread(os.path.join(SOURCE_DIR, file_name))
        image_cropped = image[0:IMAGE_H_CROPPED, 0:IMAGE_W_CROPPED]
        image_cropped_gray = cv2.cvtColor(image_cropped, cv2.COLOR_BGR2GRAY)
        image_processed = cv2.GaussianBlur(image_cropped_gray, (15, 15), 0)

        # Find brightest spot
        (_, value, _, (x, y)) = cv2.minMaxLoc(image_processed)
        xn.append(IMAGE_W - x)  # Pixel x coordinate reversed
        yn.append(y - adjust[angle]["y0"])  # Pixel y coordinate moved to y0 origin

        if WRITE_OUT:
            cv2.circle(image, (x, y), 25, (0, 255, 0), 5)
            cv2.imwrite(os.path.join(OUT_DIR, file_name), image)

    fitting_ydata = np.array(yn, dtype=np.float64)

    popt, pcov = curve_fit(lamp_position, fitting_xdata, fitting_ydata, bounds=([0.0, 0.0], [2.0 * np.pi, 1000.0]))
    (theta, radius) = popt
    x = radius * np.cos(theta)
    y = radius * np.sin(theta)
    z = np.average(xn)

    lamp_coordinates.append((x, y, z))

    # plt.plot(fitting_xdata, fitting_ydata, 'b-', label='data')
    # plt.plot(fitting_xdata, lamp_position(fitting_xdata, *popt), 'r-', label='fit: theta=%5.3f, radius=%5.3f' % tuple(popt))
    # plt.xlabel('x')
    # plt.ylabel('y')
    # plt.legend()
    # plt.show()

    print(lamp)

# Split coordinates into numpy arrays, sorting by lamp name/number
xs = np.array([lamp[0] for lamp in lamp_coordinates])
ys = np.array([lamp[1] for lamp in lamp_coordinates])
zs = np.array([lamp[2] for lamp in lamp_coordinates])


# Scale and offset so that:
# Tree height is 1
# Aspect ratio is preserved
# X and Y origins are the average of each axis respectively
# Z origin is bottom
scale = np.ptp(zs)
xs /= scale
ys /= scale
zs /= scale
xs -= np.average(xs)
ys -= np.average(ys)
zs -= np.min(zs)

# Write coordinates to file
with open(DATA_FILE, "w", newline="") as file_handle:
    writer = csv.writer(file_handle)
    for coordinates in zip(xs, ys, zs):
        writer.writerow(coordinates)

# Plot
fig, ax = plt.subplots(subplot_kw={"projection": "3d"})
ax.scatter(xs, ys, zs)
ax.set_box_aspect((np.ptp(xs), np.ptp(ys), np.ptp(zs)))
plt.show()
