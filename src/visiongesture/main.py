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
        
        # Priority 5: Air Drawing Engine
        self.drawing_engine = DrawingEngine()
        
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

        # --- Virtual Mouse Scroll Handlers ---
        def on_scroll_motion(direction: str):
            if VIRTUAL_MOUSE_ENABLED and self.active_module == "Virtual Mouse":
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

            # Core Detections
            frame, hands = self.detector.detect(frame)
            self.gesture_engine.process(hands)
            self.motion_tracker.process(hands)

            # Route execution based on Active Module
            if hands:
                if self.active_module == "Virtual Mouse":
                    self.mouse_controller.process(hands[0], frame)

            if self.active_module == "Air Drawing":
                # Air Drawing handles its own frame merging (can run even without hands)
                hand = hands[0] if hands else None
                frame = self.drawing_engine.process(hand, frame)

            fps = self.fps_counter.get_fps()

            # Render UI
            frame = self.overlay.draw(frame, hands)
            if SHOW_DASHBOARD:
                frame = self.dashboard.draw(frame, hands, fps, self.active_module)

            # Draw Control Hotkeys Hint
            cv2.putText(
                frame,
                "KEYS: [M]ouse | [D]raw | [T]rack | [Q]uit",
                (frame.shape[1] - 380, frame.shape[0] - 25),
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
            elif key == ord("t"):
                self.active_module = "Tracking Engine"

        self.camera.release()
        cv2.destroyAllWindows()


def main():
    app = VisionGestureApp()
    app.run()

if __name__ == "__main__":
    main()