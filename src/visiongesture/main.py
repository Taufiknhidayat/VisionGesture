# src/visiongesture/main.py
import cv2

from configs.settings import (
    APP_NAME,
    MIRROR_CAMERA,
)

from src.visiongesture.camera.camera import Camera
from src.visiongesture.detector.hand_detector import HandDetector
from src.visiongesture.ui.fps import FPSCounter
from src.visiongesture.ui.overlay import Overlay


class VisionGestureApp:

    def __init__(self):
        self.camera = Camera()
        self.detector = HandDetector()
        self.fps_counter = FPSCounter()
        # Inisialisasi objek overlay baru
        self.overlay = Overlay()

    def run(self):

        while True:
            success, frame = self.camera.read()

            if not success:
                print("Camera Error")
                break

            # Mirror Camera
            if MIRROR_CAMERA:
                frame = cv2.flip(frame, 1)

            # Detect Hand
            frame, hands = self.detector.detect(frame)

            # Hitung performa FPS saat ini
            fps = self.fps_counter.get_fps()

            # Render seluruh komponen UI secara profesional dalam satu panggilan
            frame = self.overlay.draw(frame, hands, fps)

            # Tampilkan instruksi keluar yang minimalis di pojok bawah
            cv2.putText(
                frame,
                "Press 'Q' to Exit",
                (25, frame.shape[0] - 25),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                (180, 180, 180),
                1,
                cv2.LINE_AA
            )

            cv2.imshow(APP_NAME, frame)

            key = cv2.waitKey(1) & 0xFF
            if key == ord("q"):
                break

        self.camera.release()
        cv2.destroyAllWindows()


def main():
    app = VisionGestureApp()
    app.run()


if __name__ == "__main__":
    main()