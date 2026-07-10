import cv2

from configs.colors import GREEN, CYAN, YELLOW, WHITE


class Overlay:

    @staticmethod
    def draw_title(frame):

        cv2.putText(
            frame,
            "VisionGesture",
            (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            CYAN,
            2,
        )

    @staticmethod
    def draw_fps(frame, fps):

        cv2.putText(
            frame,
            f"FPS : {fps}",
            (20, 80),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            GREEN,
            2,
        )

    @staticmethod
    def draw_hand(frame, hand):

        x, y, w, h = hand.bbox

        # Bounding Box
        cv2.rectangle(
            frame,
            (x - 10, y - 10),
            (x + w + 10, y + h + 10),
            GREEN,
            2,
        )

        # Header
        cv2.rectangle(
            frame,
            (x - 10, y - 45),
            (x + 130, y - 10),
            GREEN,
            -1,
        )

        cv2.putText(
            frame,
            hand.handedness,
            (x, y - 20),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            WHITE,
            2,
        )

        # Center Point
        cx, cy = hand.center

        cv2.circle(
            frame,
            (cx, cy),
            6,
            (0, 0, 255),
            -1,
        )

        cv2.putText(
            frame,
            f"({cx}, {cy})",
            (cx + 10, cy),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            CYAN,
            2,
        )

        # Informasi
        info_y = y + h + 25

        cv2.putText(
            frame,
            f"ID : {hand.id}",
            (x, info_y),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            YELLOW,
            2,
        )

        cv2.putText(
            frame,
            f"Fingers : {hand.fingers}",
            (x, info_y + 25),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            CYAN,
            2,
        )

        cv2.putText(
            frame,
            f"Landmarks : {len(hand.landmarks)}",
            (x, info_y + 50),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.55,
            GREEN,
            2,
        )

    @staticmethod
    def draw_total(frame, hands):

        total = sum(hand.fingers for hand in hands)

        cv2.rectangle(
            frame,
            (15, 140),
            (280, 180),
            (40, 40, 40),
            -1,
        )

        cv2.putText(
            frame,
            f"TOTAL FINGERS : {total}",
            (25, 168),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0, 255, 0),
            2,
        )