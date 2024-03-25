import os
import pygame
from pygame.locals import *
import FlappyBird.settings as s
import FlappyBird.colors as fc
from FlappyBird.output import draw_matrix, draw_matrix_representation
from FlappyBird.FlappyBird import flappy_bird_game
import GeometryDash.Variables as v
from GeometryDash.Main import geometry_dash_game
from Snake.snake import snake_game

started_on_pi = True
try:
    from rgbmatrix import RGBMatrix, RGBMatrixOptions
    print("Library rgbmatrix imported successfully!")
except ImportError:
    started_on_pi = False
    print("Library rgbmatrix import failed!")

# This makes it so that gampad input can be used if window is not in focus
os.environ["SDL_JOYSTICK_ALLOW_BACKGROUND_EVENTS"] = "1"

# Configuration for the matrix
matrix = None
offset_canvas = None
if started_on_pi:
    options = RGBMatrixOptions()
    options.rows = 32
    options.chain_length = 1
    options.parallel = 1
    options.hardware_mapping = 'adafruit-hat'
    options.drop_privileges = 0# DONT DROP PRIVS!!!

    # Matrix & Canvas
    matrix = RGBMatrix(options = options)
    offset_canvas = matrix.CreateFrameCanvas()

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

# Setup screen for ALL GAMES
screen = None
if started_on_pi:
    screen = pygame.display.set_mode((s.SCREEN_WIDTH, s.SCREEN_HEIGHT))
else:
    screen = pygame.display.set_mode((s.SCREEN_WIDTH*2, s.SCREEN_HEIGHT))
pygame.display.set_caption("Startscreen")

SCREEN_HALF = s.SCREEN_WIDTH // 2
SCREEN_QUARTER = s.SCREEN_WIDTH // 4
select_box_x = 0
select_box_y = 0

