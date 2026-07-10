from dataclasses import dataclass, field
from typing import List, Tuple, Any

@dataclass
class Landmark:
    id: int
    x: int
    y: int

@dataclass
class Hand:
    id: int
    handedness: str
    landmarks: List[Landmark]
    bbox: Tuple[int, int, int, int]
    center: Tuple[int, int]
    fingers: int = 0
    
    finger_state: List[int] = field(default_factory=lambda: [0, 0, 0, 0, 0])
    orientation: str = "Front"
    
    # Akan diisi oleh Gesture Engine
    gesture: Any = None