from networking import Service
from networking import Packet

def onConnect(client, packet):
    print("New client has connected")

def onDisconnect(server, client):
    pass

def onTimeout(server, client):
    pass

def onReconnect(server, client):
    pass

def onStop(server, clients):
    pass

def onReceive(server, client, packet):
    print(packet.seq)

def main():
    print("Starting the server...")

    server = Service("127.0.0.1", 5555)
    server.tickRate = 60
    server.maxClients = 8

    # event handlers for networking events
    server.onConnect      = onConnect
    server.onDisconnect   = onDisconnect
    server.onTimeout      = onTimeout
    server.onReconnect    = onReconnect
    server.onReceive      = onReceive

    server.start()

    while(server.running):


        # tickrate limiter
        server.tick()

    server.stop()

if __name__ == '__main__':
    main()
