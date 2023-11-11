import pygame
from random import randint
from constants import SCREEN_WIDTH, SCREEN_HEIGHT


class Particle(pygame.sprite.Sprite):
    def __init__(self,
                 groups: pygame.sprite.Group,
                 pos: list[int],
                 color: str,
                 direction: pygame.math.Vector2,
                 speed: int):
        super().__init__(groups)
        self.pos = pos
        self.color = color
        self.direction = direction
        self.speed = speed
        self.alpha = 255
        self.fade_speed = 200
        self.size = 4

        self.create_surf()

    def create_surf(self):
        self.image = pygame.Surface((self.size, self.size)).convert_alpha()
        self.image.set_colorkey("black")
        pygame.draw.circle(surface=self.image, color=self.color, center=(self.size / 2, self.size / 2), radius=self.size / 2)
        self.rect = self.image.get_rect(center=self.pos)

    def move(self, dt):
        self.pos += self.direction * self.speed * dt
        self.rect.center = self.pos

    def fade(self, dt):
        self.alpha -= self.fade_speed * dt
        self.image.set_alpha(self.alpha)

    def check_pos(self):
        if (
            self.pos[0] < -50 or
            self.pos[0] > SCREEN_WIDTH + 50 or
            self.pos[1] < -50 or
            self.pos[1] > SCREEN_HEIGHT + 50
        ):
            self.kill()

    def check_alpha(self):
        if self.alpha <= 0:
            self.kill()

    def update(self, dt):
        self.move(dt)
        self.fade(dt)
        self.check_pos()
        self.check_alpha()


class ExplodingParticle(Particle):
    def __init__(self,
                 groups: pygame.sprite.Group,
                 pos: list[int],
                 color: str,
                 direction: pygame.math.Vector2,
                 speed: int):
        super().__init__(groups, pos, color, direction, speed)
        self.t0 = pygame.time.get_ticks()
        self.lifetime = randint(1000, 1200)
        self.exploding = False
        self.size = 4
        self.max_size = 50
        self.inflate_speed = 500
        self.fade_speed = 3000

    def explosion_timer(self):
        if not self.exploding:
            t = pygame.time.get_ticks()
            if t - self.t0 > self.lifetime:
                self.exploding = True

    def inflate(self, dt):
        self.size += self.inflate_speed * dt
        self.create_surf()

    def check_size(self):
        if self.size > self.max_size:
            self.kill()

    def update(self, dt):
        self.move(dt)
        self.explosion_timer()
        if self.exploding:
            self.inflate(dt)
            self.fade(dt)

        self.check_pos()
        self.check_size()
        self.check_alpha()


class FloatingParticle(Particle):
    def __init__(self,
                 groups: pygame.sprite.Group,
                 pos: list[int],
                 color: str,
                 direction: pygame.math.Vector2,
                 speed: int):
        super().__init__(groups, pos, color, direction, speed)
