import pygame
import sys

# Initialize Pygame
pygame.init()

# Set up gamepads
pygame.joystick.init()
joysticks = [pygame.joystick.Joystick(i) for i in range(pygame.joystick.get_count())]

if not joysticks:
    print("No gamepads detected. Exiting.")
    pygame.quit()
    sys.exit()

for joystick in joysticks:
    joystick.init()
    print(f"Detected Gamepad: {joystick.get_name()}")

# Main loop for testing gamepads
running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.JOYBUTTONDOWN:
            joystick_id = event.joy
            button_id = event.button
            print(f"Gamepad {joystick_id + 1} - Button {button_id} pressed")

    # Cap the frame rate
    clock.tick(60)

# Quit Pygame
pygame.quit()
sys.exit()
