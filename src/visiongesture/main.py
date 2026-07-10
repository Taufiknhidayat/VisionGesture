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

            # FPS
            fps = self.fps_counter.get_fps()

            # Overlay
            Overlay.draw_title(frame)
            Overlay.draw_fps(frame, fps)

            # Draw Every Hand
            for hand in hands:

                Overlay.draw_hand(frame, hand)

            # Total Finger
            Overlay.draw_total(frame, hands)

            # Total Hands
            cv2.putText(
                frame,
                f"HANDS : {len(hands)}",
                (20, 210),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (255, 255, 0),
                2,
            )

            # Exit
            cv2.putText(
                frame,
                "Press Q to Exit",
                (20, 680),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (255, 255, 255),
                2,
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