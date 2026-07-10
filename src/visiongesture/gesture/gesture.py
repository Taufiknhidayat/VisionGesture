from dataclasses import dataclass
from src.visiongesture.gesture.gesture_state import GestureState

@dataclass
class Gesture:
    state: GestureState
    confidence: float