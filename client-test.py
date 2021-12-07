from networking import Client
from networking import Packet
import gamepackets
from pygame.math import Vector2
import time
import random

import struct

position = Vector2(150.0, 150.0)

def onReceive(client, packet):
    if(packet.type == 51):
        global position
        print(str(gamepackets.gamestate_unpack(packet.payload)))

class Player:
    def __init__(self):
        self.id =       0
        self.position = Vector2(0,0)
        self.velocity = Vector2(0,0)
        self.angle =    0.0
        self.health =   100
        self.accelerating = False
        self.shooting = False

def main():
    global position

    client = Client("127.0.0.1", 5555)
    client.onReceive = onReceive
    client.start()

    player = Player()

    while(True):
        time.sleep(0.01)
        player.position.x = player.position.x + 0.1
        player.position.y = player.position.y + 0.1
        print(player.position.x)
        packet = Packet()
        packet.type = gamepackets.PLAYER_STATE
        packet.setPayload(gamepackets.playerstate_pack(player))
        client.send(packet)

if __name__ == '__main__':
    main()
