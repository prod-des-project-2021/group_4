#from .connectionListener import ConnectionListener
import socket
import threading
import time
import pprint

from .clienthandler import ClientHandler
from .packet import Packet

class Service(threading.Thread):
    def __init__(self, addr, port):
        super().__init__()
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
        self.onTimeout    = None
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

    def run(self):
        while(self.running):
            try:
                packet = self.socket.recvfrom(self.bufferSize)
                packet_addr = packet[1][0]
                packet_port = packet[1][1]
                packet_payload = packet[0]

                # deliver the packet to the clientHandler
                # spawn a new thread so we are instantly ready to receive something again
                dispatchPacket = threading.Thread(target = self.processPacket, args = (packet_addr, packet_port, packet_payload))
                dispatchPacket.start()

            except socket.error:
                pass
                #self.running = False

    def stop(self):
        self.running = False
        self.breakOutSocket()

    def tick(self):
        clock = time.perf_counter() * self.tickRate
        sleep = int(clock) + 1 - clock
        time.sleep(sleep/self.tickRate)


    def processPacket(self, addr, port, payload):

        # checking if the packet is for an existing client
        existingClient = False
        for client in self.clients:
            if client.addr == addr and client.port == port:

                # handle the decoding here so rest of the code
                # can use just Packet objects
                packet = Packet()
                packet.decode(payload)

                # add the packet to clients input buffer
                client.addToInputBuffer(packet)
                existingClient = True
                break

        # if not, spawn a new client
        if existingClient == False:

            # creating a new instance of ClientHandler
            # and pass the incoming packet to it to handle
            newClient = ClientHandler(self, addr, port)
            packet = Packet()
            packet.decode(payload)
            newClient.addToInputBuffer(packet)
            self.clients.append(newClient)

    def io(self):
        while(self.running):
            command = input(">>")
            if command == "exit":
                self.running = False
                print("Stopping the server")
                self.breakOutSocket()
            elif command == "monitor":
                print("Starting server monitor")
            else:
                print("Command not found")

    def breakOutSocket(self):
        # send a dummy packet to close the socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.sendto(Packet().encode(), (self.addr, self.port))
