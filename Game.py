######### INITIALIZING GAME #####################
import pygame
from random import randint
import math
pygame.mixer.pre_init(44100, 16, 2, 4096)
pygame.font.init()
pygame.init()

displayWidth = 800
displayHeight = 600
playerImg1 = pygame.image.load('Images/Char.png')
playerImg2 = pygame.image.load('Images/Char2.png')
playerImg3 = pygame.image.load('Images/Char3.png')
bulletImg = pygame.image.load("Images/Bullet.png")
missileImg = pygame.image.load('Images/missile.png')
boss1Img = pygame.image.load('Images/Boss1.png')
black = (0, 0, 0)
white = (255, 255, 255)
myfont = pygame.font.SysFont('Cooper Black', 30)
shot = pygame.mixer.Sound("Music/laser.wav")
gameDisplay = pygame.display.set_mode((displayWidth, displayHeight))
pygame.display.set_caption("Alien Attack")
clock = pygame.time.Clock()

######################## Function Definition #########################################
######################## Movment Functions ######################################
# Name: playermove
# Objective: Set the speed of the player character
# Objective2: Change the position of the player character by the speed of the player character.
# Input: X and Y coordinates of the player character. Whether the left, right, up and down arrow keys are down.
# Output: The new X and Y coordinates for the player as a tuple in the form: (X, Y).
def playermove(x, y, xLeft, xRight, yUp, yDown):
    xChange = 0
    if xLeft is True:
        xChange -= 5
    if xRight is True:
        xChange += 5
    if x < 10:
        xChange = xRight * 5
    if x > 750:
        xChange = -(xLeft * 5)
    x += xChange

    yChange = 0
    if yUp is True:
        yChange -= 5
    if yDown is True:
        yChange += 5
    if y < 50:
        yChange = (yDown * 5)
    if y > 550:
        yChange = -(yUp * 5)
    y += yChange
    playerposition = (x, y)
    return(playerposition)


# Name: bulletsmove
# Objective: Move all bullets up 10 points in the y coordinate
# Objective2: If all any bullets are above the y coordininate of (x, -10), remove them
# Input: None
# Output: Modify the array bullets.
def bulletsmove():
    for b in range(len(bullets)):
        bullets[b][1] -= 10
    removed = 0
    for b in range(len(bullets)):
        if bullets[b-removed][1] < 0:
            del bullets[b - removed]
            removed = removed + 1

# Name: missilessmove
# Objective: Increase the speed of missile NPCs by 1 towards the player character, to a limit of 3 units per second in both axis's.
# Objective2: Move all missile NPCs towards the player character at their current speed.
# Input: X and Y coordinates of the player character
# Output: Modified missiles array.
def missilesmove(x, y):
    for s in range(len(missiles)):
        if x > missiles[s][0]:
            missiles[s][2] += 1
        elif x < missiles[s][0]:
            missiles[s][2] -= 1
        if missiles[s][2] > 3:
            missiles[s][2] = 3
        if missiles[s][2] < -3:
            missiles[s][2] = -3
        if missiles[s][0] == x and missiles[s][2] <= 1 and missiles[s][2] >= -1:
            missiles[s][2] = 0

        if y > missiles[s][1]:
            missiles[s][3] += 1
        elif y < missiles[s][1]:
            missiles[s][3] -= 1
        if missiles[s][3] > 3:
            missiles[s][3] = 3
        if missiles[s][3] < -3:
            missiles[s][3] = -3
        if missiles[s][1] == y and missiles[s][3] <= 1 and missiles[s][3] >= -1:
            missiles[s][3] = 0

        missiles[s][0] += missiles[s][2]
        missiles[s][1] += missiles[s][3]

######################## NPC Spawning Functions ######################################
def missilespawn():
    spawn = 0
    if loops < 600:
        spawn = 120
    elif loops < 6000:
        spawn = 60
    elif loops < 12000:
        spawn = 30
    elif loops < 36000:
        spawn = 15
    if (loops % spawn) == 0:
        sidechoice = randint(0, 1)
        if sidechoice == 0:
            x1 = randint(-20, 810)
            sidechoice = randint(0, 1)
            if sidechoice == 0:
                y1 = -20
            else:
                y1 = 610
        else:
            y1 = randint(-20, 610)
            sidechoice = randint(0, 1)
            if sidechoice == 0:
                x1 = -20
            else:
                x1 = 810
        missiles.append([x1, y1, 0, 0])


######################## Collision Functions ######################################
def collision(self, sprite):
    return self.colliderect(sprite)

def playerhitmissile(x, y):
    healthchange = 0
    missileHits = 0
    for s in range(len(missiles)):
        playerCheck = pygame.Rect(x, y, 16, 40)
        missileCheck = pygame.Rect(missiles[s - missileHits][0], missiles[s - missileHits][1], 16, 16)
        hit = collision(playerCheck, missileCheck)
        if hit == 1:
            del missiles[s]
            healthchange = healthchange + 1
            missileHits += 1
        return healthchange


