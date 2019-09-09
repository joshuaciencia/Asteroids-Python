import pygame, sys, random
from pygame.locals import *
from pygame.math import Vector2

WIDTH = 800
HEIGHT = 600

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GREY = (125, 125, 125)
YELLOW = (255, 225, 0)

class Player:
    def __init__(self, screen):
        self.pos = Vector2(WIDTH / 2, HEIGHT / 2)
        self.width = 12
        self.height = 20
        self.acc = 0.3
        self.speed = 8
        self.thickness = 2
        self.shoot_rate = 250
        self.shoot_time = 0
        self.velocity = Vector2()
        self.heading = Vector2(0, -1)
        self.angle = 90
        self.delta_ang = 10
        self.left = Vector2()
        self.right = Vector2()
        self.front = Vector2()
        self.screen = screen
        self.propulsion = False
        self.par_rate = 80
        self.par_time = 0

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
        #draw player

        self.par_time += self.screen.clock.get_time()

        # draw left side
        pygame.draw.line(self.screen.window, WHITE,
                (self.pos.x + self.left.x, self.pos.y + self.left.y),
                (self.pos.x + self.front.x, self.pos.y + self.front.y), self.thickness)
        # draw right side
        pygame.draw.line(self.screen.window, WHITE,
                (self.pos.x + self.front.x, self.pos.y + self.front.y),
                (self.pos.x + self.right.x, self.pos.y + self.right.y), self.thickness)
        # draw back side
        pygame.draw.line(self.screen.window, WHITE,
                (self.pos.x + self.right.x, self.pos.y + self.right.y),
                (self.pos.x + self.left.x, self.pos.y + self.left.y), self.thickness)
        # draw propulsion

        if self.propulsion and self.par_time > self.par_rate:
            pos = Vector2(self.pos)
            pos -= self.front
            vel = Vector2(self.heading)
            vel = vel.normalize()
            vel.scale_to_length(-2)
            par = Particle(pos, vel, 4, 1, 1500, GREY, self.screen) 
            self.screen.particles.append(par)
            self.par_time = 0

    def get_input(self):
        self.shoot_time += self.screen.clock.get_time()

        if pygame.key.get_pressed()[K_w]:
            self.heading.scale_to_length(self.acc)
            self.velocity += self.heading
            self.propulsion = True
        else:
            self.propulsion = False
        if pygame.key.get_pressed()[K_a]:
            self.heading = self.heading.rotate(self.delta_ang)
        if pygame.key.get_pressed()[K_d]:
            self.heading = self.heading.rotate(-self.delta_ang)
        if pygame.key.get_pressed()[K_SPACE] and self.shoot_time > self.shoot_rate:
            self.shoot()
            self.shoot_time = 0
    def shoot(self):
        b_pos = self.pos + self.front
        b_vel = self.heading.normalize()
        bullet = Bullet(b_pos, b_vel, self.screen)
        self.screen.add_bullet(bullet)

class Particle:
    def __init__(self, pos, vel, r, t, lt, color, screen):
        self.pos = pos
        self.vel = vel
        self.screen = screen
        self.radius = r
        self.thickness = t
        self.life_time = lt
        self.color = color
        self.time = 0

    def update(self):
        self.time += self.screen.clock.get_time()
        if self.time > self.life_time:
            self.screen.particles.remove(self)

        self.pos += self.vel
        self.draw()

    def draw(self):
        pygame.draw.circle(self.screen.window, self.color,
                (int(self.pos.x), int(self.pos.y)), self.radius, self.thickness)

class Bullet():
    def __init__(self, pos, velocity, screen):
        self.screen = screen
        self.radius = 3
        self.speed = 20
        self.velocity = velocity
        self.velocity.x *= -1
        self.velocity.scale_to_length(self.speed)
        self.pos = pos
        self.thickness = 1

    def update(self):
        self.pos += self.velocity
        self.bounds()
        self.draw()

    def draw(self):
        pygame.draw.circle(self.screen.window, WHITE,
                (int(self.pos.x), int(self.pos.y)),
                self.radius, self.thickness)
        
    def bounds(self):
        if (     self.pos.x > WIDTH + self.radius 
             or self.pos.x < -self.radius
             or self.pos.y > HEIGHT + self.radius
             or self.pos.y < -self.radius
           ):
            self.screen.remove_bullet(self)

