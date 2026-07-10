import math
from collections import deque
from configs.settings import (
    FINGER_RATIO_THRESHOLD,
    THUMB_ANGLE_THRESHOLD,
    FINGER_ANGLE_THRESHOLD,
    SMOOTHING_WINDOW_SIZE
)

class FingerCounter:
    def __init__(self):
        # Poin 7: History queue untuk filter anti-flicker (disimpan per Hand ID)
        self.history_buffers = {}

    def calculate_distance(self, p1, p2):
        """Poin 9: Menghitung jarak Euclidean antara dua landmark."""
        return math.hypot(p1.x - p2.x, p1.y - p2.y)

    def calculate_angle(self, p1, p2, p3):
        """Poin 5 & 9: Menghitung sudut dalam derajat di joint p2 antara p1 dan p3."""
        try:
            a = math.hypot(p2.x - p3.x, p2.y - p3.y)
            b = math.hypot(p1.x - p3.x, p1.y - p3.y)
            c = math.hypot(p1.x - p2.x, p1.y - p2.y)
            # Hukum Cosinus
            angle = math.acos((a**2 + c**2 - b**2) / (2 * a * c))
            return math.degrees(angle)
        except (ValueError, ZeroDivisionError):
            return 0.0

    def calculate_orientation(self, lm):
        """Poin 4 & 9: Deteksi orientasi telapak tangan berdasarkan geometri sendi."""
        wrist = lm[0]
        mcp_middle = lm[9]
        mcp_index = lm[5]
        mcp_pinky = lm[17]

        # Vektor dasar telapak tangan
        palm_y = mcp_middle.y - wrist.y
        palm_x = mcp_middle.x - wrist.x

        # Tentukan arah dominan berdasarkan pergeseran koordinat
        if abs(palm_x) > abs(palm_y):
            return "Palm Left" if palm_x < 0 else "Palm Right"
        else:
            if palm_y > 100:  # Posisi tangan terbalik ke bawah
                return "Palm Down"
            
            # Deteksi hadap depan/belakang berdasarkan urutan index ke pinky
            if mcp_index.x < mcp_pinky.x:
                return "Palm Front"
            else:
                return "Palm Back"

    def count_thumb(self, lm, orientation, handedness):
        """Poin 2 & 9: Deteksi Jempol V2 menggunakan perpaduan Sudut Joint dan Jarak Horizontal."""
        # Kombinasi Sudut CMC (1) -> MCP (2) -> IP (3) -> TIP (4)
        angle = self.calculate_angle(lm[1], sys_mcp := lm[2], lm[4])
        
        # Jarak relatif ujung jempol ke pangkal jari telunjuk
        dist_thumb_to_index = self.calculate_distance(lm[4], lm[5])
        dist_mcp_to_index = self.calculate_distance(lm[2], lm[5])

        # Jempol terbuka jika sudut sendinya rileks lurus atau jaraknya menjauh dari telapak
        if angle > THUMB_ANGLE_THRESHOLD or dist_thumb_to_index > dist_mcp_to_index * 1.1:
            return 1
        return 0

    def count_fingers(self, lm):
        """Poin 1, 5, & 9: Deteksi 4 jari menggunakan kombinasi Adaptive Ratio & Joint Angle."""
        states = []
        # Pasangan landmark untuk Telunjuk, Tengah, Manis, Kelingking
        # Format: (MCP, PIP, DIP, TIP)
        finger_joints = [
            (5, 6, 7, 8),     # Index
            (9, 10, 11, 12),  # Middle
            (13, 14, 15, 16), # Ring
            (17, 18, 19, 20)  # Pinky
        ]

        wrist = lm[0]

        for mcp, pip, dip, tip in finger_joints:
            # 1. Analisis Berbasis Jarak Adaptif (Adaptive Ratio)
            dist_wrist_to_tip = self.calculate_distance(wrist, lm[tip])
            dist_wrist_to_pip = self.calculate_distance(wrist, lm[pip])
            ratio = dist_wrist_to_tip / dist_wrist_to_pip

            # 2. Analisis Berbasis Sudut Kelurusan Joint (Joint Angle)
            angle = self.calculate_angle(lm[mcp], lm[pip], lm[tip])

            # Jika memenuhi rasio rentang atau sudut sendi menyatakan lurus terbuka
            if ratio > FINGER_RATIO_THRESHOLD or angle > FINGER_ANGLE_THRESHOLD:
                states.append(1)
            else:
                states.append(0)
                
        return states

    def count(self, hand):
        """Poin 9: Fungsi orchestrator utama untuk mengkalkulasi seluruh state tangan."""
        lm = hand.landmarks
        if not lm:
            return 0

        # 1. Tentukan Orientasi Telapak Tangan
        hand.orientation = self.calculate_orientation(lm)

        # 2. Hitung State Masing-masing Jari
        thumb_state = self.count_thumb(lm, hand.orientation, hand.handedness)
        four_finger_states = self.count_fingers(lm)

        # Poin 3: Gabungkan ke dalam susunan finger_state array [Thumb, Index, Middle, Ring, Pinky]
        current_finger_state = [thumb_state] + four_finger_states
        hand.finger_state = current_finger_state

        # 3. Poin 7: Terapkan Filter Anti-Flicker Berbasis History Buffer per Hand ID
        hand_key = f"{hand.id}_{hand.handedness}"
        if hand_key not in self.history_buffers:
            self.history_buffers[hand_key] = deque(maxlen=SMOOTHING_WINDOW_SIZE)

        # Masukkan hasil frame saat ini ke dalam buffer riwayat
        self.history_buffers[hand_key].append(current_finger_state)

        # Lakukan voting mayoritas (smoothing filter) untuk menentukan keputusan final
        smoothed_state = []
        history_list = list(self.history_buffers[hand_key])
        total_frames_tracked = len(history_list)

        for i in range(5):
            # Hitung berapa kali jari tertentu bernilai 1 di dalam window riwayat
            ones_count = sum(frame_state[i] for frame_state in history_list)
            # Jika muncul di lebih dari setengah total frame riwayat, anggap terbuka (1)
            smoothed_state.append(1 if ones_count > total_frames_tracked / 2 else 0)

        # Override state final yang telah di-smooth ke objek Hand
        hand.finger_state = smoothed_state
        hand.fingers = sum(smoothed_state)

        return hand.fingers