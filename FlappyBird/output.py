#! /usr/bin/env python3
import pygame
import colors as c
import settings as s
from rgbmatrix import RGBMatrix, RGBMatrixOptions

def draw_screen(screen, player_pos_x, player_pos_y, pillar_pos_x, pillar_pos_y):
    screen.fill(c.SKY_BLUE)
    draw_pillars(screen, pillar_pos_x, pillar_pos_y)
    pygame.draw.rect(screen, c.FLAPPY_ORANGE, (player_pos_x, player_pos_y, s.PLAYER_WIDTH, s.PLAYER_WIDTH))# Player
    pygame.draw.rect(screen, c.GROUND_BROWN, (0, s.SCREEN_HEIGHT - s.GROUND_HEIGHT, s.SCREEN_WIDTH, s.GROUND_HEIGHT))# Ground dirt
    pygame.draw.rect(screen, c.LIGHT_GREEN, (0, s.SCREEN_HEIGHT - s.GROUND_HEIGHT, s.SCREEN_WIDTH, s.PIXEL_WIDTH))# Ground top layer

def draw_matrix(screen, matrix, offset_canvas):
    for y in range(32):
        for x in range(32):
            color = screen.get_at((x, y))# get color in format (r, g, b, t)            
            offset_canvas.SetPixel(x, y, color[0], color[1], color[2])
    return matrix.SwapOnVSync(offset_canvas)

def draw_pillars(screen, pillar_pos_x, pillar_pos_y):
    for i in range(s.PILLAR_COUNT):
        pygame.draw.rect(screen, c.LIGHT_GREEN, (pillar_pos_x[i], 0, s.PIXEL_WIDTH, s.SCREEN_HEIGHT))# Pillar left
        pygame.draw.rect(screen, c.GREEN, (pillar_pos_x[i] + s.PIXEL_WIDTH, 0, s.PIXEL_WIDTH, s.SCREEN_HEIGHT))# Pillar left
        pygame.draw.rect(screen, c.DARK_GREEN, (pillar_pos_x[i] + (s.PIXEL_WIDTH * 2), 0, s.PIXEL_WIDTH, s.SCREEN_HEIGHT))# Pillar left
        pygame.draw.rect(screen, c.SKY_BLUE, (pillar_pos_x[i], pillar_pos_y[i] - s.PILLAR_HEIGHT, s.PILLAR_WIDTH, s.PILLAR_HEIGHT))# Pillar vertical gap

# Here is where the programm talks to the matrix in the future
# Right now it serves to represent how the game will actually look on the matrix in the window
def draw_matrix_representation(screen):
    for y in range(32):
        for x in range(32):
            pos_x = x * s.PIXEL_WIDTH
            pos_y = y * s.PIXEL_WIDTH
            color = screen.get_at((pos_x, pos_y))# get color in format (r, g, b, t)
            pygame.draw.rect(screen, color, (pos_x + s.SCREEN_WIDTH, pos_y, s.PIXEL_WIDTH, s.PIXEL_WIDTH))# Single Pixel representation

    pygame.draw.rect(screen, (0, 0, 0), (s.SCREEN_WIDTH, 0, 1, s.SCREEN_HEIGHT))# Seperating line

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
