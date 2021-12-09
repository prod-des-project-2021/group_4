import struct

from pygame.math import Vector2
from networking import Service
from networking import Packet
from pygame.math import Vector2
import pygame
import struct
import gamepackets
from gamemonitor import GameMonitor

NORMAL_VECTOR = Vector2(0, 1)

def isColliding(obj1, obj2):
    # obj1 and obj2 must have position Vector2 and w and h values
    return (obj1.position.x < obj2.position.x + obj2.w and
            obj1.position.x + obj1.w > obj2.position.x and
            obj1.position.y < obj2.position.y + obj2.h and
            obj1.h + obj1.position.y > obj2.position.y)

class GameServer:
    def __init__(self):
        self.running = True
        self.max_players = 4
        self.players = list()
        self.bullets = list()

    def update(self):
        for player in self.players:

            #collision detection
            for bullet in self.bullets:
                if isColliding(bullet, player) and player.id != bullet.player.id:
                    player.health = player.health - bullet.damage
                    self.bullets.remove(bullet)

            player.update()

        for bullet in self.bullets:
            if(bullet.outOfBounds()):
                self.bullets.remove(bullet)

            bullet.update()

    def sendState(self, service):
        if self.players:
            for player in self.players:
                gamestate = gamepackets.gamestate_pack(self.players, player.id)
                packet = Packet()
                packet.type = gamepackets.GAME_STATE
                packet.setPayload(gamestate)
                player.client.send(packet)

    def onServerExit(self):
        self.running = False

    def onTimeout(self, server, client_id):
        print(str(client_id)+" has timed out")
        for player in self.players:
            if player.id == client_id:
                self.players.remove(player)
                break

    def onConnect(self, server, client):
        print(str(client.id)+" has connected!")
        self.players.append(Player(client.id, client, self))

    def onReceive(self, server, client, packet):
        # receiving state from player
        if(packet.type == gamepackets.PLAYER_STATE):
            data = gamepackets.playerstate_unpack(packet.payload)

            # updating the players state
            for player in self.players:
                if player.id == client.id:
                    player.updateState(data)

    # game mechanics
    def addBullet(self, player):
        self.bullets.append(Bullet(player))


class Player:
    def __init__(self, id, client, gameserver):
        self.gameserver = gameserver
        self.id =       id
        self.position = Vector2(0,0)
        self.velocity = Vector2(0,0)
        self.direction = Vector2(0,1)
        self.angle =    0.0
        self.health =   100
        self.accelerating = False
        self.shooting = False
        self.reloadTime = 0
        self.alive = True

        self.w = 30
        self.h = 30

        self.client = client # adding handle to client so we can SEND

    def updateState(self, data):
        self.position.x = data["position.x"]
        self.position.y = data["position.y"]

        self.angle = data['angle']
        self.direction = Vector2(NORMAL_VECTOR)
        self.direction.rotate_ip(-self.angle)

        self.velocity.x = data['velocity.x']
        self.velocity.y = data['velocity.y']
        self.accelerating = data['accelerating']
        self.shooting = data['shooting']


    def update(self):
        if self.reloadTime > 0:
            self.reloadTime -= 1

        if self.health <= 0:
            self.alive = False 

        if self.reloadTime == 0 and self.shooting:
            self.gameserver.addBullet(self)
            self.reloadTime = 60

class Bullet:
    # player = owner of the bullet
    def __init__(self, player):
        self.player =       player
        self.position =     player.position

        self.direction =    player.direction
        self.damage =       10
        self.velocity =     8

        self.w = 8
        self.h = 8

    def update(self):
        # move the bullet
        self.position = self.position + self.direction * self.velocity

    def outOfBounds(self):
        return (self.position.x < 0 or self.position.x > 1920 or self.position.y < 0 or self.position.y > 1080)

def gamemonitor(players, bullets):
    gm = GameMonitor(players, bullets)

def tests():
    print("test")

def main():
    server = Service("127.0.0.1", 5555)
    gameserver = GameServer()

    # hooking the vents
    server.onTimeout = gameserver.onTimeout
    server.onConnect = gameserver.onConnect
    server.onReceive = gameserver.onReceive
    server.onServerExit = gameserver.onServerExit

    # adding own commands to the server io
    server.addCommand("monitor", gamemonitor, args=(gameserver.players, gameserver.bullets))
    server.addCommand("test", tests)

    server.start()
    clock = pygame.time.Clock()

    while(gameserver.running):
        clock.tick(120)
        gameserver.update()
        gameserver.sendState(server)

if __name__ == '__main__':
    main()
