##! /usr/bin/env python3
import os
import pygame
from pygame.locals import *
# from rgbmatrix import RGBMatrix, RGBMatrixOptions
import FlappyBird


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

# Setup screen
screen = pygame.display.set_mode((s.SCREEN_WIDTH*2, s.SCREEN_HEIGHT))
pygame.display.set_caption("Flappy Bird")