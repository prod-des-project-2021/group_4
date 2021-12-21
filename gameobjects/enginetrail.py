import pygame
from pygame.math import Vector2
import random

class ParticleEmitter:
    def __init__(self, sprite):
        self.sprite = sprite
        self.particles = list()
        self.x = 0
        self.y = 0

    def updatePosition(self, x, y):
        self.x = x
        self.y = y

    def draw(self, screen):
        for particle in self.particles:
            particle.lifetime = particle.lifetime - 1
            if particle.lifetime == 0:
                self.particles.remove(particle)
            particle.draw(screen)

    def addParticle(self, lifetime, velocity):
        self.particles.append(Particle(self.sprite, self.x, self.y, lifetime, velocity))

class Particle:
    def __init__(self, sprite, position_x, position_y, lifetime, velocity):
        self.sprite = sprite.copy()
        self.dimensions = sprite.get_rect()
        self.lifetime = lifetime
        self.total_lifetime = lifetime
        self.position = Vector2(position_x-self.dimensions.width/2, position_y-self.dimensions.height/2)
        self.velocity = Vector2(velocity)
        self.velocity.rotate_ip(random.randint(1,20))

    def draw(self, screen):
        self.position += self.velocity
        self.sprite.set_alpha(self.lifetime/self.total_lifetime*255)
        screen.blit(self.sprite, (int(self.position.x), int(self.position.y)))
