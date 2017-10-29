import pygame

pygame.init()

displayWidth = 800
displayHeight = 600
playerImg = pygame.image.load('Char.png')
saucerImg = pygame.image.load('Saucer.png')

black = (0,0,0)
white = (255,255,255)

gameDisplay = pygame.display.set_mode((displayWidth, displayHeight))
pygame.display.set_caption("A Game")
clock = pygame.time.Clock()


def car(x, y):
    gameDisplay.blit(playerImg, (x, y))


def saucer(x1, y1):
    gameDisplay.blit(saucerImg, (x1, y1))


x = (displayWidth * 0.5)
y = (displayHeight * 0.8)
x1 = (displayWidth * 0.5)
y1 = (displayHeight * 0.3)

crashed = False
while not crashed:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            crashed = True

    car(x, y)
    saucer(x1, y1)
    pygame.display.update()
    clock.tick(10)

pygame.quit()
quit()