def bullethitmissile():
    scorechange = 0
    collisionCountBullets = 0
    collisionCount = 0
    for b in range(len(bullets)):
        collisionCountBullets += collisionCount
        collisionCount = 0
        hit = 0
        for s in range(len(missiles)):
            if hit == 0:
                bulletCheck = pygame.Rect(bullets[b - collisionCountBullets][0],
                                          bullets[b - collisionCountBullets][1], 14, 16)
                missileCheck = pygame.Rect(missiles[s][0], missiles[s][1], 16, 16)
                hit = collision(bulletCheck, missileCheck)
                if hit == 1:
                    del bullets[b]
                    del missiles[s]
                    collisionCount += 1
                    scorechange += 100
    return scorechange

######################## Game Display Functions ######################################
def missile(x1, y1):
    gameDisplay.blit(missileImg, (x1, y1))


def anglefinder(s, x, y):
    if (x - missiles[s][0]) != 0:
        ytan = (y - (missiles[s][1]))
        xtan = ((missiles[s][0]) - x)
        angle = (math.degrees(math.atan2(ytan, xtan)))
        angle = angle + 90
    elif (y - (missiles[s][1])) < 0:
        angle = 0
    else:
        angle = 180
    return angle


def displaystats(myfont, loops, score, health):
    textsurface = myfont.render("Time: " + str(int(round((loops/60), 1))), False, (255, 200, 200))
    gameDisplay.blit(textsurface, (40, 0))
    textsurface = myfont.render("Score: " + str(score), False, (255, 200, 200))
    gameDisplay.blit(textsurface, (610, 0))
    textsurface = myfont.render("HP: " + str(health), False, (255, 200, 200))
    gameDisplay.blit(textsurface, (345, 0))
    pygame.display.update()


def player1(x, y):
    if health == 3:
        gameDisplay.blit(playerImg1, (x, y))
    if health == 2:
        gameDisplay.blit(playerImg2, (x, y))
    else:
        gameDisplay.blit(playerImg3, (x, y))


#######################Initialising Variables################################################
x = (displayWidth * 0.5)    # Integer containing current X co'ordinate of player character
y = (displayHeight * 0.4)   # Integer containing current Y co'ordinate of player character
xLeft = False   # Boolean determining if the left arrow key is down.
xRight = False  # Boolean determining if the right arrow key is down.
yUp = False     # Boolean determining if the upwards arrow key is down.
yDown = False   # Boolean determining if the downwards arrow key is down.
loops = 0       # Integer counting number of game ticks.
count = 0       # Integer counting number of game ticks in non-boss stages. Used to determine boss spawning.
cooldown = 300  # Integer counting enemy spawning cooldown time.
health = 3      # Integer containing the current hp of the player character. Either 3, 2, 1 or 0. Game ends at 0.
score = 0       # Integer counting total score
healthchange = 0    # Integer containing the change in player health after a loop of collision functions
scorechange = 0     # Integer containing the change in score after a loop of collision functions

bullets = []    # Array containing tuples containing the position of bullets in the form [(X0, Y0), (X1, Y1)... e.t.c.]
missiles = []   # Array containing tuples containing the position and speed of missile enemies in the form [(X0, Y0, Xspeed0, Yspeed0), (X1, Y1, Xspeed1, Yspeed1).. e.t.c]


# Stage Flags
# Stage Flags are initially True, (Other than crashed) and dictate the level of the game.
crashed = False  # If True, skip/end all stages.
start = True     # If False skip/end main menu
stage1 = True    # If False skip/end stage 1
waiting1 = True  # If False skip/end transmission period 1
waiting2 = True  # If False skip/end transmission period 2
boss1 = True     # If False skip/end first boss

############################ START MENU ############################################
while start and not crashed:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                start = False
            if event.key == pygame.K_1:
                loops = (60 * 75)
                stage1 = False
            if event.key == pygame.K_2:
                loops = (60 * 86)

                waiting1 = False
                waiting2 = False

        if event.type == pygame.QUIT:
            crashed = True
    textsurface = myfont.render("Press Space To Start", False, (255, 200, 200))
    gameDisplay.blit(textsurface, (230, 270))
    pygame.display.update()

############################ STAGE 1 #############################################
pygame.mixer.music.load("Music/MainTheme.wav")
pygame.mixer.music.set_volume(0.8)
pygame.mixer.music.play(10)
while stage1 and not crashed:
# Player Inputs
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            crashed = True

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                xLeft = True
            if event.key == pygame.K_RIGHT:
                xRight = True
            if event.key == pygame.K_UP:
                yUp = True
            if event.key == pygame.K_DOWN:
                yDown = True
            if event.key == pygame.K_SPACE:
                bullets.append([(x + 8), y])
                shot.play()

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                xLeft = False
            elif event.key == pygame.K_RIGHT:
                xRight = False
            if event.key == pygame.K_UP:
                yUp = False
            if event.key == pygame.K_DOWN:
                yDown = False

