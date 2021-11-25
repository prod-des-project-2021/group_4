import struct
from networking import Service
from pygame.math import Vector2
import pygame
import struct
import gamepackets

class GameServer:
    def __init__(self):
        self.running = True
        self.max_players = 4
        self.players = list()

    def update(self):
        for player in self.players:
            player.update()

    def sendState(self, service):
        pass

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
        self.players.append(Player(client.id))

    def onReceive(self, server, client, packet):

        # receiving state from player
        if(packet.type == PLAYER_STATE):
            data = gamepackets.playerstate_unpack(packet.payload)

            # updating the players state
            for player in self.players:
                if player.id == client.id:
                    player.updateState(data)


class Player:
    def __init__(self, id):
        self.id = id
        self.position = Vector2(0,0)
        self.velocity = Vector2(0,0)
        self.angle = 0.0
        self.health = 100
        self.accelerating = False
        self.shooting = False

    def updateState(self, data):
        self.position.x = data["position.x"]
        self.position.y = data["position.y"]

    def update(self):
        pass


def main():
    server = Service("127.0.0.1", 5555)
    gameserver = GameServer()

    # hooking the vents
    server.onTimeout = gameserver.onTimeout
    server.onConnect = gameserver.onConnect
    server.onReceive = gameserver.onReceive
    server.onServerExit = gameserver.onServerExit

    server.start()
    clock = pygame.time.Clock()

    while(gameserver.running):
        clock.tick(120)
        gameserver.update()
        gameserver.sendState(server)

if __name__ == '__main__':
    main()
