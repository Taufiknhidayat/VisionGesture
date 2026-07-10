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

# =========================================================
# FINGER COUNTER CONFIGURATIONS
# =========================================================
FINGER_RATIO_THRESHOLD = 1.05
THUMB_ANGLE_THRESHOLD = 160.0
FINGER_ANGLE_THRESHOLD = 150.0
SMOOTHING_WINDOW_SIZE = 5

# =========================================================
# GESTURE ENGINE CONFIGURATIONS
# =========================================================
GESTURE_BUFFER_SIZE = 5         
GESTURE_CONFIDENCE_MIN = 0.80   

# =========================================================
# DASHBOARD CONFIGURATIONS
# =========================================================
SHOW_DASHBOARD = True
DASHBOARD_WIDTH = 320
DASHBOARD_REFRESH_RATE = 1.0    # Seconds between CPU/RAM checks (prevents lag)
DEFAULT_ACTIVE_MODULE = "Gesture Engine"