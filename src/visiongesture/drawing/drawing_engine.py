import cv2
import numpy as np
from typing import Optional

from configs.colors import COLORS
from configs.settings import FRAME_WIDTH, FRAME_HEIGHT, DRAW_BRUSH_THICKNESS, DRAW_ERASER_THICKNESS
from src.visiongesture.models.hand import Hand
from src.visiongesture.gesture.gesture_state import GestureState
from src.visiongesture.drawing.canvas import Canvas

class DrawingEngine:
    def __init__(self):
        self.canvas = Canvas()
        self.current_color = COLORS["RED"]
        self.brush_thickness = DRAW_BRUSH_THICKNESS
        self.eraser_thickness = DRAW_ERASER_THICKNESS
        
        self.prev_x, self.prev_y = 0, 0
        self.is_drawing = False
        
        # Color Palette UI Configuration
        w, h, spacing = 80, 60, 20
        start_x = (FRAME_WIDTH - (4*w + 3*spacing)) // 2
        
        self.palette = [
            (start_x, 20, start_x+w, 20+h, COLORS["RED"], "RED"),
            (start_x + w + spacing, 20, start_x + 2*w + spacing, 20+h, COLORS["GREEN"], "GREEN"),
            (start_x + 2*(w + spacing), 20, start_x + 3*w + 2*spacing, 20+h, COLORS["CYAN"], "CYAN"),
            (start_x + 3*(w + spacing), 20, start_x + 4*w + 3*spacing, 20+h, (0, 0, 0), "ERASE")
        ]

    def process(self, hand: Optional[Hand], frame: np.ndarray) -> np.ndarray:
        # 1. Draw Palette UI on Top of the Frame
        for x1, y1, x2, y2, color, label in self.palette:
            if color == (0, 0, 0): # Eraser Box styling
                cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 255, 255), 2)
                cv2.putText(frame, "ERASER", (x1 + 10, y1 + 35), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
            else:
                cv2.rectangle(frame, (x1, y1), (x2, y2), color, cv2.FILLED)
                
            # Highlight Outline if Selected
            if self.current_color == color:
                cv2.rectangle(frame, (x1 - 3, y1 - 3), (x2 + 3, y2 + 3), (255, 255, 255), 3)

        # 2. Process Core Drawing Mechanics
        if hand and hand.landmarks and hand.gesture:
            current_gesture = hand.gesture.state
            
            # Extract Index Finger Tip (Landmark 8) coordinates
            # PERBAIKAN BUG: x dan y sudah dalam bentuk piksel, tidak perlu dikali FRAME_WIDTH lagi
            x = hand.landmarks[8].x
            y = hand.landmarks[8].y

            # HOVER & SELECT MODE (Peace Gesture: 2 Fingers)
            if current_gesture == GestureState.PEACE:
                self.prev_x, self.prev_y = 0, 0
                
                if self.is_drawing:
                    self.canvas.save_state()
                    self.is_drawing = False
                
                # Check UI Collision for Tool Selection
                for x1, y1, x2, y2, color, _ in self.palette:
                    if x1 < x < x2 and y1 < y < y2:
                        self.current_color = color
                        
                # Draw hover tracker
                cv2.circle(frame, (x, y), 10, self.current_color, cv2.FILLED)
                cv2.circle(frame, (x, y), 12, (255, 255, 255), 2)

            # DRAW MODE (Index Gesture: 1 Finger)
            elif current_gesture == GestureState.INDEX:
                if not self.is_drawing:
                    self.is_drawing = True
                    self.prev_x, self.prev_y = x, y
                    
                thickness = self.eraser_thickness if self.current_color == (0, 0, 0) else self.brush_thickness
                self.canvas.draw_line((self.prev_x, self.prev_y), (x, y), self.current_color, thickness)
                self.prev_x, self.prev_y = x, y
                
                # Draw brush tip
                cv2.circle(frame, (x, y), thickness // 2, self.current_color, cv2.FILLED)
                
            # STOP DRAWING (Any other gesture)
            else:
                if self.is_drawing:
                    self.canvas.save_state()
                    self.is_drawing = False
                self.prev_x, self.prev_y = 0, 0

        # 3. Blend Canvas onto Frame seamlessly
        gray = cv2.cvtColor(self.canvas.canvas, cv2.COLOR_BGR2GRAY)
        _, mask = cv2.threshold(gray, 1, 255, cv2.THRESH_BINARY)
        mask_inv = cv2.bitwise_not(mask)
        
        frame_bg = cv2.bitwise_and(frame, frame, mask=mask_inv)
        canvas_fg = cv2.bitwise_and(self.canvas.canvas, self.canvas.canvas, mask=mask)
        
        return cv2.add(frame_bg, canvas_fg)