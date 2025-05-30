import socket
import sys
import time

import board

from neopixel import NeoPixel

from configuration import load_configuration


def main():
    print("Hello.")

    # Load configuration
    configuration = load_configuration("map.yaml")

    # Initialize neopixel object
    pin = getattr(board, configuration["Pin"])
    pixels = NeoPixel(pin, configuration["LampCount"], auto_write=False, pixel_order=configuration["PixelOrder"])
    pixels.fill([0, 0, 0])
    pixels.show()
    print("Pixels initialized.")

    # Create and bind socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(("0.0.0.0", configuration["LampDriverPort"]))
    print("Socket open and bound.")

    # Start
    camera_address = (configuration["CameraIp"], configuration["CameraPort"])
    ack_message = bytes([0xff])

    print("Listening...")
    while True:
        try:
            buffer, _ = sock.recvfrom(2)
            i = buffer[0] | (buffer[1] << 8)

            pixels.fill([0, 0, 0])
            pixels[i] = [100, 100, 100]
            pixels.show()

            time.sleep(0.05)  # 100 ms
            # 174-175

            sock.sendto(ack_message, camera_address)

        except KeyboardInterrupt:
            print("Goodbye.")
            sys.exit(0)

        except TimeoutError:
            pass


if __name__ == "__main__":
    main()
