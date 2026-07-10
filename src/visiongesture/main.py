import cv2

from configs.settings import (
    APP_NAME,
    MIRROR_CAMERA,
)

from src.visiongesture.camera.camera import Camera
from src.visiongesture.detector.hand_detector import HandDetector
from src.visiongesture.gesture.gesture_engine import GestureEngine
from src.visiongesture.gesture.gesture_state import GestureState
from src.visiongesture.ui.fps import FPSCounter
from src.visiongesture.ui.overlay import Overlay

class VisionGestureApp:

    def __init__(self):
        self.camera = Camera()
        self.detector = HandDetector()
        self.fps_counter = FPSCounter()
        self.overlay = Overlay()
        
        # Inisialisasi Gesture Engine
        self.gesture_engine = GestureEngine()
        
        # Mendaftarkan contoh Event Listener untuk Gesture
        self._register_events()

    def _register_events(self):
        """Register custom callbacks for specific gestures (Event-Driven)."""
        def on_peace(hand):
            print(f"[EVENT] {hand.handedness} Hand triggered PEACE gesture!")
            
        def on_fist(hand):
            print(f"[EVENT] {hand.handedness} Hand triggered FIST! Ready to grab/click.")

        # Daftarkan ke mesin event
        self.gesture_engine.events.on(GestureState.PEACE, on_peace)
        self.gesture_engine.events.on(GestureState.FIST, on_fist)

    def run(self):
        while True:
            success, frame = self.camera.read()

            if not success:
                print("[ERROR] Camera failed to read frame.")
                break

            if MIRROR_CAMERA:
                frame = cv2.flip(frame, 1)

            # Deteksi Tangan (sudah menghitung matriks jari di dalamnya)
            frame, hands = self.detector.detect(frame)
            
            # Proses matriks jari menjadi Gestur
            self.gesture_engine.process(hands)

            fps = self.fps_counter.get_fps()

            # Render UI
            frame = self.overlay.draw(frame, hands, fps)

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