import pygame
from pygame.locals import *
import random
from FlappyBird.output import draw_matrix_representation

# pygame.init()

# screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
# pygame.display.set_caption("Snake")
def snake_game(screen):
    SCREEN_WIDTH = 640
    SCREEN_HEIGHT = 640
    SNAKE_SIZE = 20
    FOOD_SIZE = 20
    speed = 20

    # Snake variables
    snake_pos = [[100, 50]]  # List of segments, starting with initial head position
    snake_vel = [0, 0]  # No initial movement
    food_pos = [random.randrange(1, (SCREEN_WIDTH//SNAKE_SIZE)) * SNAKE_SIZE,
                random.randrange(1, (SCREEN_HEIGHT//SNAKE_SIZE)) * SNAKE_SIZE]
    food_spawn = True
    score = 0

    clock = pygame.time.Clock()

    run = True
    while run:
        clock.tick(15)  # Adjust the speed for gameplay

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.KEYDOWN:
                if event.key == K_LEFT and snake_vel[0] != speed:
                    snake_vel = [-speed, 0]
                elif event.key == K_RIGHT and snake_vel[0] != -speed:
                    snake_vel = [speed, 0]
                elif event.key == K_UP and snake_vel[1] != speed:
                    snake_vel = [0, -speed]
                elif event.key == K_DOWN and snake_vel[1] != -speed:
                    snake_vel = [0, speed]
                elif event.key == K_s:
                    run = False

        snake_head = [snake_pos[0][0] + snake_vel[0], snake_pos[0][1] + snake_vel[1]]

        # Prevent snake from going off screen
        if snake_head[0] >= SCREEN_WIDTH:
            snake_head[0] = 0
        elif snake_head[0] < 0:
            snake_head[0] = SCREEN_WIDTH - SNAKE_SIZE
        if snake_head[1] >= SCREEN_HEIGHT:
            snake_head[1] = 0
        elif snake_head[1] < 0:
            snake_head[1] = SCREEN_HEIGHT - SNAKE_SIZE

        snake_pos.insert(0, snake_head)  # Update snake position

        # Eating food
        if abs(snake_head[0] - food_pos[0]) < SNAKE_SIZE and abs(snake_head[1] - food_pos[1]) < SNAKE_SIZE:
            score += 1
            food_spawn = False
        else:
            snake_pos.pop()

        if not food_spawn:
            food_pos = [random.randrange(1, (SCREEN_WIDTH//FOOD_SIZE)) * FOOD_SIZE,
                        random.randrange(1, (SCREEN_HEIGHT//FOOD_SIZE)) * FOOD_SIZE]
        food_spawn = True

        # Game Over if snake collides with itself
        for block in snake_pos[1:]:
            if snake_head == block:
                run = False

        screen.fill((0, 0, 0))
        for pos in snake_pos:
            pygame.draw.rect(screen, (0, 255, 0), pygame.Rect(pos[0], pos[1], SNAKE_SIZE, SNAKE_SIZE))
        pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(food_pos[0], food_pos[1], FOOD_SIZE, FOOD_SIZE))

        draw_matrix_representation(screen)

        pygame.display.update()
