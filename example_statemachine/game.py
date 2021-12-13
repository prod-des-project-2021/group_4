from statemachine import State
from gameobjects import GameObject
from gameobjects import TextObject
from gameobjects import Player
from gameobjects import Bullet
from gameobjects import Explosion
from gameobjects import ParticleEmitter, Particle
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

        # game state variables
        #self.player = Player()
        #self.enemies = Enemies()
        #self.bullets = list()
        #self.effects = list()
        #self.particle_emitters = list()
        pygame.init()
        pygame.font.init()
        self.screen = pygame.display.set_mode((1600,900))
        self.clock  = pygame.time.Clock()
        self.running = True
        self.tickrate = 120

        # loading resources
        self.playerSprite = pygame.image.load('res/player.png')
        self.enemySprite = pygame.image.load('res/enemy.png')
        self.bulletSprite = pygame.image.load('res/ammo_small.png')
        self.enginetrailSprite = pygame.image.load('res/engine_trail_particle.png')

        self.e1 = pygame.image.load('res/e1.png')
        self.e2 = pygame.image.load('res/e2.png')
        self.e3 = pygame.image.load('res/e3.png')
        self.e4 = pygame.image.load('res/e4.png')
        self.e5 = pygame.image.load('res/e5.png')
        self.e6 = pygame.image.load('res/e6.png')

        # player object
        self.player = Player(self.playerSprite, self.enginetrailSprite)
        self.player.setAngleOffset(-90)
        self.player.setPosition(300,300)
        self.player.setNickname(nick)

        self.enemies = list()
        enemy = Player(self.enemySprite, self.enginetrailSprite)
        enemy.setPosition(300,300)
        self.enemies.append(enemy)
        self.enemy_st = time.time()

        self.bullets = list()
        self.explosions = list()

    # main game loop
    def start(self):
        while(self.running):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            self.update()
            self.draw()
            self.clock.tick(self.tickrate)

    def update(self):

        if(self.enemy_st < time.time()):
            enemy = Player(self.enemySprite, self.enginetrailSprite)
            enemy.setPosition(random.randint(50,1550), random.randint(50,850))
            self.enemies.append(enemy)
            self.enemy_st = time.time()+4

        # players input
        mouse_x, mouse_y = pygame.mouse.get_pos()
        player_angle = math.atan2(mouse_x - self.player.position.x, mouse_y - self.player.position.y)
        self.player.setAngle(math.degrees(player_angle))

        mouse_x, mouse_y = pygame.mouse.get_pos()
        mousebuttons = pygame.mouse.get_pressed()

        self.player.setState(mousebuttons[0], mousebuttons[2])
        self.player.update()


        if(mousebuttons[0]):
            if(self.player.reloadTime == 0):
                bullet = Bullet(self.bulletSprite)
                bullet.setAngleOffset(-90)
                bullet.copyAngle(self.player)
                point = self.player.getAttachmentPoint(5,12)
                bullet.setPosition(point.x, point.y)
                self.bullets.append(bullet)

                bullet = Bullet(self.bulletSprite)
                bullet.setAngleOffset(-90)
                bullet.copyAngle(self.player)
                point = self.player.getAttachmentPoint(5,-12)
                bullet.setPosition(point.x, point.y)
                self.bullets.append(bullet)
                self.player.reloadTime = self.player.reload

        for bullet in self.bullets:
            bullet.update()

            for enemy in self.enemies:
                if(bullet.colliding(enemy, "circle")):
                    enemy.damage()
                    self.explosions.append(Explosion(bullet.position.x, bullet.position.y, [self.e1, self.e2, self.e3, self.e4, self.e5, self.e6]))
                    self.bullets.remove(bullet)

        for enemy in self.enemies:
            enemy.update()
            if(enemy.alive == False):
                self.explosions.append(Explosion(enemy.position.x, enemy.position.y, [self.e1, self.e2, self.e3, self.e4, self.e5, self.e6], big = True))
                self.enemies.remove(enemy)

        for explosion in self.explosions:
            explosion.update()
            if explosion.active == False:
                self.explosions.remove(explosion)



    def draw(self):
        self.screen.fill(pygame.Color("black"))
        self.player.draw(self.screen)

        for enemy in self.enemies:
            enemy.draw(self.screen)

        for bullet in self.bullets:
            bullet.draw(self.screen)

        for explosion in self.explosions:
            explosion.draw(self.screen)

        pygame.display.flip()
