import pygame
import math

from pygame.transform import rotate

pygame.init()

#resolitions in 16:9 aspect ratio: 720p=1280x720, 1080p=1920x1080
#resolutions in 1:1 aspect ratio (that look good): 600x600, 900x900
displaywidth = 900
displayheight = 900
screen = pygame.display.set_mode((displaywidth, displayheight))

pygame.display.set_caption("Multiplayer Game")

playerImg = pygame.image.load('player.png')
angle = 0
x = 50
y = 50
width = 64
height = 64
basespeed = 2
boostmodifier = 2
boostspeed = basespeed * boostmodifier
slowmodifier = 0.5
vel = basespeed
rect = playerImg.get_rect(center=(x,y))


def player():
    screen.blit(playerImg2,rect)
    pygame.display.update()
    

running = True
while running:
    #frame rate: 7 = about 142.9 fps, 17 = about 58.8 fps, 10 = exactly 100 fps
    pygame.time.delay(10)
    screen.fill((255, 255, 255))
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
   
    angle +=1
    playerImg2 = pygame.transform.rotate(playerImg,angle)
    rect = playerImg.get_rect(center=rect.center)
    
    if buttons[pygame.K_a] and x > vel:
        x -= vel
    if buttons[pygame.K_d] and x < displaywidth - width + vel:
        x += vel
    if buttons[pygame.K_w] and y > vel:
        y -= vel
    if buttons[pygame.K_s] and y < displaywidth - height - vel:
        y += vel

    if buttons[pygame.K_SPACE]:
        vel = boostspeed
    else:
        vel = basespeed

    player()
    
pygame.quit()