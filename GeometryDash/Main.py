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
    death_file_path = "./GeometryDash/death.wav"
    music_player = None
    death_player = None
    first_death_loop = False
    if started_on_pi:
        music_player = sound.AudioPlayer(audio_file_path)
        death_player = sound.AudioPlayer(death_file_path)

    run = True
    running = True
    while running:
        drawing.varInit()

        if run:
            if started_on_pi:
                death_player.stop()
                music_player.play()
            else:
                pygame.mixer.music.stop()
                pygame.mixer.music.load(audio_file_path)
                pygame.mixer.music.play(0, 1.0)

        while run and running:
            first_death_loop = True

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

        if started_on_pi and first_death_loop:
            music_player.stop()
            death_player.play()
        elif first_death_loop:
            pygame.mixer.music.stop()
            pygame.mixer.music.load(death_file_path)
            pygame.mixer.music.play(0, 1.0)
        first_death_loop = False

        run = userInput.checkAnyInput()
        running = userInput.checkInput()
        
