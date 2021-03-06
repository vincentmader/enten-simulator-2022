import numpy as np

PATH_TO_SPRITES = "resources/sprites"
PATH_TO_SOUNDS = "resources/sounds"

# WINDOW_SCALE = 480*2.383
# ASPECT_RATIO = 12/16
WINDOW_SCALE = 900
ASPECT_RATIO = 16/9
WINDOW_HEIGHT = WINDOW_SCALE
WINDOW_WIDTH = WINDOW_SCALE * ASPECT_RATIO
WINDOW_SIZE = np.array([WINDOW_WIDTH, WINDOW_HEIGHT])

DT = 1

INITIAL_POSITION = 0.5 * WINDOW_SIZE

SIZE_DUCK = (250, 250)
SIZE_MINIDUCK = (150, 150)
SIZE_EGG = (80, 80)

EGG_HATCH_TIME = 5000
DUCK_ACCELERATION = 2.5
DUCK_GROWUP_TIME = 5000

