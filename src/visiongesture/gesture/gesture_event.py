from typing import Callable, Dict
from src.visiongesture.gesture.gesture_state import GestureState
from src.visiongesture.models.hand import Hand

class GestureEvent:
    def __init__(self):
        self.listeners: Dict[GestureState, Callable[[Hand], None]] = {}
        self.last_triggered_state: Dict[str, GestureState] = {}

    def on(self, gesture: GestureState, callback: Callable[[Hand], None]) -> None:
        """Register a callback function for a specific gesture."""
        self.listeners[gesture] = callback

    def trigger(self, hand: Hand, gesture: GestureState) -> None:
        """Triggers the callback if the gesture state has changed."""
        hand_key = f"{hand.id}_{hand.handedness}"
        last_state = self.last_triggered_state.get(hand_key, GestureState.UNKNOWN)

        # Ensure we only trigger once per state change to prevent spamming
        if gesture != last_state:
            if gesture in self.listeners:
                self.listeners[gesture](hand)
            self.last_triggered_state[hand_key] = gesture