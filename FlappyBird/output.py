#! /usr/bin/env python3
import pygame
import colors as c
import settings as s
import score
# from rgbmatrix import RGBMatrix, RGBMatrixOptions

def draw_screen(screen, player_pos_x, player_pos_y, pillar_pos_x, pillar_pos_y, score):
    screen.fill(c.DARK_SKY_BLUE)
    draw_pillars(screen, pillar_pos_x, pillar_pos_y)
    pygame.draw.rect(screen, c.FLAPPY_ORANGE, (player_pos_x, player_pos_y, s.PLAYER_WIDTH, s.PLAYER_WIDTH))# Player
    pygame.draw.rect(screen, c.GROUND_BROWN, (0, s.SCREEN_HEIGHT - s.GROUND_HEIGHT, s.SCREEN_WIDTH, s.GROUND_HEIGHT))# Ground dirt
    pygame.draw.rect(screen, c.LIGHT_GREEN, (0, s.SCREEN_HEIGHT - s.GROUND_HEIGHT, s.SCREEN_WIDTH, s.PIXEL_WIDTH))# Ground top layer
    draw_score(screen, score)

def draw_matrix(screen, matrix, offset_canvas):
    for y in range(32):
        for x in range(32):
            pos_x = x * s.PIXEL_WIDTH
            pos_y = y * s.PIXEL_WIDTH
            color = screen.get_at((pos_x, pos_y))# get color in format (r, g, b, t)            
            offset_canvas.SetPixel(x, y, color[0], color[1], color[2])
    return matrix.SwapOnVSync(offset_canvas)

# This serves to represent how the game will actually look on the matrix in the window
def draw_matrix_representation(screen):
    for y in range(32):
        for x in range(32):
            pos_x = x * s.PIXEL_WIDTH
            pos_y = y * s.PIXEL_WIDTH
            color = screen.get_at((pos_x, pos_y))# get color in format (r, g, b, t)
            pygame.draw.rect(screen, color, (pos_x + s.SCREEN_WIDTH, pos_y, s.PIXEL_WIDTH, s.PIXEL_WIDTH))# Single Pixel representation
    pygame.draw.rect(screen, (0, 0, 0), (s.SCREEN_WIDTH, 0, 1, s.SCREEN_HEIGHT))# Seperating line

def draw_pillars(screen, pillar_pos_x, pillar_pos_y):
    for i in range(s.PILLAR_COUNT):
        pygame.draw.rect(screen, c.LIGHT_GREEN, (pillar_pos_x[i], 0, s.PIXEL_WIDTH, s.SCREEN_HEIGHT))# Pillar left
        pygame.draw.rect(screen, c.GREEN, (pillar_pos_x[i] + s.PIXEL_WIDTH, 0, s.PIXEL_WIDTH, s.SCREEN_HEIGHT))# Pillar center
        pygame.draw.rect(screen, c.DARK_GREEN, (pillar_pos_x[i] + (s.PIXEL_WIDTH * 2), 0, s.PIXEL_WIDTH, s.SCREEN_HEIGHT))# Pillar right
        pygame.draw.rect(screen, c.DARK_SKY_BLUE, (pillar_pos_x[i], pillar_pos_y[i] - s.PILLAR_HEIGHT, s.PILLAR_WIDTH, s.PILLAR_HEIGHT))# Pillar vertical gap

def draw_hitboxes(screen, player_hitbox, pillar_pos_x, pillar_hitbox_top, pillar_hitbox_score, pillar_hitbox_bottom):
    pygame.draw.rect(screen, (255, 0, 0), player_hitbox, 3)  # width = 3
    for i in range(s.PILLAR_COUNT):
        if pillar_pos_x[i] < s.SCREEN_WIDTH:
            pygame.draw.rect(screen, (255, 0, 0), pillar_hitbox_top[i], 3)  # width = 3
            pygame.draw.rect(screen, (255, 0, 0), pillar_hitbox_score[i], 3)  # width = 3
            pygame.draw.rect(screen, (255, 0, 0), pillar_hitbox_bottom[i], 3)  # width = 3

# This helps to understand wich pixels get shown on the matrix
def draw_matrix_grid(screen):
    for y in range(32):
        for x in range(32):
            pos_x = x * s.PIXEL_WIDTH
            pos_y = y * s.PIXEL_WIDTH
            pygame.draw.rect(screen, (255, 0, 0), (pos_x, pos_y, 1, 1))

# These markers help during programming to see where pos_x and pos_y is at any time for each object
def draw_position_markers(screen, player_pos_x, player_pos_y, pillar_pos_x, pillar_pos_y):
    pygame.draw.rect(screen, (255, 0, 0), (player_pos_x, player_pos_y, 5, 5))# Player position
    pygame.draw.rect(screen, (255, 0, 0), (0, 0, s.PIXEL_WIDTH, s.PIXEL_WIDTH))# Single Pixel for reference
    for i in range(s.PILLAR_COUNT):
        if pillar_pos_x[i] < s.SCREEN_WIDTH:
            pygame.draw.rect(screen, (255, 0, 0), (pillar_pos_x[i], pillar_pos_y[i], 5, 5))# Pillar position

# This draws the score on the screen
# Slightly optimized to perfrom less drawing operations
def draw_score(screen, number):
    if number > 99:
        number = 99# Overflow
    number_left = number // 10# Get tens place
    number_right = number - (number_left * 10)# Get ones place
    
    for i in range(5):
        for j in range(3):
            left_pos_x = s.SCORE_POSITION_X + (j * s.PIXEL_WIDTH)
            right_pos_x = left_pos_x + (5 * s.PIXEL_WIDTH)
            pos_y = s.SCORE_POSITION_Y + (i * s.PIXEL_WIDTH)
            if(score.SCORE[number_left][i][j]):
                pygame.draw.rect(screen, c.WHITE, (left_pos_x, pos_y, s.PIXEL_WIDTH, s.PIXEL_WIDTH))# Left Number
            if(score.SCORE[number_right][i][j]):
                pygame.draw.rect(screen, c.WHITE, (right_pos_x, pos_y, s.PIXEL_WIDTH, s.PIXEL_WIDTH))# Right Number
