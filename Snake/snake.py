import pygame
from pygame.locals import *
import random
from FlappyBird.output import draw_matrix_representation, draw_matrix
started_on_pi = True
try:
    from rgbmatrix import RGBMatrix, RGBMatrixOptions
except ImportError:
    started_on_pi = False

def snake_game(screen, matrix, offset_canvas):
    SCREEN_WIDTH = 640
    SCREEN_HEIGHT = 640
    SNAKE_SIZE = 40
    FOOD_SIZE = 40
    speed = 20
    
    # Snake variables
    snake_pos = [[100, 50]]  # List of segments, starting with initial head position
    snake_vel = [0, 0]  # No initial movement
    score = 0

    def generate_food_position():
        while True:
            food_pos = [random.randrange(1, (SCREEN_WIDTH//FOOD_SIZE)) * FOOD_SIZE,
                        random.randrange(1, (SCREEN_HEIGHT//FOOD_SIZE)) * FOOD_SIZE]
            if food_pos not in snake_pos:
                return food_pos

    food_pos = generate_food_position()
    food_spawn = True

    clock = pygame.time.Clock()

    run = True
    while run:
        clock.tick(15)  # Adjust the speed for gameplay
        
        direction = ""

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.KEYDOWN:
                if event.key == K_LEFT and snake_vel[0] != speed and direction != "right":
                    snake_vel = [-speed, 0]
                    direction = "left"
                elif event.key == K_RIGHT and snake_vel[0] != -speed and direction != "left":
                    snake_vel = [speed, 0]
                    direction = "right"
                elif event.key == K_UP and snake_vel[1] != speed and direction != "down":
                    snake_vel = [0, -speed]
                    direction = "up"
                elif event.key == K_DOWN and snake_vel[1] != -speed and direction != "up":
                    snake_vel = [0, speed]
                    direction = "down"
                elif event.key == K_s:
                    run = False
            # Joypad axis motion event
            elif event.type == pygame.JOYAXISMOTION:
                if event.axis == 0:
                    if event.value < -0.5 and snake_vel[0] != speed and direction != "right":
                        snake_vel = [-speed, 0]
                        print("Left")
                        direction = "left"
                    elif event.value > 0.5 and snake_vel[0] != -speed and direction != "left":
                        snake_vel = [speed, 0]
                        print("Right")
                        direction = "right"
                elif event.axis == 1:
                    if event.value < -0.5 and snake_vel[1] != speed and direction != "down":
                        snake_vel = [0, -speed]
                        print("Up")
                        direction = "up"
                    elif event.value > 0.5 and snake_vel[1] != -speed and direction != "up":
                        snake_vel = [0, speed]
                        print("Down")
                        direction = "down"
            # SELECT
            elif event.type == pygame.JOYBUTTONDOWN and event.button == 8:
                run = False
        
        
        if pygame.Rect(snake_pos[0][0], snake_pos[0][1], SNAKE_SIZE, SNAKE_SIZE).colliderect(pygame.Rect(food_pos[0], food_pos[1], FOOD_SIZE, FOOD_SIZE)):
            score += 1
            food_spawn = False
        if not food_spawn:
            food_pos = generate_food_position()
            food_spawn = True

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

        if started_on_pi:
            offset_canvas = draw_matrix(screen, matrix, offset_canvas)
        else:
            draw_matrix_representation(screen)
            pygame.display.update()
