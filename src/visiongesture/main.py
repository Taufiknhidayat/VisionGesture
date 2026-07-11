import cv2

from configs.settings import (
    APP_NAME,
    MIRROR_CAMERA,
    SHOW_DASHBOARD,
    DEFAULT_ACTIVE_MODULE,
    VIRTUAL_MOUSE_ENABLED
)

from src.visiongesture.camera.camera import Camera
from src.visiongesture.detector.hand_detector import HandDetector
from src.visiongesture.gesture.gesture_engine import GestureEngine
from src.visiongesture.gesture.gesture_state import GestureState
from src.visiongesture.tracker.motion_tracker import MotionTracker
from src.visiongesture.virtual_mouse.mouse_controller import MouseController
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
        
        # Priority 4: Virtual Mouse Controller
        self.mouse_controller = MouseController()
        
        self.active_module = DEFAULT_ACTIVE_MODULE
        
        self._register_events()

    def _register_events(self) -> None:
        """Registers all event listeners for Gestures and Motions."""
        
        # Scroll Handlers using the Motion Tracker events
        def on_scroll_motion(direction: str):
            if VIRTUAL_MOUSE_ENABLED and self.active_module == "Virtual Mouse":
                print(f"[MOUSE] Executing {direction} scroll")
                self.mouse_controller.scroll(direction)

        self.motion_tracker.on("Swipe Up", lambda d: on_scroll_motion("Swipe Up"))
        self.motion_tracker.on("Swipe Down", lambda d: on_scroll_motion("Swipe Down"))

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
            
            # Process Recognition Engines
            self.gesture_engine.process(hands)
            self.motion_tracker.process(hands)

            # Virtual Mouse Processing (Tracking the primary hand only)
            if VIRTUAL_MOUSE_ENABLED and self.active_module == "Virtual Mouse" and hands:
                self.mouse_controller.process(hands[0], frame)

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