import cv2
import mediapipe as mp

from configs.settings import (
    MAX_HANDS,
    DETECTION_CONFIDENCE,
    TRACKING_CONFIDENCE,
)

from src.visiongesture.models.hand import Hand, Landmark
from src.visiongesture.counter.finger_counter import FingerCounter
from src.visiongesture.tracker.centroid_tracker import CentroidTracker

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
        
        # Initialize Stable Centroid Tracker
        self.centroid_tracker = CentroidTracker()

    def detect(self, frame):
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.hands.process(rgb)
        
        hand_list = []
        raw_centers = []
        raw_hand_data = []

        if results.multi_hand_landmarks:
            h, w, _ = frame.shape

            for hand_landmarks, handedness in zip(results.multi_hand_landmarks, results.multi_handedness):
                xs = []
                ys = []
                landmarks = []

                for i, lm in enumerate(hand_landmarks.landmark):
                    px = int(lm.x * w)
                    py = int(lm.y * h)
                    xs.append(px)
                    ys.append(py)
                    landmarks.append(Landmark(id=i, x=px, y=py))

                xmin, xmax = min(xs), max(xs)
                ymin, ymax = min(ys), max(ys)

                bbox = (xmin, ymin, xmax - xmin, ymax - ymin)
                center = ((xmin + xmax) // 2, (ymin + ymax) // 2)
                
                label = handedness.classification[0].label

                raw_centers.append(center)
                raw_hand_data.append((label, landmarks, bbox, center, hand_landmarks))

        # Pass raw centers to Hungarian Algorithm Tracker to get stable IDs
        tracked_objects = self.centroid_tracker.update(raw_centers)

        # Re-map tracked stable IDs back to Hand models
        for obj_id, centroid in tracked_objects.items():
            # Find matching raw data for this tracked centroid
            for data in raw_hand_data:
                label, landmarks, bbox, raw_center, mp_landmarks = data
                if centroid == raw_center:
                    hand = Hand(
                        id=obj_id, # Replaced MediaPipe index with STABLE ID
                        handedness=label,
                        landmarks=landmarks,
                        bbox=bbox,
                        center=centroid,
                    )
                    
                    self.counter.count(hand)
                    hand_list.append(hand)

                    self.drawer.draw_landmarks(
                        frame,
                        mp_landmarks,
                        self.mp_hands.HAND_CONNECTIONS,
                        self.drawer.DrawingSpec(color=(0, 255, 255), thickness=2, circle_radius=2),
                        self.drawer.DrawingSpec(color=(255, 0, 255), thickness=1),
                    )
                    break

        return frame, hand_list