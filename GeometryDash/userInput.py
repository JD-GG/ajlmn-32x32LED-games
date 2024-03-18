import GeometryDash.Variables as v, pygame
from pygame.locals import *

def checkAnyInput():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
        elif event.type == pygame.JOYBUTTONDOWN and event.button == 8:
            return False
        elif event.type == pygame.KEYDOWN and event.key == K_s:
            return False
        elif event.type == pygame.KEYDOWN: 
            return True
        elif event.type == pygame.JOYBUTTONDOWN:
            return True
def checkInput():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
        elif event.type == pygame.JOYBUTTONDOWN and event.button != 8 and v.on_ground:# Handle gamepad Button press
            v.player_vel = v.lift
            v.on_ground = False
            button = event.button #Start=9, X=0, Y=3, A=1, B=2
        elif event.type == pygame.JOYBUTTONDOWN and event.button == 8:
            return False
        elif event.type == pygame.KEYDOWN and event.key == K_SPACE and v.on_ground:
            v.player_vel = v.lift
            v.on_ground = False
        elif event.type == pygame.KEYDOWN and event.key == K_s:
            return False
    return True