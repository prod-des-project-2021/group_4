import pygame, math, random, struct
from pygame.constants import JOYHATMOTION, MOUSEBUTTONDOWN
from GameObjects import Player, Bullet, ParticleEmitter, DestroyEnemy
from pygame import Rect, transform
from pygame.draw import rect
from pygame.transform import rotate
from networking import Client, Packet
import gamepackets

pygame.init()

#resolitions in 16:9 aspect ratio: 720p=1280x720, 1080p=1920x1080
#resolutions in 1:1 aspect ratio (that look good): 600x600, 900x900
displaywidth = 1920
displayheight = 1080
screen = pygame.display.set_mode((displaywidth, displayheight))

destroyEnemyGroup = pygame.sprite.Group() #Create group for the sprites

#Caption
pygame.display.set_caption("Multiplayer Game")

#Background
background = pygame.image.load("space.jpg")
background = pygame.transform.scale(background, (1920, 1080))

#Player values
bullets = []
enemies = []
tickrate = 120
lastshot = 0        
firerate = 2        #shots per second (keep under tickrate since maximum amount of bullets created per tick is one)
bulletspeed = 8
width = 64
height = 64
playerlist = list()
own_id = 0



#colors
grey = 75,75,75
green = 0,255,0
red = 255,0,0
blue = 0,0,255
yellow = 255,255,0
white = 255,255,255
black = 0,0,0


def rotate(surface,angle,width,height):
   rotated_surface = pygame.transform.rotozoom(surface,angle,1)
   rotated_rect = rotated_surface.get_rect(center = (width,height))
   return rotated_surface, rotated_rect

def onReceive(client, packet):
    global playerlist
    global own_id
    if packet.type == gamepackets.GAME_STATE:
        own_id, playerlist = gamepackets.gamestate_unpack(packet.payload)
      

if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((displaywidth,displayheight), pygame.RESIZABLE, vsync=1)
    clock = pygame.time.Clock()
    running = True

    client = Client("135.181.97.38", 5555)
    client.onReceive = onReceive
    client.start()

    playerImg = pygame.image.load('res/player.png')
    enemyImg = pygame.image.load('res/enemy.png')
    engineTrailImg = pygame.image.load('res/engine_trail_particle.png')
    bulletImg = pygame.image.load('res/ammo_small.png')

    player = Player(playerImg)
    playerEngineTrail = ParticleEmitter(engineTrailImg)
    
    while(running):
        screen.fill(black)
        screen.blit(background,(0,0))
        Player.ZERO_X = pygame.display.Info().current_w /  2
        Player.ZERO_Y = pygame.display.Info().current_h /  2
        mouse_x, mouse_y = pygame.mouse.get_pos()
        player_angle = math.atan2(mouse_x - player.position.x, mouse_y - player.position.y)
        player.setAngle(player_angle)
        mousebuttons = pygame.mouse.get_pressed()
        playerEngineTrail.draw(screen)
        player.draw(screen)
        playerEngineTrail.updatePosition(player.position.x, player.position.y)

        if mousebuttons[2]:
            playerEngineTrail.addParticle(15, -player.direction*5)
        player.update(mousebuttons[2])   
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                client.stop()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouseDown = True
            elif event.type == pygame.MOUSEBUTTONUP:
                mouseDown = False

        if mousebuttons[0]:
            player.shooting = 1
            if lastshot > tickrate/firerate:
                b = Bullet(bulletImg, (player.position.x-9), (player.position.y-9), bulletspeed, -player.angle, own_id)
                bullets.append(b)
                lastshot = 0
        else:
            player.shooting = 0

        for b in bullets:
            if b.x > pygame.display.Info().current_w or b.x <= 0:
                bullets.remove(b)
            elif b.y > pygame.display.Info().current_h or b.y <= 0:
                bullets.remove(b)
        lastshot+=1

        destroyEnemyGroup.draw(screen)
        destroyEnemyGroup.update()
        
        for b in bullets:
            b.moveBullet()
            b.draw(screen)
            
        for p in playerlist:
            if int (p['id']) != own_id: 
                #pygame.draw.rect(screen,green,Rectangle)
                enemyAngle = p['angle']
                rotatedEnemy = pygame.transform.rotate(enemyImg, int(enemyAngle)+90)
                enemyDimensions = rotatedEnemy.get_rect()
                screen.blit(rotatedEnemy, (int(p['position.x']-enemyDimensions.width/2), int(p['position.y']-enemyDimensions.height/2)))
                
                if p['shooting'] == True:
                    #enemy shooting
                    b = Bullet(bulletImg, p['position.x'], p['position.y'], bulletspeed, -enemyAngle, p['id'])
                    bullets.append(b)
                p['shooting'] = False
                pygame.draw.rect(screen,red,(int(p['position.x'])-width/2+7,int(p['position.y'])+25,int(p['health'])/2,10))
                pygame.draw.rect(screen, white,(int(p['position.x'])-width/2+7,int(p['position.y'])+25,50,10),1)
            
            else :
                pygame.draw.rect(screen,red,(int(player.position.x)-width/2+7,int(player.position.y)+25,int(p['health'])/2,5))
                pygame.draw.rect(screen, white,(int(player.position.x)-width/2+7,int(player.position.y)+25,50,5),1)
            
            Rectangle = pygame.Rect(int(p['position.x'])-width/2,int(p['position.y'])-height/2,width,height)
            for b in bullets:
                    if b.rect.colliderect(Rectangle) and b.owner!=int(p['id']):
                        destroyEnemy = DestroyEnemy(b.x,b.y)
                        destroyEnemyGroup.add(destroyEnemy)
                        bullets.remove(b)

        encoded_position = gamepackets.playerstate_pack(player)
        packet = Packet()
        packet.type = gamepackets.PLAYER_STATE
        packet.setPayload(encoded_position)
        client.send(packet)

        clock.tick(tickrate)
        pygame.display.flip()
        print(clock.get_fps())

pygame.quit()