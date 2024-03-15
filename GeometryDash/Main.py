#pcm.!default {type hw card 1}
#ctl.!default {type hwcard 1}

import os
import pygame
import GeometryDash.Variables as v
import GeometryDash.collision as collision
import GeometryDash.drawing as drawing
import GeometryDash.userInput as userInput
from FlappyBird.output import draw_matrix_representation, draw_matrix

started_on_pi = True
try:
    from rgbmatrix import RGBMatrix, RGBMatrixOptions
except ImportError:
    started_on_pi = False

try:
    import GeometryDash.soundplayer as sound
except ImportError:
    pass

def geometry_dash_game(screen, matrix, offset_canvas):
    # pygame.mixer.music.load("./GeometryDash/music.mp3")
    # pygame.mixer.music.play(0, 1.0)

    clock = pygame.time.Clock()

    if started_on_pi:
        # Song, still to be done
        song = sound.SoundPlayer("./GeometryDash/music.mp3", 1)
        song.play()

    run = True
    while run:
        #time.sleep(0.03) # 30FPS
        tickTime = clock.tick(60) / 1000
        v.player_vel += v.gravity * tickTime  
        v.player_pos += v.player_vel
        on_ground = collision.PlayerOnGround()

        drawing.drawPlayerGround(screen)
        drawing.drawObstical(screen)
        drawing.drawPercentage(screen)
        run = userInput.checkInput(on_ground)

        if started_on_pi:
            offset_canvas = draw_matrix(screen, matrix, offset_canvas)
        else:
            draw_matrix_representation(screen)
            pygame.display.update()

    if started_on_pi:
        song.stop()
