import pygame
from pygame.locals import *
import GeometryDash.Variables as v
# import RGBMatrixEmulator
from FlappyBird.output import draw_matrix_representation, draw_matrix
from rgbmatrix import RGBMatrix, RGBMatrixOptions


def geometry_dash_game(screen, matrix, offset_canvas):
    clock = pygame.time.Clock()

    # Kollisionserkennung und -behandlung
    def PlayerOnGround(player_pos, player_vel, SCREEN_HEIGHT, GROUND, PLAYERSIZE):
        if player_pos > SCREEN_HEIGHT - GROUND - PLAYERSIZE:
            player_pos = SCREEN_HEIGHT - GROUND - PLAYERSIZE
            player_vel = 0
            return player_pos, player_vel, True
        return player_pos, player_vel, False

    run = True
    while run:
        tickTime = clock.tick(60) / 1000  
        v.player_vel += v.gravity * tickTime  
        v.player_pos += v.player_vel
        v.player_pos, v.player_vel, on_ground = PlayerOnGround(v.player_pos, v.player_vel, v.SCREEN_HEIGHT, v.GROUND, v.PLAYERSIZE)

        #Draw
        screen.fill((0, 0, 0))
        pygame.draw.rect(screen, v.GREEN, (0, v.SCREEN_HEIGHT - v.GROUND, v.SCREEN_WIDTH, v.GROUND))
        pygame.draw.rect(screen, v.RED, (v.PLAYERX, v.player_pos, v.PLAYERSIZE, v.PLAYERSIZE))
        
        if on_ground:
            key = pygame.key.get_pressed()
            if key[pygame.K_SPACE]:
                v.player_vel = v.lift
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.JOYBUTTONDOWN:# Handle gamepad Button press
                v.player_vel = v.lift
                button = event.button #Start=9, X=0, Y=3, A=1, B=2
            elif event.type == pygame.KEYDOWN and event.key == K_s:
                run = False
            elif event.type == pygame.JOYBUTTONDOWN and event.button == 8:
                run = False

        # draw_matrix_representation(screen)
        offset_canvas = draw_matrix(screen, matrix, offset_canvas)

        # pygame.display.update()
