import os
import pygame
from pygame.locals import *
import FlappyBird.settings as s
from FlappyBird.FlappyBird import flappy_bird_game
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
#screen = pygame.display.set_mode((s.SCREEN_WIDTH, s.SCREEN_HEIGHT))
screen = pygame.display.set_mode((s.SCREEN_WIDTH*2, s.SCREEN_HEIGHT))
pygame.display.set_caption("Startscreen")

# Logic to select game can go right here
flappy_bird_game(screen)
geometry_dash_game(screen)
snake_game(screen)
flappy_bird_game(screen)

pygame.quit()
