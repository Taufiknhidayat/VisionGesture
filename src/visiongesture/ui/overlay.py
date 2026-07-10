# src/visiongesture/ui/overlay.py
import cv2
import numpy as np
from configs.colors import COLORS

class Overlay:
    def __init__(self):
        # Konfigurasi font standar industri
        self.font = cv2.FONT_HERSHEY_SIMPLEX
        self.font_scale_labels = 0.55
        self.font_scale_values = 0.6
        self.thickness = 2
        
    def _draw_transparent_panel(self, frame, x, y, w, h, alpha=0.65):
        """Membuat background panel semi-transparan yang elegan."""
        overlay = frame.copy()
        # Menggunakan warna gelap modern (hampir hitam) untuk HUD
        cv2.rectangle(overlay, (x, y), (x + w, y + h), (20, 20, 20), -1)
        cv2.addWeighted(overlay, alpha, frame, 1 - alpha, 0, frame)
        # Tambahkan border tipis di sekeliling panel
        cv2.rectangle(frame, (x, y), (x + w, y + h), (60, 60, 60), 1)

    def _draw_modern_bbox(self, frame, bbox, color, length=15, t=2):
        """Menggambar bounding box dengan sudut kustom yang minimalis."""
        x, y, w, h = bbox
        # Kotak tipis utama
        cv2.rectangle(frame, (x, y), (x + w, y + h), color, 1)
        
        # Sisi Pojok Kiri Atas
        cv2.line(frame, (x, y), (x + length, y), color, t)
        cv2.line(frame, (x, y), (x, y + length), color, t)
        # Sisi Pojok Kanan Atas
        cv2.line(frame, (x + w, y), (x + w - length, y), color, t)
        cv2.line(frame, (x + w, y), (x + w, y + length), color, t)
        # Sisi Pojok Kiri Bawah
        cv2.line(frame, (x, y + h), (x + length, y + h), color, t)
        cv2.line(frame, (x, y + h), (x, y + h - length), color, t)
        # Sisi Pojok Kanan Bawah
        cv2.line(frame, (x + w, y + h), (x + w - length, y + h), color, t)
        cv2.line(frame, (x + w, y + h), (x + w, y + h - length), color, t)

    def draw(self, frame, hands, fps):
        # =========================================================
        # 1. RENDER TOP HUD PANEL (INFO FPS & TOTAL JARI GLOBAL)
        # =========================================================
        self._draw_transparent_panel(frame, 20, 20, 260, 50, alpha=0.7)
        
        # Teks FPS
        cv2.putText(frame, "SYSTEM PERF :", (35, 48), self.font, self.font_scale_labels, (150, 150, 150), 1)
        fps_color = COLORS["GREEN"] if fps > 30 else COLORS["RED"]
        cv2.putText(frame, f"{fps} FPS", (150, 49), self.font, self.font_scale_values, fps_color, self.thickness)

        # Total Jari Terdeteksi
        total_all_fingers = sum([hand.fingers for hand in hands if hand.fingers is not None])
        cv2.putText(frame, "TOTAL FINGERS :", (35, 63), self.font, self.font_scale_labels, (150, 150, 150), 1)
        cv2.putText(frame, f"{total_all_fingers}", (170, 64), self.font, self.font_scale_values, COLORS["CYAN"], self.thickness)

        # =========================================================
        # 2. RENDER HAND TRACKING OVERLAY (DURANTE DETECTION)
        # =========================================================
        for hand in hands:
            if not hand.landmarks:
                continue

            # Tentukan warna tema berdasarkan label tangan (Kanan = Cyan, Kiri = Magenta/Kuning)
            is_right = hand.handedness == "Right"
            theme_color = COLORS["CYAN"] if is_right else COLORS["YELLOW"]
            hand_label = "RIGHT HAND" if is_right else "LEFT HAND"

            # Hubungkan garis antar sendi (Gunakan ketebalan tipis agar terlihat clean)
            connections = [
                (0, 1), (1, 2), (2, 3), (3, 4),      # Jempol
                (0, 5), (5, 6), (6, 7), (7, 8),      # Telunjuk
                (5, 9), (9, 10), (10, 11), (11, 12), # Tengah
                (9, 13), (13, 14), (14, 15), (15, 16),# Manis
                (13, 17), (17, 18), (18, 19), (19, 20),# Kelingking
                (0, 17)                              # Telapak Bawah
            ]
            
            for p1_id, p2_id in connections:
                p1 = (int(hand.landmarks[p1_id].x * frame.shape[1]), int(hand.landmarks[p1_id].y * frame.shape[0]))
                p2 = (int(hand.landmarks[p2_id].x * frame.shape[1]), int(hand.landmarks[p2_id].y * frame.shape[0]))
                cv2.line(frame, p1, p2, (230, 230, 230), 1)

            # Gambar titik sendi (Landmarks)
            for lm in hand.landmarks:
                cx, cy = int(lm.x * frame.shape[1]), int(lm.y * frame.shape[0])
                cv2.circle(frame, (cx, cy), 4, theme_color, -1)
                cv2.circle(frame, (cx, cy), 5, (255, 255, 255), 1)

            # Render Bounding Box Modern dan Info Tangan di atas objek
            if hand.bbox:
                x, y, w, h = hand.bbox
                self._draw_modern_bbox(frame, hand.bbox, theme_color, length=12, t=2)

	    # Floating Info Box kecil di atas Bounding Box
                info_y = y - 10 if y - 10 > 20 else y + h + 20
                
                # Format string text info
                hand_info_text = f"[{hand_label[0]}] Fg: {hand.fingers}"
                
                # Buat background mini untuk teks info mengambang
                cv2.rectangle(frame, (x, info_y - 15), (x + 110, info_y + 5), (20, 20, 20), -1)
                cv2.rectangle(frame, (x, info_y - 15), (x + 110, info_y + 5), theme_color, 1)
                
                # PERBAIKAN: Mengubah info_y5 menjadi info_y - 2 agar koordinatnya valid
                cv2.putText(frame, hand_info_text, (x + 5, info_y - 2), 
                            self.font, 0.45, (255, 255, 255), 1, cv2.LINE_AA)

        return frame