class Asteroid:
    def __init__(self, screen, big, pos):
        if pos is None:
           self.pos = self.set_pos()
        else:
            self.pos = pos
        if big:
            self.radius = random.randrange(25, 40)
        else:
            self.radius = random.randrange(10, 20)
        self.big = big
        self.points = self.get_shape()
        self.screen = screen
        self.vel = self.set_vel()
        self.thickness = 2

    def set_pos(self):
        tmp = random.randrange(4)
        offset = 100
        p = Vector2()
        if tmp == 0:
            p.x = offset
            p.y = random.randrange(0, HEIGHT)
        elif tmp == 1:
            p.x = random.randrange(0, WIDTH)
            p.y = offset
        elif tmp == 2:
            p.x = WIDTH - offset
            p.y = random.randrange(0, HEIGHT)
        else:
            p.x = random.randrange(0, WIDTH)
            p.y = HEIGHT - offset
        return p
    
    def set_vel(self):
        v = Vector2(1, 0)
        v = v.rotate(random.randrange(360))
        v.scale_to_length(random.randrange(2, 5))
        return v

    def update(self):
        self.pos += self.vel
        self.update_points()
        self.collision()
        self.bounds()
        self.draw()
    def update_points(self):
        for p in self.points:
            p += self.vel

    def collision(self):
        # test bullet collision
        for b in self.screen.bullets:
            # get distance to bullet
            dist_to_b = (b.pos - self.pos).length()
            # if dist is less than both radius -> collision
            if dist_to_b < b.radius + self.radius:
                self.screen.bullets.remove(b)
                self.divide_asteroid()
                self.screen.create_explosion(self.pos)
                
    def divide_asteroid(self):
        if self.big:
            for i in range(4):
                self.screen.asteroids.append(Asteroid(self.screen, False, Vector2(self.pos)))
        self.screen.asteroids.remove(self)
        self.screen.add_score(20)

    def draw(self):
        # draw collider
        #pygame.draw.circle(self.screen.window, RED,
        #        (int(self.pos.x), int(self.pos.y)), self.radius, 2)
        pygame.draw.polygon(self.screen.window, RED, self.points, 2)

    def bounds(self):
        # move all points to origin
        for p in self.points:
            p -= self.pos

        if self.pos.x > WIDTH + self.radius:
            self.pos.x = - self.radius
        elif self.pos.x < -self.radius:
            self.pos.x = WIDTH + self.radius
        elif self.pos.y > HEIGHT + self.radius:
            self.pos.y = -self.radius
        elif self.pos.y < -self.radius:
            self.pos.y = HEIGHT + self.radius
        # move points back to position
        for p in self.points:
            p += self.pos

    def get_shape(self):
        p = []
        offset = 3
        for i in range(0, 361, 15):
            v = Vector2(1, 0)
            v = v.rotate(i)
            v.scale_to_length(random.randrange(self.radius - offset, self.radius + offset))
            v += self.pos
            p.append(v)
        return p

class Play_Screen:
    def __init__(self, window, font, clock):
        self.window = window
        self.clock = clock
        self.score = 0
        self.score_text = Text(window, 'Score: ' + str(self.score), font, (700, 40))
        self.player = Player(self)
        self.wave = 1
        self.pause = False
        self.lives = 3
        self.bullets = []
        self.asteroids = []
        self.particles = []
        self.explosions = []
        self.init_wave()

    def init_wave(self):
        for i in range(self.wave + 2):
            self.asteroids.append(Asteroid(self, True, None))

    def update(self):
        for asteroid in self.asteroids:
            asteroid.update()
        for bullet in self.bullets:
            bullet.update()
        for particle in self.particles:
            particle.update()
        self.player.update()
        self.draw()
    def draw(self):
        self.score_text.draw()
    def add_score(self, s):
        self.score += s
        self.score_text.text = 'Score: ' + str(self.score)
        self.score_text.update_text()
    def add_bullet(self, b):
        self.bullets.append(b)
    def remove_bullet(self, b):
        self.bullets.remove(b)
    def create_explosion(self, pos):
        parts = 15
        step = int(360 / parts)
        for i in range(0, 361, step):
            vel = Vector2(1, 0)
            vel = vel.rotate(i)
            vel.scale_to_length(5)
            p = Particle(Vector2(pos), vel, 4, 0, 250, YELLOW, self)
            self.particles.append(p)

class Text:
    def __init__(self, window, text, font, pos):
        self.window = window
        self.text = text
        self.font = font
        self.pos = pos
        self.surface = None
        self.rect = None
        self.update_text()
    def update_text(self):
        self.surface = self.font.render(self.text, True, GREEN)
        self.rect = self.surface.get_rect()
        self.rect.center = self.pos
    def draw(self):
        self.window.blit(self.surface, self.rect)

def main():

    # initializa pygame library
    pygame.init()
    # the game will run at 30 frames per second
    FPS = 30
    # create a surface object (like a canvas)
    window = pygame.display.set_mode((WIDTH, HEIGHT))
    # set window title
    pygame.display.set_caption('Holbi Game')
    # time handler
    clock = pygame.time.Clock()
    # global font
    font = pygame.font.Font('freesansbold.ttf', 32)
    #play screen
    game_screen = Play_Screen(window, font, clock)
    # main game loop
    while True:
        window.fill(BLACK)

        game_screen.update()

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

