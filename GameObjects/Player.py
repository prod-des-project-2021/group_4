import pygame
import math
from pygame.math import Vector2
import random

ZERO_X = 1920/2
ZERO_Y = 1080/2

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

class Player:
    def __init__(self, sprite):
        self.sprite = sprite
        # rewritten movement with vectors
        self.position = Vector2(ZERO_X, ZERO_Y)
        self.UP = Vector2(0, 1)
        self.direction = Vector2(0, 1)
        self.velocity = Vector2(0, 0)
        self.acceleration = 0.05
        self.angle = 0.0
        self.rotatedSprite = None
        self.rotate() # initialize the rotated sprite
        self.max_velocity = 4.0
        self.accelerating = 0
        self.shooting = 0
        self.max_health = 100
        self.health = self.max_health
          
    def draw(self, screen):
        screen.blit(self.rotatedSprite, (int(self.position.x-self.dimensions.width/2), int(self.position.y-self.dimensions.height/2)))
        pygame.draw.line(screen, (255,255,255), (ZERO_X, 0), (ZERO_X, ZERO_Y*2))
        pygame.draw.line(screen, (255,255,255), (0, ZERO_Y), (ZERO_X*2, ZERO_Y))
        pygame.draw.line(screen, (255,0,0), (ZERO_X, ZERO_Y), (ZERO_X+self.direction.x*50, ZERO_Y+self.direction.y*50))
        pygame.draw.line(screen, (0,255,0), (ZERO_X, ZERO_Y), (ZERO_X+self.velocity.x*20, ZERO_Y+self.velocity.y*20))

    def rotate(self):
        self.direction = Vector2(self.UP)
        self.direction.rotate_ip(-self.angle)
        self.rotatedSprite = pygame.transform.rotate(self.sprite, int(self.angle)-90)
        self.dimensions = self.rotatedSprite.get_rect()

    def setAngle(self,angle):
        self.angle = radToDec(angle)

    def update(self, accelerating):
        if(accelerating):
            self.accelerating = 1
            # limiting the velocity
            # guess it's little hacky but whatever
            tempVelocity = Vector2(self.velocity)
            tempVelocity += self.direction * self.acceleration
            # if incrementing velocity doesn't exceed max, allow it
            if(tempVelocity.length() < self.max_velocity):
                self.velocity += self.direction * self.acceleration

        else:
            self.accelerating = 0
            if(self.velocity.length() > 0):
                # braking vector
                braking = Vector2(0.15, 0.15)
                rotation_angle = braking.angle_to(self.velocity)
                braking.rotate_ip(rotation_angle)
                self.velocity -= braking/2
                # if velocity is smaller than braking, just zero it
                if(self.velocity.length() < braking.length()):
                    self.velocity = Vector2(0,0)    
        
        #restricting player position
        if self.position.x >= 1920:
            self.velocity = Vector2(0,0)
            self.position.x -= 20
        if self.position.y >= 1080:
            self.velocity = Vector2(0,0)
            self.position.y -= 20
        if self.position.x <= 0:
            self.velocity = Vector2(0,0)
            self.position.x += 20
        if self.position.y <= 0:
            self.velocity = Vector2(0,0)
            self.position.y += 20

        self.position += self.velocity
        self.rotate()
       
def radToDec(rad):
    return (rad*180/math.pi)

def decToRad(dec):
    return (dec/180*math.pi)
