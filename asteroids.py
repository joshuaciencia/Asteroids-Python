import pygame, sys
from pygame.locals import *
from pygame.math import Vector2
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
p_x = WIDTH / 2
p_y = HEIGHT / 2
p_width = 12
p_height = 20
p_speed = 4
thickness = 2;
angle = -90
velocity = Vector2()
heading = Vector2(0, -1)
left = Vector2()
right = Vector2()
front = Vector2()
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

    if pygame.key.get_pressed()[K_UP]:
        tmp = Vector2(heading)
        tmp.scale_to_length(p_speed)
        p_x += -tmp.x
        p_y += tmp.y
    if pygame.key.get_pressed()[K_LEFT]:
        heading = heading.rotate(10)
    if pygame.key.get_pressed()[K_RIGHT]:
        heading = heading.rotate(-10)

    # draw player ship
    left.x = - p_width / 2
    left.y = p_height / 2

    right.x = p_width / 2
    right.y = p_height / 2

    front.x = 0
    front.y = - p_height / 2

    angle = heading.angle_to(Vector2(0, -1))
    left = left.rotate(angle)
    right = right.rotate(angle)
    front = front.rotate(angle)

    # fill window with black (clear)
    window.fill(BLACK)

    # draw left side
    pygame.draw.line(window, WHITE, 
            (p_x + left.x, p_y + left.y),
            (p_x + front.x, p_y + front.y), thickness)
    # draw right side
    pygame.draw.line(window, WHITE, 
            (p_x + front.x, p_y + front.y), 
            (p_x + right.x, p_y + right.y), thickness)
    # draw back side
    pygame.draw.line(window, WHITE, 
            (p_x + right.x, p_y + right.y),
            (p_x + left.x, p_y + left.y), thickness)
    # handle events
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    # draw the surface obj to the screen
    pygame.display.update()
    # wait for the next iteration
    clock.tick(FPS)