run = True
while(run):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.KEYDOWN and event.key == K_LEFT:
            select_box_x = 0
        elif event.type == pygame.KEYDOWN and event.key == K_RIGHT:
            select_box_x = SCREEN_HALF
        elif event.type == pygame.KEYDOWN and event.key == K_UP:
            select_box_y = 0
        elif event.type == pygame.KEYDOWN and event.key == K_DOWN:
            select_box_y = SCREEN_HALF
        # Joypad axis motion event
        elif event.type == pygame.JOYAXISMOTION:
            if event.axis == 0:
                if event.value < -0.5:
                    select_box_x = 0
                    print("Left")
                elif event.value > 0.5:
                    select_box_x = SCREEN_HALF
                    print("Right")
            elif event.axis == 1:
                if event.value < -0.5:
                    select_box_y = 0
                    print("Up")
                elif event.value > 0.5:
                    select_box_y = SCREEN_HALF
                    print("Down")
        # Start selected Game
        elif event.type == pygame.KEYDOWN and event.key == K_RETURN:
            if(select_box_x == 0 and select_box_y == 0):
                flappy_bird_game(screen, matrix, offset_canvas)
            elif(select_box_x == 0 and select_box_y == SCREEN_HALF):
                snake_game(screen, matrix, offset_canvas)
            elif(select_box_x == SCREEN_HALF and select_box_y == 0):
                geometry_dash_game(screen, matrix, offset_canvas)
            elif(select_box_x == SCREEN_HALF and select_box_y == SCREEN_HALF):
                run = False
        # Start selected Game
        elif event.type == pygame.JOYBUTTONDOWN and event.button != 8:
            if(select_box_x == 0 and select_box_y == 0):
                flappy_bird_game(screen, matrix, offset_canvas)
            elif(select_box_x == 0 and select_box_y == SCREEN_HALF):
                snake_game(screen, matrix, offset_canvas)
            elif(select_box_x == SCREEN_HALF and select_box_y == 0):
                geometry_dash_game(screen, matrix, offset_canvas)
            elif(select_box_x == SCREEN_HALF and select_box_y == SCREEN_HALF):
                run = False

    # Flappy Bird Mockup
    pygame.draw.rect(screen, fc.DARK_SKY_BLUE, (0, 0, SCREEN_HALF, SCREEN_HALF))
    pygame.draw.rect(screen, fc.FLAPPY_ORANGE, (60, 60, s.PLAYER_WIDTH, s.PLAYER_WIDTH))# Player
    pygame.draw.rect(screen, fc.LIGHT_GREEN, (200, 0, s.PIXEL_WIDTH, SCREEN_HALF))# Pillar left
    pygame.draw.rect(screen, fc.GREEN, (200 + s.PIXEL_WIDTH, 0, s.PIXEL_WIDTH, SCREEN_HALF))# Pillar center
    pygame.draw.rect(screen, fc.DARK_GREEN, (200 + (s.PIXEL_WIDTH * 2), 0, s.PIXEL_WIDTH, SCREEN_HALF))# Pillar right
    pygame.draw.rect(screen, fc.DARK_SKY_BLUE, (200, 80, s.PILLAR_WIDTH, 80))# Pillar vertical gap
    pygame.draw.rect(screen, fc.GROUND_BROWN, (0, SCREEN_HALF - s.GROUND_HEIGHT, SCREEN_HALF, s.GROUND_HEIGHT))# Ground dirt
    pygame.draw.rect(screen, fc.LIGHT_GREEN, (0, SCREEN_HALF - s.GROUND_HEIGHT, SCREEN_HALF, s.PIXEL_WIDTH))#Grass

    # Geometry Dash Mockup
    pygame.draw.rect(screen, fc.BLACK, (SCREEN_HALF, 0, SCREEN_HALF, SCREEN_HALF))
    pygame.draw.rect(screen, v.BLUE, (SCREEN_HALF, 250, SCREEN_HALF, 100))
    pygame.draw.rect(screen, v.WHITE, (SCREEN_HALF + 120, 100, s.PLAYER_WIDTH, s.PLAYER_WIDTH))
    pygame.draw.rect(screen, v.BLUE, (SCREEN_HALF + 180, 160, 100, s.PLAYER_WIDTH))
    pygame.draw.rect(screen, v.RED, (SCREEN_HALF + s.PLAYER_WIDTH, 250, s.PLAYER_WIDTH, s.PLAYER_WIDTH))
    
    # Snake Mockup
    pygame.draw.rect(screen, fc.BLACK, (0, SCREEN_HALF, SCREEN_HALF, SCREEN_HALF))
    pygame.draw.rect(screen, (0, 255, 0), (0, SCREEN_HALF + 200, 140, s.PIXEL_WIDTH))
    pygame.draw.rect(screen, (0, 255, 0), (60, SCREEN_HALF + 160, 80, s.PIXEL_WIDTH))
    pygame.draw.rect(screen, (0, 255, 0), (60, SCREEN_HALF + 120, 160, s.PIXEL_WIDTH))
    pygame.draw.rect(screen, (0, 255, 0), (200, SCREEN_HALF + 140, s.PIXEL_WIDTH, s.PIXEL_WIDTH))
    pygame.draw.rect(screen, (0, 255, 0), (60, SCREEN_HALF + 140, s.PIXEL_WIDTH, s.PIXEL_WIDTH))
    pygame.draw.rect(screen, (0, 255, 0), (120, SCREEN_HALF + 180, s.PIXEL_WIDTH, s.PIXEL_WIDTH))
    pygame.draw.rect(screen, (255, 0, 0), (200, SCREEN_HALF + 200, s.PIXEL_WIDTH, s.PIXEL_WIDTH))

    # Off Switch
    pygame.draw.rect(screen, fc.BLACK, (SCREEN_HALF, SCREEN_HALF, SCREEN_HALF, SCREEN_HALF))
    pygame.draw.circle(screen, (255, 0, 0), (470, 471 + s.DOWNWARD_PIXEL_PULL_OFFSET), 129, s.PIXEL_WIDTH)
    pygame.draw.rect(screen, fc.BLACK, (SCREEN_HALF, SCREEN_HALF, SCREEN_HALF, 60))
    pygame.draw.rect(screen, (255, 0, 0), (SCREEN_HALF + 140, SCREEN_HALF + 40, 40, 120))

    # Select Box
    pygame.draw.rect(screen, (255, 255, 255), (select_box_x, select_box_y, SCREEN_HALF, SCREEN_HALF), s.PIXEL_WIDTH)
    #pygame.draw.rect(screen, (255, 255, 255), (SCREEN_HALF, SCREEN_HALF, SCREEN_HALF, SCREEN_HALF), s.PIXEL_WIDTH)
    
    if started_on_pi:
        draw_matrix(screen, matrix, offset_canvas)
    else:
        draw_matrix_representation(screen)
        pygame.display.update()

pygame.quit()
if started_on_pi:
    os.system("sudo shutdown -h now")