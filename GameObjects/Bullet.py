import math
import pygame

class Bullet:
    def __init__(self, image, x, y, speed, angle):
        self.angle = angle+90
        #  ^^  send bullet angle to server whenever you are at that point
        self.image = pygame.transform.rotozoom(image, int(-1*self.angle), 1)
        self.dx = math.cos(self.angle/180*math.pi)*speed
        self.dy = math.sin(self.angle/180*math.pi)*speed
        self.width = 16
        self.height = 16
        self.x = x
        self.y = y

    def draw(self,screen):
        screen.blit(self.image,(self.x,self.y))

    def moveBullet(self):
        self.x = self.x + self.dx
        self.y = self.y + self.dy
        self.rect = self.image.get_rect(topleft=(self.x,self.y))
        