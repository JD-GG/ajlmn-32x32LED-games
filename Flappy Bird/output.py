import pygame
import settings as s
#from rgbmatrix import RGBMatrix, RGBMatrixOptions

# Here is where the programm talks to the matrix in the future
# Right now it serves to represent how the game will actually look on the matrix in the window

def draw_matrix_representation(screen):
    for y in range(32):
        for x in range(32):
            pos_x = x * s.PIXEL_WIDTH
            pos_y = y * s.PIXEL_WIDTH
            color = screen.get_at((pos_x, pos_y))# get color in format (r, g, b, t)
            # set pixel or something idk
            pygame.draw.rect(screen, color, (pos_x + s.SCREEN_WIDTH, pos_y, s.PIXEL_WIDTH, s.PIXEL_WIDTH))# Single Pixel representation

    pygame.draw.rect(screen, (0, 0, 0), (s.SCREEN_WIDTH, 0, 1, s.SCREEN_HEIGHT))# Seperating line

def draw_matrix_grid(screen):
    for y in range(32):
        for x in range(32):
            pos_x = x * s.PIXEL_WIDTH
            pos_y = y * s.PIXEL_WIDTH
            pygame.draw.rect(screen, (255, 0, 0), (pos_x, pos_y, 1, 1))# These pixels get used to represent the matrix

def draw_position_markers(screen, player_pos_x, player_pos_y, pillar_pos_x, pillar_pos_y):
    pygame.draw.rect(screen, (255, 0, 0), (player_pos_x, player_pos_y, 5, 5))# Player position
    pygame.draw.rect(screen, (255, 0, 0), (0, 0, s.PIXEL_WIDTH, s.PIXEL_WIDTH))# Single Pixel for reference
    for i in range(s.PILLAR_COUNT):
        if pillar_pos_x[i] < s.SCREEN_WIDTH:
            pygame.draw.rect(screen, (255, 0, 0), (pillar_pos_x[i], pillar_pos_y[i], 5, 5))# Pillar position
