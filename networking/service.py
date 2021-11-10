#from .connectionListener import ConnectionListener
import socket
import threading

from .clienthandler import ClientHandler

class Service:
    def __init__(self, addr, port):
        self.running = True
        self.addr = addr
        self.port = port
        self.bufferSize = 1024
        self.socket = None

        self.clients = list()

        # server settings
        self.tickRate = 30
        self.maxClients = 16

        # server events
        self.onConnect    = None
        self.onDisconnect = None
        self.onTimeOut    = None
        self.onReconnect  = None
        self.onReceive    = None

        # initializing the UDP socket
        self.initSocket()

        # starting up the IO thread for server commands
        ioThread = threading.Thread(target=self.io)
        ioThread.start()

    def initSocket(self):
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.socket.bind((self.addr, self.port))
        except socket.error:
            print("Could not bind socket on "+str(self.addr)+":"+str(self.port))
            self.running = False

    def start(self):
        while(self.running):
            try:
                packet = self.socket.recvfrom(self.bufferSize)
                packet_addr = packet[1][0]
                packet_port = packet[1][1]
                packet_payload = packet[0]

                # deliver the packet to the clientHandler
                self.processPacket(packet_addr, packet_port, packet_payload)

            except socket.error:
                print("Socket encountered an error!")
                self.running = False

    def processPacket(self, addr, port, payload):
        self.onReceive(self, addr, payload)
        # checking if the packet is for an existing client
        #existingClient = False
        #for client in self.clients:
            #if client.addr == addr and client.port == port:
                #client.addToInputBuffer(payload)
                #existingClient = True
                #break

        # if not, spawn a new client
        #if existingClient == False:
            #pass # spawn the client



    def io(self):
        while(self.running):
            command = input(">>")
            if command == "exit":
                self.running = False
                print("Stopping the server")
                self.breakOutSocket()
            else:
                print("Command not found")

    def breakOutSocket(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.sendto(bytes("0000", "utf-8"), (self.addr, self.port))
