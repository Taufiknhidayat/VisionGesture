import cv2
import mediapipe as mp

from configs.settings import (
    MAX_HANDS,
    DETECTION_CONFIDENCE,
    TRACKING_CONFIDENCE,
    MIRROR_CAMERA,
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

                label = handedness.classification[0].label

                # Koreksi label jika kamera dimirror
                if MIRROR_CAMERA:
                    label = "Right" if label == "Left" else "Left"

                hand = Hand(
                    id=idx,
                    handedness=label,
                    landmarks=landmarks,
                    bbox=bbox,
                    center=center,
                )

                # Hitung jumlah, state jari, dan orientasi telapak tangan
                self.counter.count(hand)
                hand_list.append(hand)

                # Gambar landmark MediaPipe standar secara tipis/bersih
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