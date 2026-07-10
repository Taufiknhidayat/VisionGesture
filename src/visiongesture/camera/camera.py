import cv2

from configs.settings import CAMERA_INDEX, FRAME_WIDTH, FRAME_HEIGHT


class Camera:

    def __init__(self):

        self.cap = cv2.VideoCapture(CAMERA_INDEX)

        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, FRAME_WIDTH)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, FRAME_HEIGHT)

        if not self.cap.isOpened():
            raise RuntimeError("Camera tidak ditemukan!")

    def read(self):
        return self.cap.read()

    def release(self):
        self.cap.release()