import cv2
import numpy as np
import pyautogui
from collections import deque
from screeninfo import get_monitors

from configs.settings import FRAME_WIDTH, FRAME_HEIGHT, FRAME_REDUCTION, MOUSE_SMOOTHING
from src.visiongesture.gesture.gesture_state import GestureState
from src.visiongesture.models.hand import Hand

class PresentationController:
    def __init__(self):
        pyautogui.FAILSAFE = False
        pyautogui.PAUSE = 0.0
        
        try:
            monitor = get_monitors()[0]
            self.screen_w = monitor.width
            self.screen_h = monitor.height
        except Exception:
            self.screen_w, self.screen_h = pyautogui.size()
            
        self.loc_history = deque(maxlen=MOUSE_SMOOTHING)

    def _get_smoothed_location(self, target_x: float, target_y: float) -> tuple[int, int]:
        """Stabilizes the laser pointer movement."""
        self.loc_history.append((target_x, target_y))
        xs, ys = zip(*self.loc_history)
        return int(np.mean(xs)), int(np.mean(ys))

    def process(self, hand: Hand, frame: np.ndarray) -> None:
        """Draws the laser pointer on the screen when using the INDEX gesture."""
        cv2.rectangle(frame, (FRAME_REDUCTION, FRAME_REDUCTION), 
                      (FRAME_WIDTH - FRAME_REDUCTION, FRAME_HEIGHT - FRAME_REDUCTION), 
                      (0, 165, 255), 2) # Orange border for Presentation Mode

        if not hand.landmarks or not hand.gesture:
            return

        current_gesture = hand.gesture.state
        
        # LASER POINTER MODE
        if current_gesture == GestureState.INDEX and len(hand.landmarks) > 8:
            x_px = hand.landmarks[8].x
            y_px = hand.landmarks[8].y
            
            # Render red glowing laser pointer on the camera frame
            cv2.circle(frame, (x_px, y_px), 6, (0, 0, 255), cv2.FILLED)
            cv2.circle(frame, (x_px, y_px), 12, (0, 0, 255), 1)

            # Move system cursor to match
            mapped_x = np.interp(x_px, (FRAME_REDUCTION, FRAME_WIDTH - FRAME_REDUCTION), (0, self.screen_w))
            mapped_y = np.interp(y_px, (FRAME_REDUCTION, FRAME_HEIGHT - FRAME_REDUCTION), (0, self.screen_h))
            
            sm_x, sm_y = self._get_smoothed_location(mapped_x, mapped_y)
            pyautogui.moveTo(sm_x, sm_y)

    def control_slide(self, action: str) -> None:
        """Executes keyboard shortcuts based on motion events."""
        if action == "Swipe Left":
            # Hand moves left -> Next Slide
            print("[PRESENTATION] Next Slide (Right Arrow)")
            pyautogui.press("right")
            
        elif action == "Swipe Right":
            # Hand moves right -> Previous Slide
            print("[PRESENTATION] Previous Slide (Left Arrow)")
            pyautogui.press("left")
            
        elif action == "Zoom In":
            # Dual hand expand -> Start Slideshow
            print("[PRESENTATION] Start Slideshow (F5)")
            pyautogui.press("f5")
            
        elif action == "Zoom Out":
            # Dual hand shrink -> End Slideshow
            print("[PRESENTATION] End Slideshow (ESC)")
            pyautogui.press("esc")