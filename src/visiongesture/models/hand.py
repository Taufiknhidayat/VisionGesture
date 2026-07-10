from dataclasses import dataclass, field
from typing import List, Tuple

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
    
    # Properti Baru untuk Mendukung AI & Gesture Engine
    finger_state: List[int] = field(default_factory=lambda: [0, 0, 0, 0, 0]) # Contoh: [1, 1, 1, 1, 1]
    orientation: str = "Front"                                                # Palm Up/Down/Left/Right/Front