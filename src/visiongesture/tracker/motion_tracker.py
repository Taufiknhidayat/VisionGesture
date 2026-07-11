import math
from collections import deque
from typing import Dict, List, Callable
from configs.settings import MOTION_HISTORY_SIZE, SWIPE_THRESHOLD, ZOOM_SENSITIVITY
from src.visiongesture.models.hand import Hand

class MotionTracker:
    def __init__(self):
        self.history: Dict[int, deque] = {}
        self.listeners: Dict[str, Callable[[str], None]] = {}
        
        self.last_triggered_swipe: Dict[int, str] = {}
        self.prev_zoom_distance = None

    def on(self, event_name: str, callback: Callable[[str], None]) -> None:
        """Registers a callback for motion events like Swipe Left, Swipe Right, Zoom In, etc."""
        self.listeners[event_name] = callback

    def _trigger(self, event_name: str, data: str) -> None:
        if event_name in self.listeners:
            self.listeners[event_name](data)

    def process(self, hands: List[Hand]) -> None:
        """Analyzes movement history of stable hands to determine dynamic motions."""
        
        # 1. Single Hand Motion (Swipes)
        for hand in hands:
            if hand.id not in self.history:
                self.history[hand.id] = deque(maxlen=MOTION_HISTORY_SIZE)
            
            self.history[hand.id].append(hand.center)
            path = self.history[hand.id]

            if len(path) == MOTION_HISTORY_SIZE:
                start_x, start_y = path[0]
                end_x, end_y = path[-1]

                dx = end_x - start_x
                dy = end_y - start_y
                
                motion_detected = None

                # Check horizontal swipe
                if abs(dx) > abs(dy) and abs(dx) > SWIPE_THRESHOLD:
                    motion_detected = "Swipe Right" if dx > 0 else "Swipe Left"
                # Check vertical swipe
                elif abs(dy) > abs(dx) and abs(dy) > SWIPE_THRESHOLD:
                    motion_detected = "Swipe Down" if dy > 0 else "Swipe Up"

                # Prevent spamming the same swipe continuously
                if motion_detected:
                    if self.last_triggered_swipe.get(hand.id) != motion_detected:
                        self._trigger(motion_detected, f"Hand {hand.id}")
                        self.last_triggered_swipe[hand.id] = motion_detected
                        self.history[hand.id].clear() # Reset path after valid swipe
                else:
                    self.last_triggered_swipe[hand.id] = None

        # 2. Dual Hand Motion (Zoom)
        if len(hands) == 2:
            cx1, cy1 = hands[0].center
            cx2, cy2 = hands[1].center
            
            current_dist = math.hypot(cx2 - cx1, cy2 - cy1)
            
            if self.prev_zoom_distance is not None:
                dist_diff = current_dist - self.prev_zoom_distance
                
                if dist_diff > ZOOM_SENSITIVITY:
                    self._trigger("Zoom In", "Dual Hands")
                elif dist_diff < -ZOOM_SENSITIVITY:
                    self._trigger("Zoom Out", "Dual Hands")
                    
            self.prev_zoom_distance = current_dist
        else:
            self.prev_zoom_distance = None