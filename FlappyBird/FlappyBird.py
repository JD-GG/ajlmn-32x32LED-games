##! /usr/bin/env python3
import os
import pygame
from pygame.locals import *
from mapGeneration import init_pillar_pos_x, init_pillar_pos_y, get_random_pos_y
from output import draw_screen, draw_matrix, draw_matrix_representation, draw_hitboxes, draw_matrix_grid, draw_position_markers
import settings as s
"""from rgbmatrix import RGBMatrix, RGBMatrixOptions

# This makes it so that gampad input can be used if window is not in focus
os.environ["SDL_JOYSTICK_ALLOW_BACKGROUND_EVENTS"] = "1"

# Configuration for the matrix
options = RGBMatrixOptions()
options.rows = 32
options.chain_length = 1
options.parallel = 1
options.hardware_mapping = 'adafruit-hat'
options.drop_privileges = 0# DONT DROP PRIVS!!!

# Matrix & Canvas
matrix = RGBMatrix(options = options)
offset_canvas = matrix.CreateFrameCanvas()"""

# Init
pygame.init()
pygame.joystick.init()

# Check for available gamepads
joysticks = [pygame.joystick.Joystick(i) for i in range(pygame.joystick.get_count())]
if not joysticks:
    print("No gamepads detected.")

for joystick in joysticks:
    joystick.init()
    print(f"Detected Gamepad: {joystick.get_name()}")

# Setup screen
screen = pygame.display.set_mode((s.SCREEN_WIDTH*2, s.SCREEN_HEIGHT))
pygame.display.set_caption("Flappy Bird")

# Setup different screen halfes
changing_screen = (0, 0, s.SCREEN_WIDTH, s.SCREEN_HEIGHT)
changing_matrix_screen = (s.SCREEN_WIDTH, 0, s.SCREEN_WIDTH, s.SCREEN_HEIGHT)

# Pilar Variables
pillar_pos_y = [None] * s.PILLAR_COUNT
pillar_pos_x = [None] * s.PILLAR_COUNT
pillar_vel = 0

# Bird variables
player_pos_x = 0
player_pos_y = 0
player_vel = 0
gravity = 15
lift = -6

# Hitbox Rectangle Arrays for drawing
Rect = pygame.Rect# Collsision hitbox
player_hitbox = Rect(0, 0, 0, 0)
pillar_hitbox_top = [Rect(0, 0, 0, 0)] * s.PILLAR_COUNT
pillar_hitbox_bottom = [Rect(0, 0, 0, 0)] * s.PILLAR_COUNT
pillar_hitbox_score = [Rect(0, 0, 0, 0)] * s.PILLAR_COUNT

# Additional variables (self explanatory)
clock = pygame.time.Clock()
game_started = False
run = True
enable_input = True
score = 0
first_time = True

def initFlappyGlobals():
    global enable_input
    global player_pos_x
    global player_pos_y
    global player_vel
    global pillar_pos_y
    global pillar_pos_x
    global pillar_vel
    global score
    global first_time
    enable_input = True
    player_pos_x = 80
    player_pos_y = 100
    player_vel = lift
    pillar_pos_y = init_pillar_pos_y()
    pillar_pos_x = init_pillar_pos_x()
    pillar_vel = 2
    score = 0
    first_time = True

initFlappyGlobals()
while run:
    # Player Physics
    tickTime = clock.tick(60) / 1000  
    player_vel += gravity * tickTime  
    player_pos_y += player_vel

    # Pillar Physics
    for i in range(s.PILLAR_COUNT):
        pillar_pos_x[i] -= pillar_vel# Move object based on frames just like the old days
        if pillar_pos_x[i] <= 0 - s.PILLAR_WIDTH:
            first_time = True
            pillar_pos_x[i] += (s.PILLAR_WIDTH * s.PILLAR_COUNT) + (s.PILLAR_GAP_WIDTH * s.PILLAR_COUNT)# Reset pillar to the other side
            pillar_pos_y[i] = get_random_pos_y()# Get new random height
    
    # Edgecases
    if player_pos_y < 0:# Top
        player_pos_y = 0
        
    if player_pos_y > s.SCREEN_HEIGHT - s.PLAYER_WIDTH - s.GROUND_HEIGHT:# Bottom (kill player)
        player_pos_y = s.SCREEN_HEIGHT - s.PLAYER_WIDTH - s.GROUND_HEIGHT
        pillar_vel = 0# Stop Pillars
        enable_input = False# Disable input
    
    # Pillar kolision
    player_rect = Rect(player_pos_x, player_pos_y, s.PLAYER_WIDTH, s.PILLAR_WIDTH)
    player_hitbox = player_rect
    for i in range(s.PILLAR_COUNT):
        pillar_top_height_y = pillar_pos_y[i] - s.PILLAR_HEIGHT
        pillar_bottom_height = s.SCREEN_HEIGHT - pillar_pos_y[i]
        pillar_rect_top = Rect(pillar_pos_x[i], 0, s.PILLAR_WIDTH, pillar_top_height_y )
        pillar_rect_bottom = Rect(pillar_pos_x[i], pillar_pos_y[i], s.PILLAR_WIDTH, pillar_bottom_height )
         
        pillar_hitbox_top[i] = pillar_rect_top
        pillar_hitbox_bottom[i] = pillar_rect_bottom

        if player_rect.colliderect(pillar_rect_bottom):
            pillar_vel = 0
            enable_input = False# Disable input
        elif player_rect.colliderect(pillar_rect_top):
            pillar_vel = 0 
            enable_input = False# Disable input

    # Score increment
    for i in range(s.PILLAR_COUNT):
        pillar_top_height_y = pillar_pos_y[i] - s.PILLAR_HEIGHT
        gap_rect = Rect(pillar_pos_x[i] + s.PIXEL_WIDTH, pillar_top_height_y, s.PIXEL_WIDTH, s.PILLAR_HEIGHT)

        pillar_hitbox_score[i] = gap_rect

        if player_rect.colliderect(gap_rect):
            if first_time == True:
                score+= 1
                first_time = False

    # Event listeners
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.KEYDOWN and event.key == K_SPACE and enable_input:
            player_vel = lift
            #score += 1# This has to be changed
        elif event.type == pygame.JOYBUTTONDOWN and enable_input:# Handle gamepad Button press
            player_vel = lift
        # Space pressed when dead
        elif event.type == pygame.KEYDOWN and event.key == K_SPACE and not enable_input and player_pos_y == s.PLAYER_ON_GROUND_Y:
            initFlappyGlobals()

        # NOT SELECT button pressed when dead
        elif event.type == pygame.JOYBUTTONDOWN and event.button != 8 and not enable_input and player_pos_y == s.PLAYER_ON_GROUND_Y:
            initFlappyGlobals()

    # Drawing
    draw_screen(screen, player_pos_x, player_pos_y, pillar_pos_x, pillar_pos_y, score)
    # offset_canvas = draw_matrix(screen, matrix, offset_canvas)
    draw_matrix_representation(screen)
    draw_hitboxes(screen, player_hitbox, pillar_pos_x, pillar_hitbox_top, pillar_hitbox_score, pillar_hitbox_bottom)
    draw_matrix_grid(screen)
    draw_position_markers(screen, player_pos_x, player_pos_y, pillar_pos_x, pillar_pos_y)# Drawing markers after matrix conversion so they won't show up in the image
    
    pygame.display.update()# Update everything. What is being shown is not what is going to be given to the matrix. 

pygame.quit()
