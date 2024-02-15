import pygame

pygame.init()

# Screen variables
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
GROUND = 100
PLAYERSIZE = 50
PLAYERX = 200

# Player variables
player_pos = SCREEN_HEIGHT/2
player_vel = 0
gravity = 15
lift = -10

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
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

    player_vel += gravity * tickTime  
    player_pos += player_vel
    
    player_pos, player_vel, on_ground = PlayerOnGround(player_pos, player_vel, SCREEN_HEIGHT, GROUND, PLAYERSIZE)

    #Draw
    screen.fill((0, 0, 0))
    pygame.draw.rect(screen, (0, 255, 0), (0, SCREEN_HEIGHT - GROUND, SCREEN_WIDTH, GROUND))
    pygame.draw.rect(screen, (255, 0, 0), (PLAYERX, player_pos, PLAYERSIZE, PLAYERSIZE))
    
    if on_ground:
        key = pygame.key.get_pressed()
        if key[pygame.K_SPACE]:
            player_vel = lift
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            
    pygame.display.update()

pygame.quit()
