import pygame, sys
from pygame.locals import *
from pygame.math import Vector2

WIDTH = 800
HEIGHT = 600

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

bullets = []
clock = pygame.time.Clock()

class Player:
    def __init__(self, window):
        self.pos = Vector2(WIDTH / 2, HEIGHT / 2)
        self.width = 12
        self.height = 20
        self.acc = 0.3
        self.speed = 8
        self.thickness = 2
        self.shoot_rate = 250
        self.time = clock.get_time()
        self.dt = 0
        self.velocity = Vector2()
        self.heading = Vector2(0, -1)
        self.angle = 90
        self.delta_ang = 10
        self.left = Vector2()
        self.right = Vector2()
        self.front = Vector2()
        self.window = window

    def update(self):
        self.get_input()
        self.move()
        self.rotate()
        self.bounds()
        self.draw()
    
    def move(self):
        self.limit_speed()
        self.pos.x -= self.velocity.x
        self.pos.y += self.velocity.y

    def limit_speed(self):
        if self.velocity.length_squared() > self.speed ** 2:
            self.velocity = self.velocity.normalize()
            self.velocity.scale_to_length(self.speed)

    def rotate(self):
        self.left.x = - self.width / 2
        self.left.y = self.height / 2

        self.right.x = self.width / 2
        self.right.y = self.height / 2

        self.front.x = 0
        self.front.y = - self.height / 2

        self.angle = self.heading.angle_to(Vector2(0, -1))
        self.left = self.left.rotate(self.angle)
        self.right = self.right.rotate(self.angle)
        self.front = self.front.rotate(self.angle)

    def bounds(self):
        if self.pos.x > WIDTH + self.width / 2:
            self.pos.x = -self.width / 2
        elif self.pos.x < -self.width / 2:
            self.pos.x = WIDTH + self.width / 2
        elif self.pos.y > HEIGHT + self.height / 2:
            self.pos.y = -self.height / 2
        elif self.pos.y < -self.height / 2:
            self.pos.y = HEIGHT + self.height / 2

    def draw(self):
        #clear window
        self.window.fill(BLACK)
        #draw player

        # draw left side
        pygame.draw.line(self.window, WHITE,
                (self.pos.x + self.left.x, self.pos.y + self.left.y),
                (self.pos.x + self.front.x, self.pos.y + self.front.y), self.thickness)
        # draw right side
        pygame.draw.line(self.window, WHITE,
                (self.pos.x + self.front.x, self.pos.y + self.front.y),
                (self.pos.x + self.right.x, self.pos.y + self.right.y), self.thickness)
        # draw back side
        pygame.draw.line(self.window, WHITE,
                (self.pos.x + self.right.x, self.pos.y + self.right.y),
                (self.pos.x + self.left.x, self.pos.y + self.left.y), self.thickness)

    def get_input(self):
        self.dt += clock.get_time()

        if pygame.key.get_pressed()[K_w]:
            self.heading.scale_to_length(self.acc)
            self.velocity += self.heading
        if pygame.key.get_pressed()[K_a]:
            self.heading = self.heading.rotate(self.delta_ang)
        if pygame.key.get_pressed()[K_d]:
            self.heading = self.heading.rotate(-self.delta_ang)
        if pygame.key.get_pressed()[K_SPACE] and self.dt > self.shoot_rate:
            self.shoot()
            self.dt = 0
    def shoot(self):
        b_pos = self.pos + self.front
        b_vel = self.heading.normalize()
        bullet = Bullet(b_pos, b_vel, self.window)
        bullets.append(bullet)

class Bullet:
    def __init__(self, pos, velocity, window):
        self.window = window
        self.radius = 3
        self.speed = 20
        self.velocity = velocity
        self.velocity.x *= -1
        self.velocity.scale_to_length(self.speed)
        self.pos = pos

    def update(self):
        self.pos += self.velocity
        self.bounds()
        self.draw()

    def draw(self):
        pygame.draw.circle(self.window, WHITE,
                (int(self.pos.x), int(self.pos.y)),
                self.radius)
        
    def bounds(self):
        if (     self.pos.x > WIDTH + self.radius 
             or self.pos.x < -self.radius
             or self.pos.y > HEIGHT + self.radius
             or self.pos.y < -self.radius
           ):
            bullets.remove(self)

        

def main():

    # initializa pygame library
    pygame.init()
    # the game will run at 30 frames per second
    FPS = 30
    # create a surface object (like a canvas)
    window = pygame.display.set_mode((WIDTH, HEIGHT))
    # set window title
    pygame.display.set_caption('Holbi Game')
    # create player
    player = Player(window)
    # main game loop
    while True:
        player.update()
        for bullet in bullets:
            bullet.update()
        # handle events
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
        # draw the surface obj to the screen
        pygame.display.update()
        # wait for the next iteration
        clock.tick(FPS)

if __name__ == '__main__':
    main()