# Player Movement
    playerposition = playermove(x, y, xLeft, xRight, yUp, yDown)
    x = playerposition[0]
    y = playerposition[1]

# Spawning/NPC Removal/NPC Movement
    bulletsmove()
    missilespawn()
    missilesmove(x, y)

# Collisions
    scorechange = bullethitmissile()
    healthchange = playerhitmissile(x, y)

    if scorechange >= 1:
        score += scorechange

    if healthchange >= 1:
        health -= healthchange
    if health == 0:
        crashed = True


# Game Display
    gameDisplay.fill(black)
    for b in range(len(bullets)):
        gameDisplay.blit(bulletImg, (bullets[b][0], bullets[b][1]))
    player1(x, y)
    for s in range(len(missiles)):
        angle = anglefinder(s, x, y)
        displayer = pygame.transform.rotate(missileImg, angle)
        gameDisplay.blit(displayer, (missiles[s][0], missiles[s][1]))
    displaystats(myfont, loops, score, health)


# Cooldowns/Clocks/Ticks
    clock.tick(60)
    loops = loops + 1
    if loops == (60*75):
        stage1 = False
    cooldown = cooldown - 1

for m in range(len(missiles)):
    del missiles[0]

############################Screen Change#########################################
pygame.mixer.music.load("Music/Alien_Boss.wav")
pygame.mixer.music.set_volume(0.8)
pygame.mixer.music.play(1)
x = (displayWidth * 0.5)
y = (displayHeight * 0.4)
while waiting1 and not crashed:
    # Game Display
    clock.tick(60)
    loops = loops + 1
    if loops > (60 * 76):
        waiting1 = False
    gameDisplay.fill(white)
    displaystats(myfont, loops, score, health)

while waiting2 and not crashed:
# Player Inputs
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            crashed = True

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                xLeft = True
            if event.key == pygame.K_RIGHT:
                xRight = True
            if event.key == pygame.K_UP:
                yUp = True
            if event.key == pygame.K_DOWN:
                yDown = True
            if event.key == pygame.K_SPACE:
                bullets.append([(x + 8), y])
                shot.play()

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                xLeft = False
            elif event.key == pygame.K_RIGHT:
                xRight = False
            if event.key == pygame.K_UP:
                yUp = False
            if event.key == pygame.K_DOWN:
                yDown = False

# Player Movement
    playerposition = playermove(x, y, xLeft, xRight, yUp, yDown)
    x = playerposition[0]
    y = playerposition[1]

# Spawning/NPC Removal/NPC Movement
    bulletsmove()

# Game Display
    gameDisplay.fill((0, 40, 0))
    for b in range(len(bullets)):
        gameDisplay.blit(bulletImg, (bullets[b][0], bullets[b][1]))
    player1(x, y)
    displaystats(myfont, loops, score, health)

# Cooldowns/Clocks/Ticks
    clock.tick(60)
    loops = loops + 1
    if loops == (60 * 86):
        waiting2 = False
        count = loops
    cooldown = cooldown - 1

############################ BOSS 1 ###############################################
pygame.mixer.music.load("Music/Boss1.wav")
pygame.mixer.music.set_volume(0.8)
pygame.mixer.music.play(-1)
while boss1 and not crashed:
# Player Inputs
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            crashed = True

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                xLeft = True
            if event.key == pygame.K_RIGHT:
                xRight = True
            if event.key == pygame.K_UP:
                yUp = True
            if event.key == pygame.K_DOWN:
                yDown = True
            if event.key == pygame.K_SPACE:
                bullets.append([(x + 8), y])
                shot.play()

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                xLeft = False
            elif event.key == pygame.K_RIGHT:
                xRight = False
            if event.key == pygame.K_UP:
                yUp = False
            if event.key == pygame.K_DOWN:
                yDown = False

# Player Movement
    playerposition = playermove(x, y, xLeft, xRight, yUp, yDown)
    x = playerposition[0]
    y = playerposition[1]

# Spawning/NPC Removal/NPC Movement
    bulletsmove()

# Collisions
    healthchange = 0
    scorechange = 0

    if healthchange >= 1:
        health -= healthchange
    if health == 0:
        crashed = True

# Game Display
    gameDisplay.fill(( 0, 40, 0))
    for b in range(len(bullets)):
        gameDisplay.blit(bulletImg, (bullets[b][0], bullets[b][1]))
    player1(x, y)
    gameDisplay.blit(boss1Img, (40, 40))
    displaystats(myfont, loops, score, health)

# Cooldowns/Clocks/Ticks
    clock.tick(60)
    loops = loops + 1
    count = count + 1
    if count == (60*150):
        stage2 = False
    cooldown = cooldown - 1

pygame.quit()
quit()