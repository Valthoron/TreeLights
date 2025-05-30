import socket
import time

import board

from neopixel import NeoPixel

from configuration import load_configuration


def main():
    print("Hello.")

    # Load configuration
    configuration = load_configuration("map.yaml")

    # Initialize neopixel object
    pin = getattr(board, configuration["NeoPixel"]["Pin"])
    pixels = NeoPixel(pin, configuration["NeoPixel"]["LampCount"], auto_write=False, pixel_order=configuration["NeoPixel"]["PixelOrder"])
    pixels.fill([0, 0, 0])
    pixels.show()
    print("Pixels initialized.")

    # Create and bind socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(("0.0.0.0", configuration["LampDriver"]["Port"]))
    print("Socket open and bound.")

    # Start
    camera_address = (configuration["Camera"]["Ip"], configuration["Camera"]["Port"])
    ack_message = bytes([0xff])
    sleep_duration = configuration["LampDriver"]["Sleep"]

    print("Listening...")
    while True:
        try:
            # Get 2-byte lamp index
            buffer, _ = sock.recvfrom(2)
            i = buffer[0] | (buffer[1] << 8)

            # Illuminate only selected lamp
            pixels.fill([0, 0, 0])
            pixels[i] = [100, 100, 100]
            pixels.show()

            # Maybe NeoPixel isn't done sending, previous lamp is still illuminated, or this one isn't at full brightness yet
            # Tweak in map.yaml
            time.sleep(sleep_duration)

            # Sending acknowledge once is fine. Even if it gets lost, camera process keeps hammering until it receives the ack
            sock.sendto(ack_message, camera_address)

        except KeyboardInterrupt:
            break

        except TimeoutError:
            pass

    print("Goodbye.")


if __name__ == "__main__":
    main()
