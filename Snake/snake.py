import pygame

pygame.init()

SCREEN_WIDTH = 640
SCREEN_HEIGHT = 640
SNAKE_SIZE = 40

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Snake")

# Snake variables
snake_pos = [100, 320]
snake_vel = [0, 0]
speed = 5

clock = pygame.time.Clock()

run = True
while run:
    clock.tick(60)

    # Update snake position
    snake_pos[0] += snake_vel[0]
    snake_pos[1] += snake_vel[1]

    screen.fill((0, 0, 0))
    rect = pygame.draw.rect(screen, (255, 0, 0), (snake_pos[0], snake_pos[1], SNAKE_SIZE, SNAKE_SIZE))

    # Update snake direction based on key press
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        snake_vel = [-speed, 0]
    if keys[pygame.K_RIGHT]:
        snake_vel = [speed, 0]
    if keys[pygame.K_UP]:
        snake_vel = [0, -speed]
    if keys[pygame.K_DOWN]:
        snake_vel = [0, speed]

    # Prevent snake from going off screen
    if snake_pos[0] < 0:
        snake_pos[0] = 0
    if snake_pos[0] > SCREEN_WIDTH - SNAKE_SIZE:
        snake_pos[0] = SCREEN_WIDTH - SNAKE_SIZE
    if snake_pos[1] < 0:
        snake_pos[1] = 0
    if snake_pos[1] > SCREEN_HEIGHT - SNAKE_SIZE:
        snake_pos[1] = SCREEN_HEIGHT - SNAKE_SIZE

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()

pygame.quit()