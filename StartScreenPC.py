import os
import pygame
from pygame.locals import *
import FlappyBird.settings as s
import FlappyBird.colors as fc
from FlappyBird.output import draw_matrix_representation
from FlappyBird.FlappyBird import flappy_bird_game
import GeometryDash.Variables as v
from GeometryDash.Main import geometry_dash_game
from Snake.snake import snake_game

# This makes it so that gampad input can be used if window is not in focus
os.environ["SDL_JOYSTICK_ALLOW_BACKGROUND_EVENTS"] = "1"

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
screen = pygame.display.set_mode((s.SCREEN_WIDTH*2, s.SCREEN_HEIGHT))
pygame.display.set_caption("Startscreen")

SCREEN_HALF = s.SCREEN_WIDTH // 2
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
        # Stop game and go to game select
        elif event.type == pygame.KEYDOWN and event.key == K_RETURN:
            if(select_box_x == 0 and select_box_y == 0):
                flappy_bird_game(screen)
            elif(select_box_x == 0 and select_box_y == SCREEN_HALF):
                snake_game(screen)
            elif(select_box_x == SCREEN_HALF and select_box_y == 0):
                geometry_dash_game(screen)
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
    pygame.draw.rect(screen, v.GREEN, (SCREEN_HALF, SCREEN_HALF - v.GROUND, SCREEN_HALF, v.GROUND))
    pygame.draw.rect(screen, v.RED, (SCREEN_HALF + 60, 180, s.PLAYER_WIDTH, s.PLAYER_WIDTH))

    # Snake Mockup
    pygame.draw.rect(screen, fc.BLACK, (0, SCREEN_HALF, SCREEN_HALF, SCREEN_HALF))

    # Off Switch
    pygame.draw.rect(screen, fc.BLACK, (SCREEN_HALF, SCREEN_HALF, SCREEN_HALF, SCREEN_HALF))

    # Select Box
    pygame.draw.rect(screen, (255, 255, 255), (select_box_x, select_box_y, SCREEN_HALF, SCREEN_HALF), s.PIXEL_WIDTH)
    
    draw_matrix_representation(screen)
    pygame.display.update()

pygame.quit()
