import pygame
from pygame.math import Vector2
import math

class GameObject:
    def __init__(self, sprite):
        self.NORMAL_VECTOR  = Vector2(0, 1) # all rotations are based on this normal vector
        self.id             = 0 # 0 is reserved for local objects
        self.sprite         = sprite
        self.rotatedSprite  = None

        self.position   = Vector2(0,0)
        self.angle      = 0.0 # angle in DEGREES
        self.angle_offset = 0
        self.direction  = Vector2(0,0)

        self.rotate() # generates the rotatedSprite
        self.dimensions = self.rotatedSprite.get_rect()

    def rotate(self):
        # Clone the normal vector
        self.direction = Vector2(self.NORMAL_VECTOR)

        # Rotate the normal vector by degrees
        self.direction.rotate_ip(-self.angle)
        self.rotatedSprite = pygame.transform.rotozoom(self.sprite, int(self.angle) + self.angle_offset, 1.0)
        self.dimensions = self.rotatedSprite.get_rect()

    def update(self):
        # Override this method
        pass

    def draw(self, screen):
        # objects center point is at xy at all times
        screen.blit(self.rotatedSprite, (int(self.position.x-self.dimensions.width/2), int(self.position.y-self.dimensions.height/2)))

    # collision detection
    def colliding(self, gameobject, type = "rect"):
        if(type == "rect"):
            return (self.position.x < gameobject.position.x + gameobject.dimensions.width and
            self.position.x + self.dimensions.width > gameobject.position.x and
            self.position.y < gameobject.position.y + gameobject.dimensions.height and
            self.dimensions.height + self.position.y > gameobject.position.y)
        elif(type == "circle"):
            # calculating average radius if w and h are different
            self_radius = (self.dimensions.width / 2 + self.dimensions.height / 2) / 2
            gameobject_radius = (gameobject.dimensions.width / 2 + gameobject.dimensions.height / 2) / 2

            # calculating the distance between center points
            distance = math.sqrt((gameobject.position.x - self.position.x)**2 + (gameobject.position.y - self.position.y)**2)
            return distance < (self_radius + gameobject_radius)

        return False

    def setPosition(self, x, y):
        self.position.x = x
        self.position.y = y

    def setAngle(self, angle):
        self.angle = angle
        self.rotate()

    # angle offset only for drawing!
    def setAngleOffset(self, angle):
        self.angle_offset = angle

    def copyAngle(self, gameobject):
        self.angle = gameobject.angle
        self.rotate()

    def copyPosition(self, gameobject):
        self.position.x = gameobject.position.x
        self.position.y = gameobject.position.y

    # attach something to gameobject
    # specify the offsets at 0 angle
    # and they are rotated automatically
    def getAttachmentPoint(self, x, y):
        point = Vector2(x, y)
        point_angle = point.angle_to(self.direction)
        point_angle2 = point.angle_to(Vector2(0,0))
        point.rotate_ip(point_angle-point_angle2)
        return Vector2(self.position.x+point.x, self.position.y+point.y)
