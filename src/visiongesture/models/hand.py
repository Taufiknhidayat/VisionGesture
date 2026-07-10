from dataclasses import dataclass
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