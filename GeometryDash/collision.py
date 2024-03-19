import GeometryDash.Variables as v,pygame,math
# Kollisionserkennung und -behandlung
def PlayerOnGround():
    if v.player_pos > v.SCREEN_HEIGHT - v.GROUND - (v.PLAYERSIZE):
        v.player_pos = v.SCREEN_HEIGHT - v.GROUND - (v.PLAYERSIZE)
        v.player_vel = 0
        v.on_ground = True


def PlayerHitObstical(Rect):
    player_hitbox = pygame.Rect(v.PLAYERX, v.player_pos, v.PLAYERSIZE, v.PLAYERSIZE)
    if player_hitbox.colliderect(Rect):

        if v.player_vel > 0 and player_hitbox.right > Rect.left and player_hitbox.left < Rect.left and player_hitbox.bottom-8 > Rect.top: #Dead falling down
            return True
        elif v.player_vel <= 0 and player_hitbox.right > Rect.left and player_hitbox.left < Rect.left: #Dead jumping up
            return True
        elif player_hitbox.bottom > Rect.top and player_hitbox.top < Rect.top: #On Top
            v.player_pos = Rect.top - v.PLAYERSIZE
            v.player_vel = 0
            v.on_ground = True
            return False
        
def PlayerOnDeathObstical(Rect):
    player_hitbox = pygame.Rect(v.PLAYERX, v.player_pos, v.PLAYERSIZE, v.PLAYERSIZE)
    if player_hitbox.colliderect(Rect):
        return True
    return False