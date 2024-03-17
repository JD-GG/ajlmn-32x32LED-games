import pygame
import sys

pygame.init()

# Farben
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Bildschirmgröße
WIDTH, HEIGHT = 800, 600
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Kollisionsdetektion")

# Spieler Rechteck
player_width, player_height = 50, 50
player_x, player_y = 50, HEIGHT // 2
player_rect = pygame.Rect(player_x, player_y, player_width, player_height)

# Hindernis Rechteck
obstacle_width, obstacle_height = 100, 200
obstacle_x, obstacle_y = WIDTH - 150, HEIGHT // 2
obstacle_rect = pygame.Rect(obstacle_x, obstacle_y, obstacle_width, obstacle_height)

clock = pygame.time.Clock()

running = True
while running:
    SCREEN.fill(WHITE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        player_rect.y -= 5
    if keys[pygame.K_DOWN]:
        player_rect.y += 5
    if keys[pygame.K_LEFT]:
        player_rect.x -= 5
    if keys[pygame.K_RIGHT]:
        player_rect.x += 5

    # Kollisionserkennung
    if player_rect.colliderect(obstacle_rect):
        # Kollision von links
        if player_rect.right > obstacle_rect.left and player_rect.left < obstacle_rect.left:
            print("Kollision von links - Spiel beenden")
            pygame.quit()
            sys.exit()
        # Kollision von oben
        elif player_rect.bottom > obstacle_rect.top and player_rect.top < obstacle_rect.top:
            print("Kollision von oben - Spieler auf Höhe des Hindernisses weiterführen")
            player_rect.y = obstacle_rect.top - player_height

    pygame.draw.rect(SCREEN, RED, obstacle_rect)
    pygame.draw.rect(SCREEN, BLACK, player_rect)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()