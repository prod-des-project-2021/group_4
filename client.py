import pygame
import math
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
playerImg = pygame.image.load('player.png')
angle = 0
x = 50
y = 50
bullets = []
width = 64
height = 64
basespeed = 4
boostmodifier = 2
boostspeed = basespeed * boostmodifier
boostfuel = 100
maxboostfuel = 300
slowmodifier = 0.4
vel = basespeed
green = 0,255,0
red = 255,0,0
blue = 0,0,255
yellow = 255,255,0
white = 255,255,255
black = 0,0,0

#Bullet
bulletImg = pygame.image.load('bullet1.png')
bulletX = x
bulletY = y

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
        self.dx = math.cos(angle)*speed
        self.dy = math.sin(angle)*speed
        self.x = x
        self.y = y
    def moveBullet(self):
        self.rect.x = self.rect.x + float(self.dx)
        self.rect.y = self.rect.y + float(self.dy)

def updatePlayer(x2,y2):
    screen.blit(playerImg, (x2, y2))
    pygame.display.update()

running = True
while running:
    #frame rate: 7 = about 142.9 fps, 17 = about 58.8 fps, 10 = exactly 100 fps
    clock.tick(60)
    screen.fill((white))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    buttons = pygame.key.get_pressed()

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

    if event.type == pygame.MOUSEBUTTONDOWN:
        targetX, targetY = pygame.mouse.get_pos()
        print(targetX,targetY) #comment this later
        b = Bullet(red, (x+width/2), (y+height/2), 20, 20, 10, targetX, targetY)
        bullets.append(b)

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
    
    screen.fill(white)
    for b in bullets:
        b.moveBullet()
        b.draw(screen)

    updatePlayer(x,y)
    
pygame.quit()