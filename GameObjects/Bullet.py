import math
import pygame


class Bullet:
    def __init__(self, image, x, y, speed, targetX, targetY):
        
        self.angle = math.atan2(targetY-y, targetX-x) #radians
        #  ^^  send bullet angle to server whenever you are at that point
        self.image = pygame.transform.rotozoom(image, int(-1*self.angle*180/math.pi)-90, 1)
        self.dx = math.cos(self.angle)*speed
        self.dy = math.sin(self.angle)*speed
        self.x = x
        self.y = y

    def draw(self,screen):
        screen.blit(self.image,(self.x,self.y))


    def moveBullet(self):
        self.x = self.x + self.dx
        self.y = self.y + self.dy
        self.x = int(self.x)
        self.y = int(self.y)