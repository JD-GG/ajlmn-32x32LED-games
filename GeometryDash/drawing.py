import GeometryDash.Variables as v,pygame,math,GeometryDash.collision as c
def varInit():
    # Player variables
    v.player_pos = v.SCREEN_HEIGHT/2
    v.player_vel = 0
    v.gravity = 25
    v.lift = -10

    # Map variabels
    v.mapStartLength = v.PLAYERX + 500
    v.obsticalGround = v.SCREEN_HEIGHT - v.GROUND - v.OBSTICALSIZE
    v.drawingPoint = 0 #dictates the point the map is at
    v.drawingPointevery40 = 0 #makes so drawing point only gets increased every 40 instences
    v.floorLevel = 1



def drawPlayerGround(screen):
#Draw
    pygame.draw.rect(screen, v.BLUE, (0, v.SCREEN_HEIGHT - v.GROUND, v.SCREEN_WIDTH, v.GROUND))#Ground
    pygame.draw.rect(screen, v.RED, (v.PLAYERX, v.player_pos, v.PLAYERSIZE, v.PLAYERSIZE))#Player

def drawObstical(screen):
    v.mapStartLength = v.mapStartLength - v.mapSpeed
    run = True
    for p, item in enumerate(v.mapOne):
        for i ,row in enumerate(item):
            for j, cell in enumerate(row):
                if cell == 1:
                    x = (j*40 + v.mapStartLength) + p * (v.partSize * v.OBSTICALSIZE) #calculating x for every part of the map
                    pygame.draw.rect(screen, v.BLUE, (x, (i*40), v.OBSTICALSIZE, v.OBSTICALSIZE))
                    Rect = pygame.Rect(x, (i*40), v.OBSTICALSIZE, v.OBSTICALSIZE)
                    if c.PlayerHitObstical(Rect):
                        run = False
                
                elif cell == 2:
                    x = (j*40 + v.mapStartLength) + p * (v.partSize * v.OBSTICALSIZE) #calculating x for every part of the map
                    pygame.draw.rect(screen, v.RED, (x, (i*40), v.OBSTICALSIZE, v.OBSTICALSIZE))
                    Rect = pygame.Rect(x, (i*40) -1, v.OBSTICALSIZE, v.OBSTICALSIZE + 1)
                    if c.PlayerOnDeathObstical(Rect):
                        run = False
    return run

        

def drawPercentage(screen):
    percentage = 0
    if v.mapStartLength - 200 < 0: #Percentage Calculation
        mapTylesOne = len(v.mapOne) * 16 # anzahl der spalten in mapOne
        temp = abs((v.mapStartLength - 200) / 40)
        percentage = math.ceil((temp * 100) / mapTylesOne)

    if percentage > 99:
        for i in range(5): #print 100
            for j in range(3):
                pos1 = v.SCORE_POSITION_X + (j * v.PIXLESIZE) - (5 * v.PIXLESIZE)
                pos2 = pos1 + (5 * v.PIXLESIZE)
                pos3 = pos2 + (5 * v.PIXLESIZE)
                posPercent = pos3 + (5 * v.PIXLESIZE)
                pos_y = v.SCORE_POSITION_Y + (i * v.PIXLESIZE)
                if(v.SCORE[1][i][j]):
                    pygame.draw.rect(screen, v.WHITE, (pos1, pos_y, v.PIXLESIZE, v.PIXLESIZE))# 1 Number
                if(v.SCORE[0][i][j]):
                    pygame.draw.rect(screen, v.WHITE, (pos2, pos_y, v.PIXLESIZE, v.PIXLESIZE))# 0 Number
                if(v.SCORE[0][i][j]):
                    pygame.draw.rect(screen, v.WHITE, (pos3, pos_y, v.PIXLESIZE, v.PIXLESIZE))# 0 Number
                if(v.SCORE[10][i][j]):
                    pygame.draw.rect(screen, v.WHITE, (posPercent, pos_y, v.PIXLESIZE, v.PIXLESIZE))# % Sign

    else:
        number_left = percentage // 10# Get tens place
        number_right = percentage - (number_left * 10)# Get ones place
    
        for i in range(5):
            for j in range(3):
                left_pos_x = v.SCORE_POSITION_X + (j * v.PIXLESIZE)
                right_pos_x = left_pos_x + (5 * v.PIXLESIZE)
                posPercent = right_pos_x + (5 * v.PIXLESIZE)
                pos_y = v.SCORE_POSITION_Y + (i * v.PIXLESIZE)
                if(v.SCORE[number_left][i][j]):
                    pygame.draw.rect(screen, v.WHITE, (left_pos_x, pos_y, v.PIXLESIZE, v.PIXLESIZE))# Left Number
                if(v.SCORE[number_right][i][j]):
                    pygame.draw.rect(screen, v.WHITE, (right_pos_x, pos_y, v.PIXLESIZE, v.PIXLESIZE))# Right Number
                if(v.SCORE[10][i][j]):
                    pygame.draw.rect(screen, v.WHITE, (posPercent, pos_y, v.PIXLESIZE, v.PIXLESIZE))# % Sign