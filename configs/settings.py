APP_NAME = "VisionGesture"
CAMERA_INDEX = 0

FRAME_WIDTH = 1280
FRAME_HEIGHT = 720
FPS = 60

MAX_HANDS = 2
DETECTION_CONFIDENCE = 0.7
TRACKING_CONFIDENCE = 0.6
SHOW_FPS = True
MIRROR_CAMERA = True

# Poin 1: Ratio Threshold untuk 4 Jari Utama
FINGER_RATIO_THRESHOLD = 1.05  

# Poin 2 & 5: Sudut Kelurusan Jari dalam Derajat (Angle Thresholds)
THUMB_ANGLE_THRESHOLD = 160.0   # Sudut CMC-MCP-IP-TIP untuk jempol
FINGER_ANGLE_THRESHOLD = 150.0  # Sudut MCP-PIP-DIP-TIP untuk jari lain

# Poin 7: Jendela Riwayat Frame untuk Anti-Flicker (Smoothing Window)
SMOOTHING_WINDOW_SIZE = 5