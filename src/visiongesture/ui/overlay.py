import cv2
from configs.colors import COLORS

class Overlay:
    def __init__(self):
        self.font = cv2.FONT_HERSHEY_SIMPLEX
        
    def _draw_modern_bbox(self, frame, bbox, color, length=15, t=2):
        x, y, w, h = bbox
        cv2.rectangle(frame, (x, y), (x + w, y + h), color, 1)
        cv2.line(frame, (x, y), (x + length, y), color, t)
        cv2.line(frame, (x, y), (x, y + length), color, t)
        cv2.line(frame, (x + w, y), (x + w - length, y), color, t)
        cv2.line(frame, (x + w, y), (x + w, y + length), color, t)
        cv2.line(frame, (x, y + h), (x + length, y + h), color, t)
        cv2.line(frame, (x, y + h), (x, y + h - length), color, t)
        cv2.line(frame, (x + w, y + h), (x + w - length, y + h), color, t)
        cv2.line(frame, (x + w, y + h), (x + w, y + h - length), color, t)

    def draw(self, frame, hands):
        """Draws skeletons and bounding boxes over the hands."""
        for hand in hands:
            if not hand.landmarks:
                continue

            is_right = hand.handedness == "Right"
            theme_color = COLORS["CYAN"] if is_right else COLORS["YELLOW"]

            # Define skeleton connections
            connections = [
                (0, 1), (1, 2), (2, 3), (3, 4),
                (0, 5), (5, 6), (6, 7), (7, 8),
                (5, 9), (9, 10), (10, 11), (11, 12),
                (9, 13), (13, 14), (14, 15), (15, 16),
                (13, 17), (17, 18), (18, 19), (19, 20),
                (0, 17)
            ]
            
            # Draw connections (bones)
            for p1_id, p2_id in connections:
                p1 = (int(hand.landmarks[p1_id].x * frame.shape[1]), int(hand.landmarks[p1_id].y * frame.shape[0]))
                p2 = (int(hand.landmarks[p2_id].x * frame.shape[1]), int(hand.landmarks[p2_id].y * frame.shape[0]))
                cv2.line(frame, p1, p2, (230, 230, 230), 1)

            # Draw joints
            for lm in hand.landmarks:
                cx, cy = int(lm.x * frame.shape[1]), int(lm.y * frame.shape[0])
                cv2.circle(frame, (cx, cy), 4, theme_color, -1)
                cv2.circle(frame, (cx, cy), 5, (255, 255, 255), 1)

            # Draw bounding box
            if hand.bbox:
                self._draw_modern_bbox(frame, hand.bbox, theme_color, length=12, t=2)

        return frame