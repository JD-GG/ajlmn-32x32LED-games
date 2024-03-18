#pcm.!default {type hw card 1}
#ctl.!default {type hwcard 1}

import os
import pygame,time
import GeometryDash.Variables as v
import GeometryDash.collision as collision
import GeometryDash.drawing as drawing
import GeometryDash.userInput as userInput
from FlappyBird.output import draw_matrix_representation, draw_matrix, draw_matrix_grid
import GeometryDash.newSoundplayer as sound
started_on_pi = True
try:
    from rgbmatrix import RGBMatrix, RGBMatrixOptions
except ImportError:
    started_on_pi = False

def geometry_dash_game(screen, matrix, offset_canvas):
    clock = pygame.time.Clock()

    audio_file_path = "./GeometryDash/music.wav"
    player = None
    if started_on_pi:
        player = sound.AudioPlayer(audio_file_path)
    else:
        pygame.mixer.music.load("./GeometryDash/music.wav")
        pygame.mixer.music.play(0, 1.0)

    run = True
    running = True
    while running:
        if started_on_pi:
            player.play()
        else:
            pygame.mixer.music.rewind()
            pygame.mixer.music.play(0, 1.0)

        drawing.varInit()

        while run and running:
            tickTime = clock.tick(60) / 1000
            screen.fill((0, 0, 0))
            collision.PlayerOnGround()
            drawing.drawPlayerGround(screen)
            run = drawing.drawObstical(screen)
            running = userInput.checkInput()
            drawing.drawPercentage(screen)

            if started_on_pi:
                offset_canvas = draw_matrix(screen, matrix, offset_canvas)
            else:
                draw_matrix_representation(screen)
                draw_matrix_grid(screen)
                pygame.display.update()

            v.player_vel += v.gravity * tickTime  
            v.player_pos += v.player_vel

        if started_on_pi:
            player.stop()
        else:
            pygame.mixer.music.stop()

        run = userInput.checkAnyInput()
        running = userInput.checkInput()
        
