import cv2
import numpy as np
import pyautogui
from screeninfo import get_monitors
from collections import deque

from configs.settings import FRAME_WIDTH, FRAME_HEIGHT, MOUSE_SMOOTHING, FRAME_REDUCTION
from src.visiongesture.gesture.gesture_state import GestureState
from src.visiongesture.models.hand import Hand

class MouseController:
    def __init__(self):
        # Disable PyAutoGUI failsafe and pause for real-time smooth performance
        pyautogui.FAILSAFE = False
        pyautogui.PAUSE = 0.0
        
        # Multi-monitor support: Get primary monitor resolution dynamically
        try:
            monitor = get_monitors()[0]
            self.screen_w = monitor.width
            self.screen_h = monitor.height
        except Exception:
            self.screen_w, self.screen_h = pyautogui.size()
        
        self.loc_history = deque(maxlen=MOUSE_SMOOTHING)
        self.is_dragging = False
        self.last_gesture = GestureState.UNKNOWN

    def _get_smoothed_location(self, target_x: float, target_y: float) -> tuple[int, int]:
        """Applies a moving average filter to stabilize the mouse cursor."""
        self.loc_history.append((target_x, target_y))
        xs, ys = zip(*self.loc_history)
        return int(np.mean(xs)), int(np.mean(ys))

    def process(self, hand: Hand, frame: np.ndarray) -> None:
        """Processes hand gestures to control the mouse pointer and clicks."""
        if not hand.landmarks or not hand.gesture:
            return

        # Draw Active Region Box on the frame (user visual guide)
        cv2.rectangle(frame, (FRAME_REDUCTION, FRAME_REDUCTION), 
                      (FRAME_WIDTH - FRAME_REDUCTION, FRAME_HEIGHT - FRAME_REDUCTION), 
                      (255, 0, 255), 2)

        # We use the Index Finger Tip (Landmark 8) for cursor tracking
        if len(hand.landmarks) <= 8:
            return

        x1, y1 = hand.landmarks[8].x, hand.landmarks[8].y
        
        # Draw a highlighted circle on the tracking finger
        cv2.circle(frame, (x1, y1), 8, (255, 255, 0), cv2.FILLED)

        # Map camera coordinates to screen coordinates
        mapped_x = np.interp(x1, (FRAME_REDUCTION, FRAME_WIDTH - FRAME_REDUCTION), (0, self.screen_w))
        mapped_y = np.interp(y1, (FRAME_REDUCTION, FRAME_HEIGHT - FRAME_REDUCTION), (0, self.screen_h))
        
        # Apply smoothing
        sm_x, sm_y = self._get_smoothed_location(mapped_x, mapped_y)

        current_gesture = hand.gesture.state

        # -------------------------------------------------------------
        # VIRTUAL MOUSE ACTIONS MAPPING
        # -------------------------------------------------------------
        
        # 1. MOVE: Index Gesture (1 finger up)
        if current_gesture == GestureState.INDEX:
            pyautogui.moveTo(sm_x, sm_y)
            if self.is_dragging:
                pyautogui.mouseUp()
                self.is_dragging = False
                
        # 2. LEFT CLICK & DRAG: OK Gesture (Thumb & Index pinched together)
        elif current_gesture == GestureState.OK:
            pyautogui.moveTo(sm_x, sm_y)
            if self.last_gesture != GestureState.OK:
                pyautogui.mouseDown()
                self.is_dragging = True
                
        # 3. RIGHT CLICK: Peace Gesture (2 fingers up)
        elif current_gesture == GestureState.PEACE:
            if self.last_gesture != GestureState.PEACE:
                pyautogui.rightClick()
                
        # 4. DOUBLE CLICK: Rock Gesture
        elif current_gesture == GestureState.ROCK:
            if self.last_gesture != GestureState.ROCK:
                pyautogui.doubleClick()

        self.last_gesture = current_gesture

    def scroll(self, direction: str) -> None:
        """Handles scrolling events triggered by MotionTracker."""
        scroll_amount = 500
        if direction == "Swipe Up":
            pyautogui.scroll(scroll_amount)
        elif direction == "Swipe Down":
            pyautogui.scroll(-scroll_amount)