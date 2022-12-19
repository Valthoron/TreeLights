import time
import socket
import cv2

ANGLE = "315"
CAMERA_PORT = 0
HOST = "192.168.0.22"
PORT = 2593
SERVER = (HOST, PORT)

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(("0.0.0.0", PORT))
sock.settimeout(1.0)

camera = cv2.VideoCapture(CAMERA_PORT)
time.sleep(0.5)  # Need this, or else we get a black image

for i in range(0, 500):
    message = bytes([(i & 0xff), ((i >> 8) & 0xff)])
    sock.sendto(message, SERVER)
    sock.recvfrom(1)

    _, image = camera.read()
    filename = f"capture/{i}_{ANGLE}.jpg"
    cv2.imwrite(filename, image)

camera.release()
