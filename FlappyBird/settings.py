# This file stores setting to be used in all modules.
# Get a setting by using importName.setting

# All variables that have anything to do with diplaying should be multiples of 20 to represent the actual pixels on the matrix
SCREEN_WIDTH = 640# The screen has to be seen as 32 20x20 pixels
SCREEN_HEIGHT = 640
PLAYER_WIDTH = 40# This is eqvalent to 2 pixels on the matrix
PILLAR_COUNT = 4
PILLAR_WIDTH = 60# This is eqvalent to 3 pixels on the matrix
PILLAR_HEIGHT = 140# This is the gap the bird has to go through
PILLAR_GAP_WIDTH = 160# This is the horizontal gap between the pillars
GROUND_HEIGHT = 80
PIXEL_WIDTH = 20# Single pixel
SCORE_POSITION_Y = PIXEL_WIDTH# One Pixel down

# Calculated Globals (please don't touch)
PILLAR_HEIGHT_PIXELS = PILLAR_HEIGHT // PIXEL_WIDTH# // is integer division
GROUND_HEIGHT_PIXELS = GROUND_HEIGHT // PIXEL_WIDTH
SCORE_POSITION_X = (SCREEN_WIDTH // 2) - (4 * PIXEL_WIDTH)
PLAYER_ON_GROUND_Y = SCREEN_HEIGHT - GROUND_HEIGHT - PLAYER_WIDTH
