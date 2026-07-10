import cv2
import mediapipe as mp

from configs.settings import (
    MAX_HANDS,
    DETECTION_CONFIDENCE,
    TRACKING_CONFIDENCE,
)

from src.visiongesture.models.hand import Hand, Landmark
from src.visiongesture.counter.finger_counter import FingerCounter


class HandDetector:

    def __init__(self):
        self.mp_hands = mp.solutions.hands

        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=MAX_HANDS,
            min_detection_confidence=DETECTION_CONFIDENCE,
            min_tracking_confidence=TRACKING_CONFIDENCE,
        )

        self.drawer = mp.solutions.drawing_utils
        self.counter = FingerCounter()

    def detect(self, frame):
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.hands.process(rgb)
        hand_list = []

        if results.multi_hand_landmarks:
            h, w, _ = frame.shape

            for idx, (hand_landmarks, handedness) in enumerate(
                zip(results.multi_hand_landmarks, results.multi_handedness)
            ):
                xs = []
                ys = []
                landmarks = []

                for i, lm in enumerate(hand_landmarks.landmark):
                    px = int(lm.x * w)
                    py = int(lm.y * h)

                    xs.append(px)
                    ys.append(py)

                    landmarks.append(
                        Landmark(
                            id=i,
                            x=px,
                            y=py,
                        )
                    )

                xmin, xmax = min(xs), max(xs)
                ymin, ymax = min(ys), max(ys)

                bbox = (xmin, ymin, xmax - xmin, ymax - ymin)
                center = ((xmin + xmax) // 2, (ymin + ymax) // 2)

                # Fetch raw label directly from MediaPipe
                # Removed the manual swap logic to fix the inverted Right/Left issue on front camera
                label = handedness.classification[0].label

                hand = Hand(
                    id=idx,
                    handedness=label,
                    landmarks=landmarks,
                    bbox=bbox,
                    center=center,
                )

                # Calculate finger state, angles, and palm orientation
                self.counter.count(hand)
                hand_list.append(hand)

                # Draw standard MediaPipe landmarks cleanly
                self.drawer.draw_landmarks(
                    frame,
                    hand_landmarks,
                    self.mp_hands.HAND_CONNECTIONS,
                    self.drawer.DrawingSpec(
                        color=(0, 255, 255),
                        thickness=2,
                        circle_radius=2,
                    ),
                    self.drawer.DrawingSpec(
                        color=(255, 0, 255),
                        thickness=1,
                    ),
                )

        return frame, hand_list