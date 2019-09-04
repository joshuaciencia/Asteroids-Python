import pygame, sys
from pygame.locals import *
# initializa pygame library
pygame.init()
# window dimensions
WIDTH = 800
HEIGHT = 600
#color constants (saved in tuplas)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
# player properties (position, size, speed)
playerX = WIDTH / 2
playerY = HEIGHT / 2
playerSize = 20
playerSpeed = 4
thickness = 2;
#font property
fontObj = pygame.font.Font('freesansbold.ttf', 32)
textSurfaceObj = fontObj.render('Holberton Game !', True, GREEN, BLUE)
textRectObj = textSurfaceObj.get_rect()
textRectObj.center = (WIDTH / 2, (HEIGHT / 2) - 100)
# the game will run at 30 frames per second
FPS = 30
# this obj is used ti run the game at the desired speed (FPS)
clock = pygame.time.Clock()
# create a surface object (like a canvas)
window = pygame.display.set_mode((WIDTH, HEIGHT))
# set window title
pygame.display.set_caption('Holbi Game')
# main game loop
while True:
    # fill the window with black color
    window.fill(BLACK)
    # draw the text obj
    window.blit(textSurfaceObj, textRectObj)
    # draw player ship
    # draw left side
    pygame.draw.line(window, WHITE,
            (playerX - playerSize / 2, playerY + playerSize / 2),
            (playerX, playerY - playerSize / 2), thickness)
    # draw right side
    pygame.draw.line(window, WHITE,
            (playerX, playerY - playerSize / 2),
            (playerX + playerSize / 2, playerY + playerSize / 2), thickness)
    # draw back side
    pygame.draw.line(window, WHITE, 
            (playerX - playerSize / 2, playerY + playerSize / 2),
            (playerX + playerSize / 2, playerY + playerSize / 2), thickness)
    # get player input. Note: this is not how the ship should move, this is just test code
    if pygame.key.get_pressed()[K_UP]:
        playerY -= playerSpeed
    if pygame.key.get_pressed()[K_DOWN]:
        playerY += playerSpeed
    if pygame.key.get_pressed()[K_LEFT]:
        playerX -= playerSpeed
    if pygame.key.get_pressed()[K_RIGHT]:
        playerX += playerSpeed
    # handle events
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    # draw the surface obj to the screen
    pygame.display.update()
    # wait for the next iteration
    clock.tick(FPS)

