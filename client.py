import pygame

pygame.init()

screen = pygame.display.set_mode((600,600))

pygame.display.set_caption("Multiplayer Game")

playerImg = pygame.image.load('player.png')
x = 50
y = 50
width = 64
height = 64
vel = 15

def player():
    screen.blit(playerImg,(x,y))
    pygame.display.update()

running = True
while running:
    pygame.time.delay(100)
    screen.fill((255, 255, 255
    ))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    buttons = pygame.key.get_pressed()

    if buttons[pygame.K_LEFT]:
        x -= vel
    if buttons[pygame.K_RIGHT]:
        x += vel
    if buttons[pygame.K_UP]:
        y -= vel
    if buttons[pygame.K_DOWN]:
        y += vel
    player()
   
    

pygame.quit()