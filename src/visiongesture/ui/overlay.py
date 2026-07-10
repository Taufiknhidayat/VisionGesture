import cv2
from configs.colors import COLORS

class Overlay:
    def __init__(self):
        self.font = cv2.FONT_HERSHEY_SIMPLEX
        self.font_scale_labels = 0.55
        self.font_scale_values = 0.6
        self.thickness = 2
        
    def _draw_transparent_panel(self, frame, x, y, w, h, alpha=0.65):
        overlay = frame.copy()
        cv2.rectangle(overlay, (x, y), (x + w, y + h), (20, 20, 20), -1)
        cv2.addWeighted(overlay, alpha, frame, 1 - alpha, 0, frame)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (60, 60, 60), 1)

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

    def draw(self, frame, hands, fps):
        self._draw_transparent_panel(frame, 20, 20, 260, 50, alpha=0.7)
        
        cv2.putText(frame, "SYSTEM PERF :", (35, 48), self.font, self.font_scale_labels, (150, 150, 150), 1)
        fps_color = COLORS["GREEN"] if fps > 30 else COLORS["RED"]
        cv2.putText(frame, f"{fps} FPS", (150, 49), self.font, self.font_scale_values, fps_color, self.thickness)

        for hand in hands:
            if not hand.landmarks:
                continue

            is_right = hand.handedness == "Right"
            theme_color = COLORS["CYAN"] if is_right else COLORS["YELLOW"]
            hand_label = "RIGHT HAND" if is_right else "LEFT HAND"

            connections = [
                (0, 1), (1, 2), (2, 3), (3, 4),
                (0, 5), (5, 6), (6, 7), (7, 8),
                (5, 9), (9, 10), (10, 11), (11, 12),
                (9, 13), (13, 14), (14, 15), (15, 16),
                (13, 17), (17, 18), (18, 19), (19, 20),
                (0, 17)
            ]
            
            for p1_id, p2_id in connections:
                p1 = (int(hand.landmarks[p1_id].x * frame.shape[1]), int(hand.landmarks[p1_id].y * frame.shape[0]))
                p2 = (int(hand.landmarks[p2_id].x * frame.shape[1]), int(hand.landmarks[p2_id].y * frame.shape[0]))
                cv2.line(frame, p1, p2, (230, 230, 230), 1)

            for lm in hand.landmarks:
                cx, cy = int(lm.x * frame.shape[1]), int(lm.y * frame.shape[0])
                cv2.circle(frame, (cx, cy), 4, theme_color, -1)
                cv2.circle(frame, (cx, cy), 5, (255, 255, 255), 1)

            if hand.bbox:
                x, y, w, h = hand.bbox
                self._draw_modern_bbox(frame, hand.bbox, theme_color, length=12, t=2)

                info_y = y - 10 if y - 10 > 20 else y + h + 20
                
                # Menampilkan state Gestur dan Confidence Score
                gesture_name = hand.gesture.state.value if hand.gesture else "Unknown"
                conf = int(hand.gesture.confidence * 100) if hand.gesture else 0
                
                hand_info_text = f"[{hand_label[0]}] {gesture_name} ({conf}%)"
                
                # Buat background dinamis menyesuaikan panjang teks
                text_size = cv2.getTextSize(hand_info_text, self.font, 0.45, 1)[0]
                box_width = text_size[0] + 10
                
                cv2.rectangle(frame, (x, info_y - 15), (x + box_width, info_y + 5), (20, 20, 20), -1)
                cv2.rectangle(frame, (x, info_y - 15), (x + box_width, info_y + 5), theme_color, 1)
                
                cv2.putText(frame, hand_info_text, (x + 5, info_y - 2), 
                            self.font, 0.45, (255, 255, 255), 1, cv2.LINE_AA)

        return frame