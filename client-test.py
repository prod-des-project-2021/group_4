from networking import Client
from networking import Packet
import time
import random

def onReceive(client, packet):
    if(packet.type == 5):
        print("PONG "+str(packet.seq))    

def main():
    client = Client("127.0.0.1", 5555)
    client.onReceive = onReceive
    client.start()

if __name__ == '__main__':
    main()
