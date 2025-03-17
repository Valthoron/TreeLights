import time
import socket
import cv2

ANGLE = "315"
CAMERA_PORT = 0
HOST = "192.168.1.238"
PORT = 2593
SERVER = (HOST, PORT)

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(("0.0.0.0", PORT))
sock.settimeout(1.0)

print("*** Connecting to camera...")
camera = cv2.VideoCapture(CAMERA_PORT)
time.sleep(0.5)  # Need this, or else we get a black image
_ = camera.read()
time.sleep(0.25)
camera.set(cv2.CAP_PROP_FRAME_WIDTH, 4096)
camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 2160)
camera.set(cv2.CAP_PROP_AUTO_EXPOSURE, 0.25)
camera.set(cv2.CAP_PROP_EXPOSURE, 0.0)
time.sleep(0.25)

print("*** Capturing...")
for i in range(0, 498):
    message = bytes([(i & 0xff), ((i >> 8) & 0xff)])

    ok = 0
    while (ok == 0):
        try:
            sock.sendto(message, SERVER)
            sock.recvfrom(1)
            ok = 1
        except Exception as e:
            pass

    _, image = camera.read()
    filename = f"capture/{i}_{ANGLE}.jpg"
    cv2.imwrite(filename, image)

camera.release()
print("*** Finished.")