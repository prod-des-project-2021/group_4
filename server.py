import struct

from pygame.math import Vector2
from networking import Service

position = Vector2(0, 0)


def onTimeout(server, client_id):
    print(str(client_id)+" has timed out")

def onConnect(server, client):
    print(str(client.id)+" has connected!")

def onReceive(server, client, packet):
    if packet.type == 11:
        decoded_position = struct.unpack("d d",packet.payload)
        position.x = decoded_position[0]
        position.y = decoded_position[1]
        
        #print(str(position.x)+" "+str(position.y))
    #print("Packet from "+str(client.id)+": "+str(packet.seq))

def main():
    server = Service("127.0.0.1", 3333)
    server.onTimeout = onTimeout
    server.onConnect = onConnect
    server.onReceive = onReceive
    server.start()

if __name__ == '__main__':
    main()
