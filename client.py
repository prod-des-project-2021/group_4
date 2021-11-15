import pygame
import math
import random
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
angle = 0
x = 50
y = 50
bullets = []
enemies = []
tickrate = 60
lastshot = 0        
firerate = 4        #shots per second (keep under tickrate since maximum amount of bullets created per tick is one)
width = 64
height = 64
basespeed = 4
boostmodifier = 2
boostspeed = basespeed * boostmodifier
boostfuel = 100
maxboostfuel = 300
slowmodifier = 0.4
vel = basespeed

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

class Bullet(Square):
    def __init__(self, color, x, y, width, height, speed, targetX, targetY):
        super().__init__(color, x, y, width, height, speed)
        angle = math.atan2(targetY-y, targetX-x) #radians
        #  ^^  send bullet angle to server whenever you are at that point
        self.dx = math.cos(angle)*speed
        self.dy = math.sin(angle)*speed
        self.x = x
        self.y = y

    def moveBullet(self):
        self.x = self.x + self.dx
        self.y = self.y + self.dy
        self.rect.x = int(self.x)
        self.rect.y = int(self.y)

def updatePlayer(x,y):
    mousex,mousey = pygame.mouse.get_pos()
    angle = math.atan2(mousex - x, mousey - y)
    playrot = pygame.transform.rotozoom(playerImg,int(angle*180/math.pi)-180,1)
    playpos = (x - playrot.get_rect().width/2,y - playrot.get_rect().height/2)
    screen.blit(playrot, playpos)
    pygame.display.update()
    #updateServer() or something similar here

class Enemy(Square):
    def __init__(self, color, x, y, width, height, tempspeed):
        self.rect = pygame.Rect(x,y, width, height)
        self.x = x
        self.y = y
        self.color = color

    def moveEnemy(self):
        self.dx = 0                           #most of these are useless when we get other players from server
        self.dy = basespeed * slowmodifier    #here for testing only (get these from server at some point)
        self.x = self.x + self.dx
        self.y = self.y + self.dy       
        self.rect.x = int(self.x)
        self.rect.y = int(self.y)


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
        e = Enemy(green, ex, 0, width, height, 4)
        enemies.append(e)

    if buttons[pygame.K_a] and buttons[pygame.K_w] and x > vel and y > vel:
        x += slowmodifier * vel
        y += slowmodifier * vel
    if buttons[pygame.K_a] and buttons[pygame.K_s] and x > vel and y < displaywidth - height - vel:
        x += slowmodifier * vel
        y -= slowmodifier * vel   
    if buttons[pygame.K_d] and buttons[pygame.K_w] and x < displaywidth - width + vel and y > vel:
        x -= slowmodifier * vel
        y += slowmodifier * vel
    if buttons[pygame.K_d] and buttons[pygame.K_s] and x < displaywidth - width + vel and y< displaywidth - height - vel:
        x -= slowmodifier * vel
        y -= slowmodifier * vel
    
    if buttons[pygame.K_a] and x > vel:
        x -= vel
    if buttons[pygame.K_d] and x < displaywidth - width + vel:
        x += vel
    if buttons[pygame.K_w] and y > vel:
        y -= vel
    if buttons[pygame.K_s] and y < displaywidth - height - vel:
        y += vel

    if mousebuttons[0]:
        if lastshot > tickrate/firerate:
            targetX, targetY = pygame.mouse.get_pos()
            #print(targetX,targetY) #comment this later
            b = Bullet(red, (x), (y), 20, 4, 10, targetX, targetY)
            bullets.append(b)
            lastshot = 0

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
    
    for b in bullets:
        if b.rect.x > displaywidth or b.rect.x <= 0:
            bullets.remove(b)
        elif b.rect.y > displayheight or b.rect.y <= 0:
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
        b.draw(screen)
    updatePlayer(x,y)

    
pygame.quit()