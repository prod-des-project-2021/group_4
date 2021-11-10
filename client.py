import pygame
import math


from pygame.transform import rotate

pygame.init()

#resolitions in 16:9 aspect ratio: 720p=1280x720, 1080p=1920x1080
#resolutions in 1:1 aspect ratio (that look good): 600x600, 900x900
displaywidth = 900
displayheight = 900
screen = pygame.display.set_mode((displaywidth, displayheight))

#Caption
pygame.display.set_caption("Multiplayer Game")

#Player values
playerImg = pygame.image.load('player.png')
angle = 0
x = 50
y = 50
width = 64
height = 64
basespeed = 2
boostmodifier = 2
boostspeed = basespeed * boostmodifier
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




def updateScreen(x2,y2):
    screen.blit(playerImg, (x2, y2))
    pygame.display.update()
    
def fire_bullet(x2,y2):
    y2 -= 10
    screen.blit(bulletImg,(x2 + 9 ,y2))

running = True
while running:
    #frame rate: 7 = about 142.9 fps, 17 = about 58.8 fps, 10 = exactly 100 fps
    pygame.time.delay(10)
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
    if buttons[pygame.K_x]:
        if bulletY < 0:
         bulletX = x
         bulletY = y
         fire_bullet(bulletX,bulletY)
    if bulletY >= 0:
        bulletY -= 5
        fire_bullet(bulletX,bulletY)
    if buttons[pygame.K_SPACE]:
        vel = boostspeed
    else:
        vel = basespeed
    
        
    
    updateScreen(x,y)
    
pygame.quit()