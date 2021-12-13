from statemachine import State
from gameobjects import GameObject
from gameobjects import TextObject
from gameobjects import Player
from gameobjects import Bullet
from gameobjects import Explosion
from gameobjects import ParticleEmitter, Particle
from networking import Client
from networking import Packet
import gamepackets
import pygame
import math
import time
import random

class Game(State):
    def __init__(self, stateMachine):
        super().__init__(stateMachine)

    def initialize(self, nick, ip):
        # main menu vars
        self.nick   = nick
        self.ip     = ip

        # initialize pygame
        pygame.init()
        pygame.font.init()
        pygame.mixer.init()
        self.screen = pygame.display.set_mode((1600,900))
        pygame.display.set_caption("Multiplayer Game")
        self.clock  = pygame.time.Clock()
        self.running = True
        self.tickrate = 120

        # loading resources
        self.playerSprite = pygame.image.load('res/player.png')
        self.enemySprite = pygame.image.load('res/enemy.png')
        self.bulletSprite = pygame.image.load('res/ammo_small.png')
        self.enginetrailSprite = pygame.image.load('res/engine_trail_particle.png')
        self.background = pygame.image.load("space.jpg")
        self.background = pygame.transform.scale(self.background, (1600,900))

        self.explosion_small = pygame.mixer.Sound("sfx/explosion_small.ogg")
        self.explosion_big = pygame.mixer.Sound("sfx/explosion_big.ogg")
        self.laser = pygame.mixer.Sound("sfx/laser.ogg")
        self.engine = pygame.mixer.Sound("sfx/engine.ogg")


        self.e1 = pygame.image.load('res/e1.png')
        self.e2 = pygame.image.load('res/e2.png')
        self.e3 = pygame.image.load('res/e3.png')
        self.e4 = pygame.image.load('res/e4.png')
        self.e5 = pygame.image.load('res/e5.png')
        self.e6 = pygame.image.load('res/e6.png')

        # player object
        self.player = Player(self.playerSprite, self.enginetrailSprite)
        self.player.setAngleOffset(-90)
        self.player.setNickname(nick)

        self.playerlist = dict()
        self.own_id = 0
        self.enemies = list()

        self.bullets = list()
        self.explosions = list()

        # initialize networking client
        self.client = Client(self.ip, 5555)
        self.client.onReceive = self.onReceive
        self.client.start()

    def onReceive(self, client, packet):
        if packet.type == gamepackets.GAME_STATE:
            self.player.id, self.playerlist = gamepackets.gamestate_unpack(packet.payload)

    # main game loop
    def start(self):
        while(self.running):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    self.client.stop()

            self.update()
            self.draw()
            self.clock.tick(self.tickrate)

    def update(self):

        # players input
        mouse_x, mouse_y = pygame.mouse.get_pos()
        player_angle = math.atan2(mouse_x - self.player.position.x, mouse_y - self.player.position.y)
        self.player.setAngle(math.degrees(player_angle))

        mouse_x, mouse_y = pygame.mouse.get_pos()
        mousebuttons = pygame.mouse.get_pressed()

        # if alive, allow state updates
        if self.player.alive:
            self.player.setState(mousebuttons[0], mousebuttons[2])
        else:
            # exploding the player upon death only once
            if self.player.exploded == False:
                self.explosion_big.play()
                self.explosions.append(Explosion(self.player.position.x, self.player.position.y, [self.e1, self.e2, self.e3, self.e4, self.e5, self.e6], big = True))
                self.player.exploded = True

        self.player.update()

        if(mousebuttons[0] and self.player.alive):
            if(self.player.reloadTime == 0):
                self.laser.play()
                bullet = Bullet(self.bulletSprite)
                bullet.owner = self.player.id
                bullet.setAngleOffset(-90)
                bullet.copyAngle(self.player)
                point = self.player.getAttachmentPoint(5,0)
                bullet.setPosition(point.x, point.y)
                self.bullets.append(bullet)

                self.player.reloadTime = self.player.reload



        for bullet in self.bullets:
            bullet.update()

            for enemy in self.enemies:
                if(bullet.colliding(enemy, "rect") and bullet.owner != enemy.id):
                    self.explosion_small.play()
                    self.explosions.append(Explosion(bullet.position.x, bullet.position.y, [self.e1, self.e2, self.e3, self.e4, self.e5, self.e6]))
                    self.bullets.remove(bullet)

            if(bullet.colliding(self.player, "rect") and bullet.owner != self.player.id and self.player.alive):
                self.explosion_small.play()
                self.explosions.append(Explosion(bullet.position.x, bullet.position.y, [self.e1, self.e2, self.e3, self.e4, self.e5, self.e6]))
                self.bullets.remove(bullet)

        # updating local enemies
        for enemy in self.enemies:
            enemy.update()

            if(enemy.shooting and enemy.reloadTime == 0):
                self.laser.play()
                bullet = Bullet(self.bulletSprite)
                bullet.owner = enemy.id
                bullet.setAngleOffset(-90)
                bullet.copyAngle(enemy)
                point = enemy.getAttachmentPoint(5,0)
                bullet.setPosition(point.x, point.y)
                self.bullets.append(bullet)
                enemy.reloadTime = enemy.reload

            if(not int(enemy.alive)):
                self.explosion_big.play()
                self.explosions.append(Explosion(enemy.position.x, enemy.position.y, [self.e1, self.e2, self.e3, self.e4, self.e5, self.e6], big = True))
                self.enemies.remove(enemy)

        # updating explosions
        for explosion in self.explosions:
            explosion.update()
            if explosion.active == False:
                self.explosions.remove(explosion)

        # looping the player list from server
        for p in self.playerlist:

            # map players own state from server
            if p['id'] == self.player.id:
                self.player.mapOwnState(p)

            # check if were dealing with existing enemy
            existing = False
            for enemy in self.enemies:
                if enemy.id == p['id'] and p['id'] != self.player.id:
                    enemy.mapState(p)
                    existing = True
                    break

            # if we get a new enemy id
            # append it to local enemies list
            if(existing == False and p['id'] != self.player.id and int(p['alive'])):
                enemy = Player(self.enemySprite, self.enginetrailSprite)
                enemy.setAngleOffset(90)
                enemy.id = p['id']
                enemy.mapState(p)
                self.enemies.append(enemy)

        # sending player state to server
        packet = Packet()
        packet.type = gamepackets.PLAYER_STATE
        packet.setPayload(gamepackets.playerstate_pack(self.player))
        self.client.send(packet)


    def draw(self):
        self.screen.fill(pygame.Color("black"))
        self.screen.blit(self.background,(0,0))
        self.player.draw(self.screen)

        for enemy in self.enemies:
            enemy.draw(self.screen)

        for bullet in self.bullets:
            bullet.draw(self.screen)

        for explosion in self.explosions:
            explosion.draw(self.screen)

        pygame.display.flip()
