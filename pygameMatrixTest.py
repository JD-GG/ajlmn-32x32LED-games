#! /usr/bin/env python3
import sys
import pygame
from rgbmatrix import RGBMatrix, RGBMatrixOptions

# Configuration for the matrix
options = RGBMatrixOptions()
options.rows = 32
options.chain_length = 1
options.parallel = 1
options.hardware_mapping = 'adafruit-hat'# Important don't forget
options.drop_privileges = 0# Random Python guy said this would help

matrix = RGBMatrix(options = options)

offset_canvas = matrix.CreateFrameCanvas()

for y in range(32):
    for x in range(32):
        offset_canvas.SetPixel(x, y, 255, 0, 0)
        offset_canvas = matrix.SwapOnVSync(offset_canvas)

offset_canvas.Clear()
offset_canvas = matrix.SwapOnVSync(offset_canvas)
print("output red")

#-------------------------------Detect gampeads after matrix test-------------------------------------------

# Init
pygame.init()
print("pygame initialized")
pygame.joystick.init()
print("joystick initialized")

# Check for available gamepads
joysticks = [pygame.joystick.Joystick(i) for i in range(pygame.joystick.get_count())]
if not joysticks:
    print("No gamepads detected")

for joystick in joysticks:
    joystick.init()
    print(f"Detected Gamepad: {joystick.get_name()}")

# Setup screen
screen = pygame.display.set_mode((640, 640))
print("screen set mode")
pygame.display.set_caption("Screen Test")
print("screen set caption")

# Main loop for testing gamepads
running = True
clock = pygame.time.Clock()
print("clock initialized")

#-------------------------------Test Matrix during pygame-------------------------------------------
for y in range(32):
    for x in range(32):
        offset_canvas.SetPixel(x, y, 0, 255, 0)
        offset_canvas = matrix.SwapOnVSync(offset_canvas)

offset_canvas.Clear()
offset_canvas = matrix.SwapOnVSync(offset_canvas)
print("output green")

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.JOYBUTTONDOWN:
            joystick_id = event.joy
            button_id = event.button
            print(f"Gamepad {joystick_id + 1} - Button {button_id} pressed")
#-------------------------------Test Matrix if gamepad input-------------------------------------------
            offset_canvas.Clear()
            offset_canvas = matrix.SwapOnVSync(offset_canvas)
            
            for y in range(32):
                for x in range(32):
                    offset_canvas.SetPixel(x, y, 0, 0, 255)
                    offset_canvas = matrix.SwapOnVSync(offset_canvas)

    # Cap the frame rate
    clock.tick(60)

# Quit Pygame
pygame.quit()
sys.exit()

