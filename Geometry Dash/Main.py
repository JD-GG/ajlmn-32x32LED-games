import pygame
import Variables as v
import RGBMatrixEmulator

pygame.init()

screen = pygame.display.set_mode((v.SCREEN_WIDTH, v.SCREEN_HEIGHT))
pygame.display.set_caption("Geometry Dash")
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
    
    v.player_pos, v.player_vel, on_ground = PlayerOnGround(player_pos, player_vel, v.SCREEN_HEIGHT, v.GROUND, v.PLAYERSIZE)

    #Draw
    screen.fill((0, 0, 0))
    pygame.draw.rect(screen, (0, 255, 0), (0, v.SCREEN_HEIGHT - v.GROUND, v.SCREEN_WIDTH, v.GROUND))
    pygame.draw.rect(screen, (255, 0, 0), (v.PLAYERX, v.player_pos, v.PLAYERSIZE, v.PLAYERSIZE))
    
    if on_ground:
        key = pygame.key.get_pressed()
        if key[pygame.K_SPACE]:
            player_vel = v.lift
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            
    pygame.display.update()

pygame.quit()
