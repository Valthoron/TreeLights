import socket
import sys
import time

import cv2

from configuration import load_configuration


def print_usage():
    print("Usage: map_capture_camera.py <angle>")
    print("\tangle: Tree rotation angle for which the images will be captured.")


def main():
    if len(sys.argv) != 2:
        print_usage()
        sys.exit()

    try:
        angle = int(sys.argv[1])
    except ValueError:
        print_usage()
        sys.exit()

    print("Hello.")

    # Load configuration
    configuration = load_configuration("map.yaml")

    # Create and bind socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(("0.0.0.0", configuration["CameraPort"]))
    sock.settimeout(1.0)
    print("Socket open and bound.")

    # Initialize camera
    camera = cv2.VideoCapture(configuration["CameraIndex"])
    time.sleep(0.5)  # Need this, or else we get a black image
    _ = camera.read()
    time.sleep(0.25)
    # camera.set(cv2.CAP_PROP_FRAME_WIDTH, 4096)
    # camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 2160)
    camera.set(cv2.CAP_PROP_AUTO_EXPOSURE, 0.25)
    camera.set(cv2.CAP_PROP_EXPOSURE, 0.0)
    time.sleep(0.25)
    print("Camera open.")

    # Start
    print("Capturing...")
    driver_address = (configuration["LampDriverIp"], configuration["LampDriverPort"])

    for i in range(0, configuration["LampCount"]):
        lamp_message = bytes([(i & 0xff), ((i >> 8) & 0xff)])

        ok = 0
        while (ok == 0):
            try:
                sock.sendto(lamp_message, driver_address)
                sock.recvfrom(1)
                ok = 1
            except TimeoutError:
                pass

        _, image = camera.read()
        file_name = f"capture/{i}_{angle}.jpg"
        cv2.imwrite(file_name, image)

    camera.release()
    print("Finished.")


if __name__ == "__main__":
    main()
