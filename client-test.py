from networking import Client
from networking import Packet
from pygame.math import Vector2
import time
import random

import struct

position = Vector2(150.0, 150.0)
def onReceive(client, packet):
    if(packet.type == 5):
        global position
        print("PONG "+str(packet.seq))

        packet = Packet()
        packet.type = 11
        encoded_position = struct.pack("d d", position.x, position.y)
        packet.setPayload(encoded_position)
        client.send(packet)

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
