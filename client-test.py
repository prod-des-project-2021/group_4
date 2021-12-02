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

def main():
    global position

    client = Client("127.0.0.1", 5555)
    client.onReceive = onReceive
    client.start()

    while(True):
        time.sleep(0.02)
        position.x = position.x + 0.01
        position.y = position.y + 0.01

if __name__ == '__main__':
    main()
