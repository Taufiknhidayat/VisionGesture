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
from src.visiongesture.drawing.drawing_engine import DrawingEngine
from src.visiongesture.presentation.presentation_controller import PresentationController
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
        
        self.mouse_controller = MouseController()
        self.drawing_engine = DrawingEngine()
        
        # Priority 6: Presentation Controller
        self.presentation_controller = PresentationController()
        
        self.active_module = DEFAULT_ACTIVE_MODULE
        self._register_events()

    def _register_events(self) -> None:
        """Registers all event listeners for Gestures and Motions."""
        
        # --- Air Drawing Gesture Handlers ---
        def on_thumb_up(hand):
            if self.active_module == "Air Drawing":
                self.drawing_engine.canvas.undo()

        def on_thumb_down(hand):
            if self.active_module == "Air Drawing":
                self.drawing_engine.canvas.redo()

        def on_love(hand):
            if self.active_module == "Air Drawing":
                self.drawing_engine.canvas.save("png")
                self.drawing_engine.canvas.save("pdf")

        def on_fist(hand):
            if self.active_module == "Air Drawing":
                self.drawing_engine.canvas.clear()

        self.gesture_engine.events.on(GestureState.THUMB_UP, on_thumb_up)
        self.gesture_engine.events.on(GestureState.THUMB_DOWN, on_thumb_down)
        self.gesture_engine.events.on(GestureState.LOVE, on_love)
        self.gesture_engine.events.on(GestureState.FIST, on_fist)

        # --- Dynamic Motion Route Handlers ---
        def on_motion(action: str):
            if self.active_module == "Virtual Mouse" and VIRTUAL_MOUSE_ENABLED:
                if action in ["Swipe Up", "Swipe Down"]:
                    self.mouse_controller.scroll(action)
            
            elif self.active_module == "Presentation Controller":
                self.presentation_controller.control_slide(action)

        self.motion_tracker.on("Swipe Up", lambda d: on_motion("Swipe Up"))
        # PERBAIKAN BUG: Typo on_scroll_motion telah diganti menjadi on_motion
        self.motion_tracker.on("Swipe Down", lambda d: on_motion("Swipe Down"))
        self.motion_tracker.on("Swipe Left", lambda d: on_motion("Swipe Left"))
        self.motion_tracker.on("Swipe Right", lambda d: on_motion("Swipe Right"))
        self.motion_tracker.on("Zoom In", lambda d: on_motion("Zoom In"))
        self.motion_tracker.on("Zoom Out", lambda d: on_motion("Zoom Out"))

    def run(self) -> None:
        while True:
            success, frame = self.camera.read()

            if not success:
                print("[ERROR] Camera failed to read frame.")
                break

            if MIRROR_CAMERA:
                frame = cv2.flip(frame, 1)

            # Core Detections
            frame, hands = self.detector.detect(frame)
            self.gesture_engine.process(hands)
            self.motion_tracker.process(hands)

            # Route execution based on Active Module
            if hands:
                primary_hand = hands[0]
                if self.active_module == "Virtual Mouse":
                    self.mouse_controller.process(primary_hand, frame)
                elif self.active_module == "Presentation Controller":
                    self.presentation_controller.process(primary_hand, frame)

            if self.active_module == "Air Drawing":
                hand = hands[0] if hands else None
                frame = self.drawing_engine.process(hand, frame)

            fps = self.fps_counter.get_fps()

            # Render UI Layers
            frame = self.overlay.draw(frame, hands)
            if SHOW_DASHBOARD:
                frame = self.dashboard.draw(frame, hands, fps, self.active_module)

            # Draw Control Hotkeys Hint
            cv2.putText(
                frame,
                "KEYS: [M]ouse | [D]raw | [P]resent | [T]rack",
                (frame.shape[1] - 400, frame.shape[0] - 25),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                (180, 180, 180),
                1,
                cv2.LINE_AA
            )

            cv2.imshow(APP_NAME, frame)

            # Hotkey Switcher Logic
            key = cv2.waitKey(1) & 0xFF
            if key == ord("q"):
                break
            elif key == ord("m"):
                self.active_module = "Virtual Mouse"
            elif key == ord("d"):
                self.active_module = "Air Drawing"
            elif key == ord("p"):
                self.active_module = "Presentation Controller"
            elif key == ord("t"):
                self.active_module = "Tracking Engine"

        self.camera.release()
        cv2.destroyAllWindows()


def main():
    app = VisionGestureApp()
    app.run()

if __name__ == "__main__":
    main()