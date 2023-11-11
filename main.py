import pygame
from random import choice, randint, uniform
from constants import SCREEN_WIDTH, SCREEN_HEIGHT
from particles import Particle, ExplodingParticle, FloatingParticle

display_surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()

particle_group = pygame.sprite.Group()

floating_particle_timer = pygame.event.custom_type()
pygame.time.set_timer(floating_particle_timer, 10)


def spawn_particles(n: int):
    for _ in range(n):
        pos = pygame.mouse.get_pos()
        color = choice(("red", "green", "blue"))
        direction = pygame.math.Vector2(uniform(-1, 1), uniform(-1, 1))
        direction = direction.normalize()
        speed = randint(50, 400)
        Particle(particle_group, pos, color, direction, speed)


def spawn_exploding_particles(n: int):
    for _ in range(n):
        pos = pygame.mouse.get_pos()
        color = choice(("red", "yellow", "orange"))
        direction = pygame.math.Vector2(uniform(-0.2, 0.2), uniform(-1, 0))
        direction = direction.normalize()
        speed = randint(50, 400)
        ExplodingParticle(particle_group, pos, color, direction, speed)


def spawn_floating_particle():
    init_pos = pygame.mouse.get_pos()
    pos = init_pos[0] + randint(-10, 10), init_pos[1] + randint(-10, 10)
    color = "white"
    direction = pygame.math.Vector2(0, -1)
    speed = randint(50, 100)
    FloatingParticle(particle_group, pos, color, direction, speed)


def main_loop():
    while True:
        # events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed()[0]:
                    spawn_particles(1000)
                elif pygame.mouse.get_pressed()[2]:
                    spawn_exploding_particles(1000)
            if event.type == floating_particle_timer:
                spawn_floating_particle()

        # clock
        dt = clock.tick() / 1000

        # display
        display_surface.fill("black")
        particle_group.draw(display_surface)

        # update
        particle_group.update(dt)
        pygame.display.update()


if __name__ == "__main__":
    pygame.init()
    main_loop()
