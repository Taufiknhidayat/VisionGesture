from collections import deque
from typing import Dict
from src.visiongesture.gesture.gesture_state import GestureState

class GestureHistory:
    def __init__(self, max_size: int):
        self.max_size = max_size
        self.buffers: Dict[str, deque] = {}

    def update(self, hand_id: str, gesture: GestureState) -> GestureState:
        if hand_id not in self.buffers:
            self.buffers[hand_id] = deque(maxlen=self.max_size)

        self.buffers[hand_id].append(gesture)

        # Voting majority
        counts: Dict[GestureState, int] = {}
        for g in self.buffers[hand_id]:
            counts[g] = counts.get(g, 0) + 1

        most_frequent_gesture = max(counts, key=counts.get)
        frequency = counts[most_frequent_gesture]

        if frequency >= (self.max_size // 2) + 1:
            return most_frequent_gesture
            
        return GestureState.UNKNOWN