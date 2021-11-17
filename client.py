import pygame
import math
import random

from pygame.constants import JOYHATMOTION

from GameObjects import Bullet

from pygame import transform
from pygame.draw import rect
from pygame.transform import rotate

pygame.init()

#resolitions in 16:9 aspect ratio: 720p=1280x720, 1080p=1920x1080
#resolutions in 1:1 aspect ratio (that look good): 600x600, 900x900
displaywidth = 900
displayheight = 900
screen = pygame.display.set_mode((displaywidth, displayheight))
clock = pygame.time.Clock()

#Caption
pygame.display.set_caption("Multiplayer Game")

#Player values
playerImg = pygame.image.load('player2.png')
bulletImg = pygame.image.load('bullet2.png')
angle = 0
x = 50
y = 50
bullets = []
enemies = []
tickrate = 60
lastshot = 0        
firerate = 4        #shots per second (keep under tickrate since maximum amount of bullets created per tick is one)
bulletspeed = 10
width = 64
height = 64
basespeed = 4
boostmodifier = 2
boostspeed = basespeed * boostmodifier
boostfuel = 100
maxboostfuel = 300
slowmodifier = 0.5
vel = basespeed
goforeward = 0
gobackward = 0
goleft = 0
goright = 0

#colors
grey = 75,75,75
green = 0,255,0
red = 255,0,0
blue = 0,0,255
yellow = 255,255,0
white = 255,255,255
black = 0,0,0


def updatePlayer():
    mousex,mousey = pygame.mouse.get_pos()
    global goforeward, angle, vel, x, y

    if goforeward == 1:
        x += math.sin(angle) * vel
        y += math.cos(angle) * vel
    
    
    if x > displaywidth - vel or y > displayheight - vel:
            x -= vel + 32
            y -= vel + 32
    elif x < 0 + vel or y < 0 + vel:
            x += vel + 32
            y += vel + 32

    angle = math.atan2(mousex - x, mousey - y)
    playrot = pygame.transform.rotozoom(playerImg,int(angle*180/math.pi)-180,1)
    playpos = (x - playrot.get_rect().width/2,y - playrot.get_rect().height/2)
    screen.blit(playrot, playpos)
    pygame.display.update()
    #updateServer() or something similar here

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

running = True
while running:
    clock.tick(tickrate)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    buttons = pygame.key.get_pressed()
    mousebuttons = pygame.mouse.get_pressed()

    #randomized enemies for testing purposes
    if random.randint(1,60) == 1:
        ex = random.randint(1, displaywidth - width)
        e = Enemy(green, ex, 0, width, height)
        enemies.append(e)

    if buttons[pygame.K_SPACE]:
        if boostfuel > 0:
            vel = boostspeed
            boostfuel -= 2
        else:
            vel = basespeed
    else:
        vel = basespeed
        if boostfuel < maxboostfuel:
            boostfuel += 1
    if buttons[pygame.K_w]:
        goforeward = 1
    else:
        goforeward = 0

    if mousebuttons[0]:
        if lastshot > tickrate/firerate:
            #targetX, targetY = pygame.mouse.get_pos()
            #print(targetX,targetY) #comment this later
            b = Bullet(bulletImg, (x-9), (y-9), bulletspeed, -angle + math.pi/2 )
            bullets.append(b)
            lastshot = 0

    for b in bullets:
        if b.x > displaywidth or b.x <= 0:
            bullets.remove(b)
        elif b.y > displayheight or b.y <= 0:
            bullets.remove(b)
    lastshot+=1
    screen.fill(grey)

    for e in enemies:
        e.moveEnemy()
        e.draw(screen)
        if e.rect.y > displayheight:
            enemies.remove(e)

    for b in bullets:
        b.moveBullet()
        for e in enemies:
            if b.rect.colliderect(e.rect):
                enemies.remove(e)
                bullets.remove(b)
        b.draw(screen)

    updatePlayer()

pygame.quit()