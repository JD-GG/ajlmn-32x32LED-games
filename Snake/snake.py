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
    
    #sets game dimensions
    SCREEN_WIDTH = 640
    SCREEN_HEIGHT = 640
    BLOCK_SIZE = 40

    screen = pygame.display.set_mode((640, 640))
    clock = pygame.time.Clock()

    #defines the snake class, with, updates position, checks for collision, and checks for apple collision
    class Snake:
        def __init__(self):
            self.x, self.y = BLOCK_SIZE, BLOCK_SIZE
            self.xdir = 1
            self.ydir = 0
            self.head = pygame.Rect(self.x, self.y, BLOCK_SIZE, BLOCK_SIZE)
            self.body = [pygame.Rect(self.x-BLOCK_SIZE, self.y, BLOCK_SIZE, BLOCK_SIZE)]
            self.dead = False
        
        def update(self):
            global apple
            
            for square in self.body:
                if self.head.x == square.x and self.head.y == square.y:
                    self.dead = True
                if self.head.x not in range(0, SCREEN_WIDTH) or self.head.y not in range(0, SCREEN_HEIGHT):
                    self.dead = True
            
            if self.dead:
                self.x, self.y = BLOCK_SIZE, BLOCK_SIZE
                self.head = pygame.Rect(self.x, self.y, BLOCK_SIZE, BLOCK_SIZE)
                self.body = [pygame.Rect(self.x-BLOCK_SIZE, self.y, BLOCK_SIZE, BLOCK_SIZE)]
                self.xdir = 1
                self.ydir = 0
                self.dead = False
                apple = Apple()
            
            self.body.append(self.head)
            for i in range(len(self.body)-1):
                self.body[i].x, self.body[i].y = self.body[i+1].x, self.body[i+1].y
            self.head.x += self.xdir * BLOCK_SIZE
            self.head.y += self.ydir * BLOCK_SIZE
            self.body.remove(self.head)
            
            if self.head.x < 0:
                self.head.x = SCREEN_WIDTH - BLOCK_SIZE
            elif self.head.x >= SCREEN_WIDTH:
                self.head.x = 0
            if self.head.y < 0:
                self.head.y = SCREEN_HEIGHT - BLOCK_SIZE
            elif self.head.y >= SCREEN_HEIGHT:
                self.head.y = 0

    #defines the apple class, with, updates position
    class Apple:
        def __init__(self):
            self.x = int(random.randint(0, SCREEN_WIDTH)/BLOCK_SIZE) * BLOCK_SIZE
            self.y = int(random.randint(0, SCREEN_HEIGHT)/BLOCK_SIZE) * BLOCK_SIZE
            self.rect = pygame.Rect(self.x, self.y, BLOCK_SIZE, BLOCK_SIZE)
        
        def update(self):
            pygame.draw.rect(screen, "red", self.rect)

    

    snake = Snake()
    apple = Apple()

    #game loop that updates the screen, and checks for input
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    snake.ydir = 0
                    snake.xdir = -1
                elif event.key == pygame.K_RIGHT:
                    snake.ydir = 0
                    snake.xdir = 1
                elif event.key == pygame.K_UP:
                    snake.ydir = -1
                    snake.xdir = 0
                elif event.key == pygame.K_DOWN:
                    snake.ydir = 1
                    snake.xdir = 0
                elif event.key == pygame.K_s:
                    run = False
            
            #Joypad axis motion event
            elif event.type == pygame.JOYAXISMOTION:
                if event.axis == 0:
                    if event.value < -0.5:
                        snake.ydir = 0
                        snake.xdir = -1
                        print("Left")
                    elif event.value > 0.5:
                        snake.ydir = 0
                        snake.xdir = 1
                        print("Right")
                elif event.axis == 1:
                    if event.value < -0.5:
                        snake.ydir = -1
                        snake.xdir = 0
                        print("Up")
                    elif event.value > 0.5:
                        snake.ydir = 1
                        snake.xdir = 0
                        print("Down")

            # SELECT
            elif event.type == pygame.JOYBUTTONDOWN and event.button == 8:
                run = False

        snake.update()
        
        screen.fill('black')

        apple.update()

        pygame.draw.rect(screen, "green", snake.head)

        for square in snake.body:
            pygame.draw.rect(screen, "green", square)

        if snake.head.x == apple.x and snake.head.y == apple.y:
            snake.body.append(pygame.Rect(square.x, square.y, BLOCK_SIZE, BLOCK_SIZE))
            apple = Apple()

        #draws the screen
        if started_on_pi:
            offset_canvas = draw_matrix(screen, matrix, offset_canvas)
        else:
            draw_matrix_representation(screen)
            pygame.display.update()
        clock.tick(10)
