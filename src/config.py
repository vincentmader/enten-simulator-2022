import numpy as np

PATH_TO_SPRITES = "../resources/sprites"
PATH_TO_SOUNDS = "../resources/sounds"

# WINDOW_SCALE = 480*2.383
# ASPECT_RATIO = 12/16
WINDOW_SCALE = 900
ASPECT_RATIO = 16/9
WINDOW_HEIGHT = WINDOW_SCALE
WINDOW_WIDTH = WINDOW_SCALE * ASPECT_RATIO
WINDOW_SIZE = np.array([WINDOW_WIDTH, WINDOW_HEIGHT])

POND_CENTER = np.array([WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2])
POND_RADIUS_X = 420
POND_RADIUS_Y = 300

DT = 1

INITIAL_POSITION = 0.5 * WINDOW_SIZE

SIZE_DUCK = (250, 250)
SIZE_MINIDUCK = (150, 150)
SIZE_EGG = (80, 80)

EGG_HATCH_TIME = 5000
DUCK_ACCELERATION = 2.5
DUCK_GROWUP_TIME = 5000

SPLASH_FRAME_COUNT = 10   # ripple frames
SPLASH_FRAME_SPEED = 3    # game ticks per ripple frame
SPLASH_SIZE_LARGE  = (420, 168)   # entry   — 2.5:1 ratio
SPLASH_SIZE_MEDIUM = (280, 112)   # exit    — 2.5:1 ratio

WAKE_FRAME_COUNT   = 8    # wake frames
WAKE_FRAME_SPEED   = 2    # game ticks per wake frame (faster)
SPLASH_SIZE_WAKE   = (280, 112)   # movement wake — 2.5:1 ratio

SPLASH_INTERVAL    = 12   # game ticks between wake particle pairs

