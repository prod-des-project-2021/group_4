import pygame
import math
import random


from pygame.constants import JOYHATMOTION, MOUSEBUTTONDOWN

from GameObjects import Player
from GameObjects import Bullet
from GameObjects import ParticleEmitter

from pygame import transform
from pygame.draw import rect
from pygame.transform import rotate

pygame.init()

#resolitions in 16:9 aspect ratio: 720p=1280x720, 1080p=1920x1080
#resolutions in 1:1 aspect ratio (that look good): 600x600, 900x900
displaywidth = 1024
displayheight = 768
screen = pygame.display.set_mode((displaywidth, displayheight))


#Caption
pygame.display.set_caption("Multiplayer Game")

#Player values
angle = 0
#x = 50
#y = 50
bullets = []
enemies = []
tickrate = 120
lastshot = 0        
firerate = 4        #shots per second (keep under tickrate since maximum amount of bullets created per tick is one)
bulletspeed = 8
width = 64
height = 64
basespeed = 4
slowmodifier = 0.5
#vel = basespeed



#colors
grey = 75,75,75
green = 0,255,0
red = 255,0,0
blue = 0,0,255
yellow = 255,255,0
white = 255,255,255
black = 0,0,0


class Square:
    def __init__(self, color, x, y, width, height, speed):
        self.rect = pygame.Rect(x,y,width,height)
        self.color = color
        self.speed = speed
    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)

class Enemy(Square):
    def __init__(self, color, ex, ey, width, height):
        self.rect = pygame.Rect(ex,ey, width, height)
        self.width = width
        self.height = height
        self.x = ex
        self.y = ey
        self.color = color

    def moveEnemy(self):
        self.dx = 0                           #most of these are useless when we get other players from server
        self.dy = basespeed * slowmodifier    #here for testing only (get these from server at some point)
        self.x = self.x + self.dx
        self.y = self.y + self.dy       
        self.rect.x = int(self.x)
        self.rect.y = int(self.y)

def rotate(surface,angle,width,height):
   rotated_surface = pygame.transform.rotozoom(surface,angle,1)
   rotated_rect = rotated_surface.get_rect(center = (width,height))
   return rotated_surface, rotated_rect

if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((displaywidth,displayheight), pygame.RESIZABLE, vsync=1)
    clock = pygame.time.Clock()

    running = True

    playerImg = pygame.image.load('res/player.png')
    enemyImg = pygame.image.load('res/enemy.png')
    engineTrailImg = pygame.image.load('res/engine_trail_particle.png')
    bulletImg = pygame.image.load('res/ammo_small.png')

    player = Player(playerImg)
    playerEngineTrail = ParticleEmitter(engineTrailImg)

    
    while(running):
        Player.ZERO_X = pygame.display.Info().current_w /  2
        Player.ZERO_Y = pygame.display.Info().current_h /  2
        mouse_x, mouse_y = pygame.mouse.get_pos()
        player_angle = math.atan2(mouse_x - player.position.x, mouse_y - player.position.y)
        player.setAngle(player_angle)
        mousebuttons = pygame.mouse.get_pressed()

        screen.fill(black)
        playerEngineTrail.draw(screen)
        player.draw(screen)
        
        
        playerEngineTrail.updatePosition(player.position.x, player.position.y)
        if mousebuttons[2]:
            playerEngineTrail.addParticle(15, -player.direction*5)
        player.update(mousebuttons[2])   
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouseDown = True
            elif event.type == pygame.MOUSEBUTTONUP:
                mouseDown = False

        #randomized enemies for testing purposes
        if random.randint(1,60) == 1:
            ex = random.randint(1, displaywidth - width)
            e = Enemy(green, ex, 0, width, height)
            enemies.append(e)

        if mousebuttons[0]:
            if lastshot > tickrate/firerate:
                #targetX, targetY = pygame.mouse.get_pos()
                #print(targetX,targetY) #comment this later
                b = Bullet(bulletImg, (player.position.x-9), (player.position.y-9), bulletspeed, -player.angle)
                bullets.append(b)
                lastshot = 0

        for b in bullets:
            if b.x > displaywidth or b.x <= 0:
                bullets.remove(b)
            elif b.y > displayheight or b.y <= 0:
                bullets.remove(b)
        lastshot+=1
        
        
        for b in bullets:
            b.moveBullet()
            b.draw(screen)
            for e in enemies:
                if b.rect.colliderect(e.rect):
                    enemies.remove(e)
                    bullets.remove(b)
                    

        for e in enemies:
            e.moveEnemy()
            e.draw(screen)
            if e.rect.y > displayheight:
                enemies.remove(e)



        clock.tick(tickrate)
        pygame.display.flip()

pygame.quit()