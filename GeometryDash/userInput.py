import GeometryDash.Variables as v, pygame
from pygame.locals import *

def checkInput(on_ground):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
        elif event.type == pygame.JOYBUTTONDOWN and event.button != 8:# Handle gamepad Button press
            v.player_vel = v.lift
            button = event.button #Start=9, X=0, Y=3, A=1, B=2
        elif event.type == pygame.JOYBUTTONDOWN and event.button == 8:
            return False
        elif event.type == pygame.KEYDOWN and event.key == K_SPACE and on_ground:
            v.player_vel = v.lift
        elif event.type == pygame.KEYDOWN and event.key == K_s:
            return False
    return True