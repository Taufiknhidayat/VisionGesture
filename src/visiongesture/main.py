import cv2

from configs.settings import (
    APP_NAME,
    MIRROR_CAMERA,
    SHOW_DASHBOARD,
    DEFAULT_ACTIVE_MODULE
)

from src.visiongesture.camera.camera import Camera
from src.visiongesture.detector.hand_detector import HandDetector
from src.visiongesture.gesture.gesture_engine import GestureEngine
from src.visiongesture.gesture.gesture_state import GestureState
from src.visiongesture.tracker.motion_tracker import MotionTracker
from src.visiongesture.ui.fps import FPSCounter
from src.visiongesture.ui.overlay import Overlay
from src.visiongesture.ui.dashboard import Dashboard

class VisionGestureApp:

    def __init__(self):
        self.camera = Camera()
        self.detector = HandDetector()
        self.fps_counter = FPSCounter()
        self.overlay = Overlay()
        self.dashboard = Dashboard()
        
        self.gesture_engine = GestureEngine()
        self.motion_tracker = MotionTracker()
        
        self.active_module = DEFAULT_ACTIVE_MODULE
        
        self._register_events()

    def _register_events(self) -> None:
        """Registers all event listeners for Gestures and Motions."""
        # --- Static Gestures ---
        def on_peace(hand):
            print(f"[GESTURE] {hand.handedness} Hand ID-{hand.id} triggered PEACE!")
            
        def on_fist(hand):
            print(f"[GESTURE] {hand.handedness} Hand ID-{hand.id} triggered FIST!")

        self.gesture_engine.events.on(GestureState.PEACE, on_peace)
        self.gesture_engine.events.on(GestureState.FIST, on_fist)

        # --- Dynamic Motions ---
        def on_swipe(data):
            print(f"[MOTION] {data} performed a Swipe!")
            
        def on_zoom_in(data):
            print(f"[MOTION] {data} are Zooming IN +++")

        def on_zoom_out(data):
            print(f"[MOTION] {data} are Zooming OUT ---")

        self.motion_tracker.on("Swipe Left", lambda d: print(f"[MOTION] {d}: SWIPE LEFT <<<"))
        self.motion_tracker.on("Swipe Right", lambda d: print(f"[MOTION] {d}: SWIPE RIGHT >>>"))
        self.motion_tracker.on("Swipe Up", lambda d: print(f"[MOTION] {d}: SWIPE UP ^^^"))
        self.motion_tracker.on("Swipe Down", lambda d: print(f"[MOTION] {d}: SWIPE DOWN vvv"))
        self.motion_tracker.on("Zoom In", on_zoom_in)
        self.motion_tracker.on("Zoom Out", on_zoom_out)

    def run(self) -> None:
        while True:
            success, frame = self.camera.read()

            if not success:
                print("[ERROR] Camera failed to read frame.")
                break

            if MIRROR_CAMERA:
                frame = cv2.flip(frame, 1)

            # Detector includes MediaPipe processing + Hungarian Stable Centroid Tracker
            frame, hands = self.detector.detect(frame)
            
            # Static Gesture Recognition
            self.gesture_engine.process(hands)
            
            # Dynamic Motion Recognition (Swipes, Zoom)
            self.motion_tracker.process(hands)

            fps = self.fps_counter.get_fps()

            # Render UI
            frame = self.overlay.draw(frame, hands)
            if SHOW_DASHBOARD:
                frame = self.dashboard.draw(frame, hands, fps, self.active_module)

            cv2.putText(
                frame,
                "Press 'Q' to Exit",
                (frame.shape[1] - 180, frame.shape[0] - 25),
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