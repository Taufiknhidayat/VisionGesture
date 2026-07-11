import cv2
import numpy as np
import os
import time
from datetime import datetime
from PIL import Image

from configs.settings import FRAME_WIDTH, FRAME_HEIGHT, DRAW_MAX_UNDO_STEPS, EXPORT_DIR

class Canvas:
    def __init__(self):
        self.max_undo = DRAW_MAX_UNDO_STEPS
        self.canvas = np.zeros((FRAME_HEIGHT, FRAME_WIDTH, 3), dtype=np.uint8)
        self.undo_stack = [self.canvas.copy()]
        self.redo_stack = []
        
        os.makedirs(EXPORT_DIR, exist_ok=True)
        self.last_action_time = time.time()

    def draw_line(self, pt1: tuple, pt2: tuple, color: tuple, thickness: int) -> None:
        """Draws a continuous line on the canvas array."""
        cv2.line(self.canvas, pt1, pt2, color, thickness)

    def save_state(self) -> None:
        """Pushes the current canvas to the undo stack upon completing a stroke."""
        self.undo_stack.append(self.canvas.copy())
        if len(self.undo_stack) > self.max_undo:
            self.undo_stack.pop(0)
        self.redo_stack.clear()

    def undo(self) -> None:
        if time.time() - self.last_action_time < 0.5: return
        if len(self.undo_stack) > 1:
            self.redo_stack.append(self.undo_stack.pop())
            self.canvas = self.undo_stack[-1].copy()
            self.last_action_time = time.time()
            print("[CANVAS] Undo executed.")

    def redo(self) -> None:
        if time.time() - self.last_action_time < 0.5: return
        if len(self.redo_stack) > 0:
            self.undo_stack.append(self.redo_stack.pop())
            self.canvas = self.undo_stack[-1].copy()
            self.last_action_time = time.time()
            print("[CANVAS] Redo executed.")

    def clear(self) -> None:
        if time.time() - self.last_action_time < 1.0: return
        self.canvas = np.zeros((FRAME_HEIGHT, FRAME_WIDTH, 3), dtype=np.uint8)
        self.save_state()
        self.last_action_time = time.time()
        print("[CANVAS] Cleared.")

    def save(self, fmt="png") -> None:
        """Exports drawing. PNG is transparent. PDF has a white background."""
        if time.time() - self.last_action_time < 1.5: return
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{EXPORT_DIR}/drawing_{timestamp}.{fmt}"
        
        if fmt == "png":
            # Extract color drawing and create an Alpha (Transparency) mask
            b, g, r = cv2.split(self.canvas)
            alpha = cv2.cvtColor(self.canvas, cv2.COLOR_BGR2GRAY)
            _, alpha = cv2.threshold(alpha, 1, 255, cv2.THRESH_BINARY)
            rgba = cv2.merge((b, g, r, alpha))
            cv2.imwrite(filename, rgba)
            
        elif fmt == "pdf":
            # Inject a white background before converting to PDF for clean printing
            white_bg = np.ones_like(self.canvas) * 255
            gray = cv2.cvtColor(self.canvas, cv2.COLOR_BGR2GRAY)
            _, mask = cv2.threshold(gray, 1, 255, cv2.THRESH_BINARY)
            mask_inv = cv2.bitwise_not(mask)
            
            white_bg = cv2.bitwise_and(white_bg, white_bg, mask=mask_inv)
            canvas_fg = cv2.bitwise_and(self.canvas, self.canvas, mask=mask)
            final_img = cv2.add(white_bg, canvas_fg)
            
            img_rgb = cv2.cvtColor(final_img, cv2.COLOR_BGR2RGB)
            pil_img = Image.fromarray(img_rgb)
            pil_img.save(filename, "PDF", resolution=100.0)
            
        self.last_action_time = time.time()
        print(f"[CANVAS] File saved to {filename}")