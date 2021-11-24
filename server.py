from networking import Service

def onTimeout(server, client_id):
    print(str(client_id)+" has timed out")

def onConnect(server, client):
    print(str(client.id)+" has connected!")

def onReceive(server, client, packet):
    pass #print("Packet from "+str(client.id)+": "+str(packet.seq))

def main():
    server = Service("127.0.0.1", 5555)
    server.onTimeout = onTimeout
    server.onConnect = onConnect
    server.onReceive = onReceive
    server.start()

if __name__ == '__main__':
    main()
