import pygame

pygame.init()

SCREEN_WIDTH = 640
SCREEN_HEIGHT = 640
BIRD_SIZE = 40

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Flappy Bird")

# Bird variables
player_pos = [100, 320]
player_vel = 0
gravity = 15
lift = -6

clock = pygame.time.Clock()

run = True
while run:
    tickTime = clock.tick(60) / 1000  

    player_vel += gravity * tickTime  
    player_pos[1] += player_vel
    
    screen.fill((0, 0, 0))
    pygame.draw.rect(screen, (255, 0, 0), (player_pos[0], player_pos[1], BIRD_SIZE, BIRD_SIZE))
    
    key = pygame.key.get_pressed()
    if key[pygame.K_SPACE]:
        player_vel = lift
    
    if player_pos[1] < 0:
        player_pos[1] = 0
        
    if player_pos[1] > SCREEN_HEIGHT - BIRD_SIZE:
        player_pos[1] = SCREEN_HEIGHT - BIRD_SIZE
        player_vel = 0
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            
    pygame.display.update()

pygame.quit()
