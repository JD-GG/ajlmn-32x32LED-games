import GeometryDash.Variables as v
# Kollisionserkennung und -behandlung
def PlayerOnGround():
    if v.player_pos > v.SCREEN_HEIGHT - v.GROUND - v.PLAYERSIZE:
        v.player_pos = v.SCREEN_HEIGHT - v.GROUND - v.PLAYERSIZE
        v.player_vel = 0
        return True
    return False

#def PlayerOnObstical():

#def PlayerHitObstical():

#def PlayerOnDeathObstical():