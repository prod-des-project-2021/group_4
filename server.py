import struct

from pygame.math import Vector2
from networking import Service
from networking import Packet
from pygame.math import Vector2
import pygame
import struct
import gamepackets
from gamemonitor import GameMonitor

NORMAL_VECTOR = Vector2(0, -1)

class GameServer:
    def __init__(self):
        self.running = True
        self.max_players = 4
        self.players = list()
        self.bullets = list()

    def update(self):
        for player in self.players:
            player.update()

        for bullet in self.bullets:
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
        self.players.append(Player(client.id, client))

    def onReceive(self, server, client, packet):
        # receiving state from player
        if(packet.type == gamepackets.PLAYER_STATE):
            data = gamepackets.playerstate_unpack(packet.payload)

            # updating the players state
            for player in self.players:
                if player.id == client.id:
                    player.updateState(data)


class Player:
    def __init__(self, id, client):
        self.id =       id
        self.position = Vector2(0,0)
        self.velocity = Vector2(0,0)
        self.direction = Vector(0,1)
        self.angle =    0.0
        self.health =   100
        self.accelerating = False
        self.shooting = False
        self.reloadTime = 0

        self.w = 30
        self.h = 30

        self.client = client # adding handle to client so we can SEND

    def updateState(self, data):
        self.position.x = data["position.x"]
        self.position.y = data["position.y"]

        self.angle = data['angle']
        self.direction = Vector2(NORMAL_VECTOR)
        self.direction.rotate_ip(self.angle)

        self.velocity.x = data['velocity.x']
        self.velocity.y = data['velocity.y']
        self.accelerating = data['accelerating']
        self.shooting = data['shooting']


    def update(self):
        if self.reloadTime > 0:
            self.reloadTime -= 1

        if self.reloadTime == 0 and self.shooting:
            #shoot
            self.reloadTime = 60

class Bullet:
    # player = owner of the bullet
    def __init__(self, player):
        self.player =       player
        self.position =     player.position

        self.direction =    player.direction
        self.damage =       10
        self.velocity =     0.5

        self.w = 8
        self.h = 8

    def update(self):
        # move the bullet
        self.position + self.direction * self.velocity

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
