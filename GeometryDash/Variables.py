# Screen variables
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 640
GROUND = 120
PLAYERSIZE = 40
OBSTICALSIZE = 40
PLAYERX = 200
PIXLESIZE = 20

# Colors
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)

# Player variables
player_pos = SCREEN_HEIGHT/2
player_vel = 0
gravity = 25
lift = -10

# Map variabels
mapStartLength = PLAYERX + 500
mapSpeed = 5 # bigger = faster
obsticalGround = SCREEN_HEIGHT - GROUND - OBSTICALSIZE
drawingPoint = 0 #dictates the point the map is at
drawingPointevery40 = 0 #makes so drawing point only gets increased every 40 instences
partSize = 16 #size of the parts (16x16)
floorLevel = 1
on_ground = False

mapPartOne = [ # 0= air, 1= wall, 2= death 
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],       # 1.
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 1, 1, 2, 2, 1]        # In Ground
]
mapPartTwo = [ # 0= air, 1= wall, 2= death 
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1],       # 1.
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 1, 1]        # In Ground
]
mapOne = [mapPartOne,mapPartTwo,mapPartOne,mapPartOne,mapPartTwo]

#Score Variables
# This represents the numbers for the scoring system as an array
SCORE_POSITION_Y = PIXLESIZE# One Pixel down
SCORE_POSITION_X = (SCREEN_WIDTH // 2) - (4 * PIXLESIZE)

SCORE = [None] * 11
SCORE[0] = [[1, 1, 1],[1, 0, 1],[1, 0, 1],[1, 0, 1],[1, 1, 1]]
SCORE[1] = [[0, 0, 1],[0, 0, 1],[0, 0, 1],[0, 0, 1],[0, 0, 1]]
SCORE[2] = [[1, 1, 1],[0, 0, 1],[1, 1, 1],[1, 0, 0],[1, 1, 1]]
SCORE[3] = [[1, 1, 1],[0, 0, 1],[1, 1, 1],[0, 0, 1],[1, 1, 1]]
SCORE[4] = [[1, 0, 1],[1, 0, 1],[1, 1, 1],[0, 0, 1],[0, 0, 1]]
SCORE[5] = [[1, 1, 1],[1, 0, 0],[1, 1, 1],[0, 0, 1],[1, 1, 1]]
SCORE[6] = [[1, 1, 1],[1, 0, 0],[1, 1, 1],[1, 0, 1],[1, 1, 1]]
SCORE[7] = [[1, 1, 1],[0, 0, 1],[0, 0, 1],[0, 0, 1],[0, 0, 1]]
SCORE[8] = [[1, 1, 1],[1, 0, 1],[1, 1, 1],[1, 0, 1],[1, 1, 1]]
SCORE[9] = [[1, 1, 1],[1, 0, 1],[1, 1, 1],[0, 0, 1],[1, 1, 1]]
SCORE[10] = [[1, 0, 1],[0, 0, 1],[0, 1, 0],[1, 0, 0],[1, 0, 1]] # %
