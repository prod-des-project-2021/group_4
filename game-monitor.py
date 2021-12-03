import pygame 
import sys
from pygame.math import Vector2
from networking import Service
from networking import Client
from networking import Packet
from server import *

pygame.init()
widthWindow = 1024
heightWindow = 768
tickrate = 120
screen = pygame.display.set_mode((widthWindow, heightWindow))
pygame.display.set_caption("Tracking monitor")
font = pygame.font.SysFont('Arial', 14)


class GameMonitor:
    def __init__(self, players): #rockets, bullets
        self.players = players
       # self.rockets = rockets
       # self.bullets = bullets
        
        
    def draw(self):
        for player in self.players:
            pygame.draw.rect(screen, (255,0,0), player.position.x, player.position.y, 32,32)
            screen.blit(self.font.render(player.health),True,(0,255,0),player.position.x,player.position.y)

        #for Bullet in bullets:
            #pygame.draw.rect(screen,(0,0,255), Bullet.position.x, Bullet.position.y, 8,8)

        #for Rocket in rockets:
            #pygame.draw.rect(screen,(0,255,0), Rocket.position.x, Rocket.position.y, 16,16)
    

if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((widthWindow,heightWindow), pygame.RESIZABLE, vsync=1)
    clock = pygame.time.Clock()
    gm = GameMonitor()
    running = True
    while (running):
        gm.draw()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
    clock.tick(tickrate)
    pygame.display.flip()
            
pygame.quit()
    