import pygame

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

pygame.display.set_caption("Flappy Bird")





# Bird variables
player_pos = [200, 300]
player_vel = 0
gravity = 0.001
lift = -1

run = True
while run:
    
    player_vel += gravity
    player_pos[1] += player_vel
    
    screen.fill((0, 0, 0))
    
    pygame.draw.rect(screen, (255, 0, 0), (player_pos[0], player_pos[1], 50, 50)) 
    
    key = pygame.key.get_pressed()
    
    if(key[pygame.K_SPACE]):
        player_pos[1] -= 2
    
        
    if(player_pos[0] < 0):
        player_pos[0] = 0
    
    if(player_pos[1] < 0):
        player_pos[1] = 0
        
    
    if(player_pos[1] > SCREEN_HEIGHT - 50):
        player_pos[1] = SCREEN_HEIGHT - 50
        player_vel = 0
    
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            
    pygame.display.update()

pygame.quit()