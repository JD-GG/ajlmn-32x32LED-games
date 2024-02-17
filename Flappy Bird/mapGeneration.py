import pygame
from random import randint
import colors as c
import settings as s

def init_pillar_pos_x():
    first_pillar_position = s.SCREEN_WIDTH + s.PILLAR_WIDTH
    start_pos_x = [None] * s.PILLAR_COUNT
    for i in range(s.PILLAR_COUNT):
        start_pos_x[i] = first_pillar_position + (i * s.PILLAR_WIDTH) + (i * s.PILLAR_GAP_WIDTH)
    return start_pos_x

def init_pillar_pos_y():
    random_pos_y = [None] * s.PILLAR_COUNT
    for i in range(s.PILLAR_COUNT):
        random_pos_y[i] = get_random_pos_y()
    return random_pos_y

def get_random_pos_y():
    return randint(s.PILLAR_HEIGHT + 80, 480)# 80 = 4 pixels; 480 = SCREEN_HEIGHT - GROUND_HEIGHT - 4 PIXELS

def draw_pillars(screen, pillar_pos_x, pillar_pos_y):
    for i in range(s.PILLAR_COUNT):
        pygame.draw.rect(screen, c.LIGHT_GREEN, (pillar_pos_x[i], 0, s.PIXEL_WIDTH, s.SCREEN_HEIGHT))# Pillar left
        pygame.draw.rect(screen, c.GREEN, (pillar_pos_x[i] + s.PIXEL_WIDTH, 0, s.PIXEL_WIDTH, s.SCREEN_HEIGHT))# Pillar left
        pygame.draw.rect(screen, c.DARK_GREEN, (pillar_pos_x[i] + (s.PIXEL_WIDTH * 2), 0, s.PIXEL_WIDTH, s.SCREEN_HEIGHT))# Pillar left
        pygame.draw.rect(screen, c.SKY_BLUE, (pillar_pos_x[i], pillar_pos_y[i] - s.PILLAR_HEIGHT, s.PILLAR_WIDTH, s.PILLAR_HEIGHT))# Pillar vertical gap
        pygame.draw.rect(screen, (255, 0, 0), (pillar_pos_x[i], pillar_pos_y[i], 5, 5))# Pillar position (can be removed)

def global_test():
    global pillar_pos_x
    global pillar_pos_y
    