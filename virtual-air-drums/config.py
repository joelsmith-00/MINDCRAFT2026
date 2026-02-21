"""
Configuration file for Virtual Air Drums
Adjust these settings to customize your experience
"""

# ==================== CAMERA SETTINGS ====================
CAMERA_INDEX = 0  # 0 for default camera, 1, 2, etc. for other cameras
FRAME_WIDTH = 1280  # Camera resolution width
FRAME_HEIGHT = 720  # Camera resolution height

# ==================== HAND DETECTION SETTINGS ====================
MAX_HANDS = 2  # Maximum number of hands to detect (1 or 2)
DETECTION_CONFIDENCE = 0.7  # Hand detection confidence (0.0 to 1.0)
TRACKING_CONFIDENCE = 0.5  # Hand tracking confidence (0.0 to 1.0)

# ==================== GESTURE RECOGNITION SETTINGS ====================
VELOCITY_THRESHOLD = 300  # Minimum velocity for hit detection (pixels/second)
DOWNWARD_MOTION_THRESHOLD = 5  # Minimum downward pixels for hit detection
HIT_COOLDOWN = 0.3  # Minimum time between hits (seconds)
POSITION_HISTORY_SIZE = 5  # Number of positions to track for velocity calculation

# ==================== AUDIO SETTINGS ====================
AUDIO_FREQUENCY = 22050  # Audio sample rate (Hz)
AUDIO_BUFFER_SIZE = 512  # Audio buffer size (samples) - lower = less latency
VOLUME_MULTIPLIER = 2000  # Velocity to volume conversion factor

# ==================== DRUM ZONE COLORS ====================
# Colors in BGR format (Blue, Green, Red)
HIHAT_COLOR = (100, 100, 255)  # Red
SNARE_COLOR = (100, 255, 100)  # Green
BASS_COLOR = (255, 100, 100)   # Blue

# ==================== VISUAL SETTINGS ====================
SHOW_FPS = True  # Show FPS counter
SHOW_HAND_LANDMARKS = True  # Draw hand skeleton
SHOW_FINGER_INDICATOR = True  # Highlight finger tip
ZONE_TRANSPARENCY = 0.3  # Drum zone transparency (0.0 to 1.0)
HIT_FLASH_DURATION = 0.2  # How long zones stay lit after hit (seconds)

# ==================== DRUM SOUND FILES ====================
HIHAT_SOUND = "sounds/hihat.wav"
SNARE_SOUND = "sounds/snare.wav"
BASS_SOUND = "sounds/bass.wav"

# ==================== PERFORMANCE SETTINGS ====================
MIRROR_MODE = True  # Flip camera horizontally for natural interaction
TARGET_FPS = 60  # Target frame rate (actual may vary)

# ==================== ADVANCED SETTINGS ====================
# Finger landmark to track (8 = index finger tip)
# Other options: 4=thumb, 12=middle finger, 16=ring finger, 20=pinky
TRACKING_FINGER_LANDMARK = 8

# Drum zone layout (can be customized)
# Format: (name, x1, y1, x2, y2, sound_file, color)
# Coordinates are in percentages (0.0 to 1.0) of screen size
CUSTOM_ZONES = None  # Set to None to use default layout

# ==================== DEBUG SETTINGS ====================
DEBUG_MODE = False  # Print debug information
SHOW_VELOCITY = False  # Display velocity values on screen
LOG_HITS = False  # Log drum hits to console

# ==================== NOTES ====================
# - Lower VELOCITY_THRESHOLD = easier to trigger hits
# - Higher VELOCITY_THRESHOLD = need faster movements
# - Lower HIT_COOLDOWN = can hit faster (may cause double-hits)
# - Higher HIT_COOLDOWN = prevents accidental double-hits
# - Lower AUDIO_BUFFER_SIZE = less latency (may cause audio glitches)
# - Higher AUDIO_BUFFER_SIZE = more stable audio (more latency)
