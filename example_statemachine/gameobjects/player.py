from .gameobject import GameObject
from .textobject import TextObject
from .enginetrail import ParticleEmitter, Particle
from pygame.math import Vector2
import pygame

class Player(GameObject):
    def __init__(self, sprite, enginetrailSprite):
        super().__init__(sprite)

        self.accelerating   = False
        self.shooting       = False
        self.acceleration   = 0.05
        self.braking        = 0.05
        self.max_velocity   = 4.0
        self.velocity       = Vector2(0,0)
        self.reloadTime     = 0
        self.reload         = 20 # how many ticks it takes to reload

        self.nickname = "Player 1"
        self.nickname_text = TextObject(self.nickname, "Arial", (255,255,255))

        self.alive = True
        self.health = 100
        self.max_health = 100
        self.shield = 100
        self.max_shield = 100

        self.engine_trail = ParticleEmitter(enginetrailSprite)

    def draw(self, screen):
        if(self.alive):
            super().draw(screen)
            pygame.draw.rect(screen, (0,0,255), (self.position.x - 25, self.position.y+25, int(self.shield/2), 5))
            pygame.draw.rect(screen, (255,0,0), (self.position.x - 25, self.position.y+32, int(self.health/2), 5))
            self.engine_trail.draw(screen)
            self.nickname_text.draw(screen)

    def setNickname(self, nickname):
        self.nickname = nickname
        self.nickname_text = TextObject(self.nickname, "Arial", (255,255,255))

    def damage(self):
        if(self.shield > 0):
            self.shield -= 50
        else:
            if(self.health > 0):
                self.health -= 25

        if(self.health <= 0):
            self.alive = False

    def update(self):
        # updating the nickname text position
        self.nickname_text.setPosition(self.position.x-20, self.position.y-40)

        # updating the particle emitters position
        trailpos = self.getAttachmentPoint(-10,0)
        self.engine_trail.updatePosition(trailpos.x, trailpos.y)

        if(self.shield < self.max_shield and self.alive):
            self.shield += 0.2

        if(self.reloadTime > 0):
            self.reloadTime -= 1

        if(self.accelerating):
            # adding particles to engine trail
            self.engine_trail.addParticle(15, -self.direction*5)

            # calculating the next velocity
            tempVelocity = Vector2(self.velocity)
            tempVelocity += self.direction * self.acceleration
            # if incrementing velocity doesn't exceed max, allow it
            if(tempVelocity.length() < self.max_velocity):
                self.velocity += self.direction * self.acceleration
        else:
            if(self.velocity.length() > 0):
                braking_vector = Vector2(self.braking, self.braking)
                rotation_angle = braking_vector.angle_to(self.velocity)
                braking_vector.rotate_ip(rotation_angle)
                self.velocity -= braking_vector

            if(self.velocity.length() > 0 and self.velocity.length() < self.braking):
                self.velocity = Vector2(0,0)

        self.position += self.velocity

    def setState(self, btn1, btn2):
        self.shooting = btn1
        self.accelerating = btn2
