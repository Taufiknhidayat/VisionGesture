import cv2
import psutil
import time
from typing import List
from configs.colors import COLORS
from configs.settings import FRAME_HEIGHT, DASHBOARD_WIDTH, DASHBOARD_REFRESH_RATE
from src.visiongesture.models.hand import Hand

class Dashboard:
    def __init__(self):
        self.font = cv2.FONT_HERSHEY_SIMPLEX
        self.last_sys_check = time.time()
        self.cpu_usage = 0.0
        self.ram_usage = 0.0
        
        # Initialize psutil to avoid blocking on first call
        psutil.cpu_percent()

    def _update_system_stats(self) -> None:
        """Asynchronously updates CPU and RAM usage to prevent frame drops."""
        current_time = time.time()
        if current_time - self.last_sys_check > DASHBOARD_REFRESH_RATE:
            self.cpu_usage = psutil.cpu_percent()
            self.ram_usage = psutil.virtual_memory().percent
            self.last_sys_check = current_time

    def draw(self, frame, hands: List[Hand], fps: int, active_module: str) -> None:
        """Renders the dashboard side panel onto the frame."""
        self._update_system_stats()
        
        # Draw dark semi-transparent side panel
        overlay = frame.copy()
        cv2.rectangle(overlay, (0, 0), (DASHBOARD_WIDTH, FRAME_HEIGHT), (15, 15, 15), -1)
        cv2.addWeighted(overlay, 0.85, frame, 0.15, 0, frame)
        
        # Draw accent border line
        cv2.line(frame, (DASHBOARD_WIDTH, 0), (DASHBOARD_WIDTH, FRAME_HEIGHT), COLORS["CYAN"], 2)

        # ---------------------------------------------------------
        # HEADER SECTION
        # ---------------------------------------------------------
        cv2.putText(frame, "VISION GESTURE", (20, 40), self.font, 0.8, COLORS["WHITE"], 2, cv2.LINE_AA)
        cv2.putText(frame, f"MODULE : {active_module}", (20, 70), self.font, 0.5, COLORS["YELLOW"], 1, cv2.LINE_AA)

        # ---------------------------------------------------------
        # SYSTEM PERFORMANCE SECTION
        # ---------------------------------------------------------
        cv2.putText(frame, "--- SYSTEM STATUS ---", (20, 115), self.font, 0.5, COLORS["CYAN"], 1, cv2.LINE_AA)
        
        fps_color = COLORS["GREEN"] if fps > 30 else COLORS["RED"]
        cv2.putText(frame, f"FPS    : {fps}", (20, 150), self.font, 0.6, fps_color, 2, cv2.LINE_AA)
        
        cpu_color = COLORS["RED"] if self.cpu_usage > 80 else COLORS["WHITE"]
        cv2.putText(frame, f"CPU    : {self.cpu_usage}%", (20, 180), self.font, 0.6, cpu_color, 1, cv2.LINE_AA)
        
        ram_color = COLORS["RED"] if self.ram_usage > 85 else COLORS["WHITE"]
        cv2.putText(frame, f"RAM    : {self.ram_usage}%", (20, 210), self.font, 0.6, ram_color, 1, cv2.LINE_AA)
        
        cv2.putText(frame, "CAMERA : ACTIVE", (20, 240), self.font, 0.6, COLORS["GREEN"], 1, cv2.LINE_AA)

        # ---------------------------------------------------------
        # GESTURE TRACKING SECTION
        # ---------------------------------------------------------
        cv2.putText(frame, "--- GESTURE STATUS ---", (20, 295), self.font, 0.5, COLORS["CYAN"], 1, cv2.LINE_AA)
        
        y_offset = 330
        if not hands:
            cv2.putText(frame, "No hands detected.", (20, y_offset), self.font, 0.5, (150, 150, 150), 1, cv2.LINE_AA)
        else:
            for hand in hands:
                hand_color = COLORS["CYAN"] if hand.handedness == "Right" else COLORS["YELLOW"]
                header_text = f"[{hand.handedness.upper()}] Hand ID: {hand.id}"
                
                cv2.putText(frame, header_text, (20, y_offset), self.font, 0.6, hand_color, 1, cv2.LINE_AA)
                
                # Fetch gesture data
                gesture_name = hand.gesture.state.value if hand.gesture else "Unknown"
                conf = int(hand.gesture.confidence * 100) if hand.gesture else 0
                fingers = hand.fingers
                
                # Render metrics
                cv2.putText(frame, f"Gesture : {gesture_name}", (20, y_offset + 25), self.font, 0.55, COLORS["WHITE"], 1, cv2.LINE_AA)
                cv2.putText(frame, f"Conf    : {conf}%", (20, y_offset + 50), self.font, 0.55, COLORS["WHITE"], 1, cv2.LINE_AA)
                cv2.putText(frame, f"Fingers : {fingers}", (20, y_offset + 75), self.font, 0.55, COLORS["WHITE"], 1, cv2.LINE_AA)
                
                y_offset += 120

        return frame