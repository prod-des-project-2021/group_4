from networking import Service

def onConnect(server, client, packet):
    pass

def onDisconnect(server, client):
    pass

def onTimeout(server, client):
    pass

def onReconnect(server, client):
    pass

def onReceive(server, client, packet):
    print(packet)

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
        pass # do the game simulation

if __name__ == '__main__':
    main()
