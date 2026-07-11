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
# TRACKING & MOTION CONFIGURATIONS
# =========================================================
TRACKER_MAX_DISAPPEARED = 10    # Frames to wait before dropping a lost hand
TRACKER_MAX_DISTANCE = 150      # Max pixel distance for Hungarian matching
MOTION_HISTORY_SIZE = 15        # Queue size for motion path
SWIPE_THRESHOLD = 80            # Minimum pixel movement to trigger a swipe
ZOOM_SENSITIVITY = 15           # Minimum distance change to trigger zoom

# =========================================================
# DASHBOARD CONFIGURATIONS
# =========================================================
SHOW_DASHBOARD = True
DASHBOARD_WIDTH = 320
DASHBOARD_REFRESH_RATE = 1.0
DEFAULT_ACTIVE_MODULE = "Tracking Engine"