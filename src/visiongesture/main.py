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
        
        self.active_module = DEFAULT_ACTIVE_MODULE
        
        self._register_events()

    def _register_events(self) -> None:
        """Register custom callbacks for specific gestures."""
        def on_peace(hand):
            print(f"[EVENT] {hand.handedness} Hand triggered PEACE gesture!")
            
        def on_fist(hand):
            print(f"[EVENT] {hand.handedness} Hand triggered FIST!")

        self.gesture_engine.events.on(GestureState.PEACE, on_peace)
        self.gesture_engine.events.on(GestureState.FIST, on_fist)

    def run(self) -> None:
        while True:
            success, frame = self.camera.read()

            if not success:
                print("[ERROR] Camera failed to read frame.")
                break

            if MIRROR_CAMERA:
                frame = cv2.flip(frame, 1)

            # Detect Hands and calculate finger states
            frame, hands = self.detector.detect(frame)
            
            # Process gestures
            self.gesture_engine.process(hands)

            # Calculate FPS
            fps = self.fps_counter.get_fps()

            # Render UI Layers
            frame = self.overlay.draw(frame, hands)
            
            if SHOW_DASHBOARD:
                frame = self.dashboard.draw(frame, hands, fps, self.active_module)

            # Draw Exit Instruction
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