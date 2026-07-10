import math


class FingerCounter:

    TIP_IDS = [4, 8, 12, 16, 20]
    PIP_IDS = [3, 6, 10, 14, 18]

    def distance(self, p1, p2):
        return math.hypot(p1.x - p2.x, p1.y - p2.y)

    def count(self, hand):

        lm = hand.landmarks

        fingers = 0

        # ===== THUMB =====
        if hand.handedness == "Right":
            if lm[4].x < lm[3].x:
                fingers += 1
        else:
            if lm[4].x > lm[3].x:
                fingers += 1

        # ===== INDEX =====
        if lm[8].y < lm[6].y:
            fingers += 1

        # ===== MIDDLE =====
        if lm[12].y < lm[10].y:
            fingers += 1

        # ===== RING =====
        if lm[16].y < lm[14].y:
            fingers += 1

        # ===== PINKY =====
        if lm[20].y < lm[18].y:
            fingers += 1

        hand.fingers = fingers

        return fingers