import struct

from pygame.math import Vector2
from networking import Service
from networking import Packet
from pygame.math import Vector2
import pygame
import struct
import gamepackets

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
            gamestate = gamepackets.gamestate_pack(self.players)
            packet = Packet()
            packet.type = gamepackets.GAME_STATE
            packet.setPayload(gamestate)

            for player in self.players:
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
        print(packet)
        # receiving state from player
        if(packet.type == gamepackets.PLAYER_STATE):
            data = gamepackets.playerstate_unpack(packet.payload)
            print(data)
            # updating the players state
            for player in self.players:
                if player.id == client.id:
                    player.updateState(data)


class Player:
    def __init__(self, id, client):
        self.id =       id
        self.position = Vector2(0,0)
        self.velocity = Vector2(0,0)
        self.angle =    0.0
        self.health =   100
        self.accelerating = False
        self.shooting = False

        self.client = client # adding handle to client so we can SEND

    def updateState(self, data):
        print(data)
        self.position.x = data["position.x"]
        self.position.y = data["position.y"]

    def update(self):
        pass

class Bullet:
    # player = owner of the bullet
    def __init__(self, player):
        self.player =       player
        self.position =     Vector2(0,0)
        self.velocity =     0.5
        self.direction =    Vector2(0,0)
        self.damage =       10

    def update(self):
        pass

def gamemonitor(viesti):
    print("Starting up the monitor..."+viesti)

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
    server.addCommand("monitor", gamemonitor, args=("testArg"))
    server.addCommand("test", tests)

    server.start()
    clock = pygame.time.Clock()

    while(gameserver.running):
        clock.tick(120)
        gameserver.update()
        gameserver.sendState(server)

if __name__ == '__main__':
    main()
