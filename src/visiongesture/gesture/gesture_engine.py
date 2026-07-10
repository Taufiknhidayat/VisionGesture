from typing import List
from configs.settings import GESTURE_BUFFER_SIZE, GESTURE_CONFIDENCE_MIN
from src.visiongesture.models.hand import Hand
from src.visiongesture.gesture.gesture_state import GestureState
from src.visiongesture.gesture.gesture import Gesture
from src.visiongesture.gesture.gesture_history import GestureHistory
from src.visiongesture.gesture.gesture_event import GestureEvent

class GestureEngine:
    def __init__(self):
        self.history = GestureHistory(max_size=GESTURE_BUFFER_SIZE)
        self.events = GestureEvent()

    def _recognize_pattern(self, hand: Hand) -> Gesture:
        """Maps binary finger state and palm orientation to a specific gesture."""
        state = hand.finger_state
        recognized_state = GestureState.UNKNOWN
        confidence = 0.0

        if state == [0, 0, 0, 0, 0]:
            recognized_state = GestureState.FIST
            confidence = 0.95
            
        elif state == [1, 1, 1, 1, 1]:
            recognized_state = GestureState.OPEN_HAND
            confidence = 0.98
            
        elif state == [0, 1, 0, 0, 0]:
            recognized_state = GestureState.INDEX
            confidence = 0.90
            
        elif state == [0, 1, 1, 0, 0]:
            recognized_state = GestureState.PEACE
            confidence = 0.92
            
        elif state == [1, 1, 0, 0, 1]:
            recognized_state = GestureState.LOVE
            confidence = 0.85
            
        elif state == [0, 1, 0, 0, 1]:
            recognized_state = GestureState.ROCK
            confidence = 0.88
            
        elif state == [1, 0, 0, 0, 1]:
            recognized_state = GestureState.CALL_ME
            confidence = 0.90
            
        elif state == [0, 0, 1, 1, 1]: 
            # OK gesture (Thumb and Index touching, others open)
            recognized_state = GestureState.OK
            confidence = 0.80
            
        elif state == [1, 0, 0, 0, 0]:
            # Use orientation or y-coordinates to differentiate Thumb Up and Down
            wrist_y = hand.landmarks[0].y
            thumb_tip_y = hand.landmarks[4].y
            
            if thumb_tip_y < wrist_y:
                recognized_state = GestureState.THUMB_UP
            else:
                recognized_state = GestureState.THUMB_DOWN
            confidence = 0.95

        # Note: VULCAN [0,1,1,1,1] requires distance checking between middle and ring.
        # This will be refined later, mapped as Unknown for now to avoid false positives.

        return Gesture(state=recognized_state, confidence=confidence)

    def process(self, hands: List[Hand]) -> None:
        """Processes all detected hands through the history buffer and triggers events."""
        for hand in hands:
            if not hand.finger_state:
                continue

            raw_gesture = self._recognize_pattern(hand)
            hand_key = f"{hand.id}_{hand.handedness}"

            # Apply buffer filter
            smoothed_state = self.history.update(hand_key, raw_gesture.state)

            # Assign to hand model
            final_gesture = Gesture(state=smoothed_state, confidence=raw_gesture.confidence)
            hand.gesture = final_gesture

            # Trigger registered events if confidence meets the minimum threshold
            if final_gesture.confidence >= GESTURE_CONFIDENCE_MIN:
                self.events.trigger(hand, final_gesture.state)