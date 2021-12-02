# ################################################################ #
# The server main class                                            #
# ################################################################ #

import socket
import threading
import time
import random
import pprint

from queue import Queue
from .packet2 import Packet
from .clienthandler2 import ClientHandler

class Service:
    def __init__(self, addr, port):
        # service variables
        self.running = False
        self.socket = None
        self.addr = addr
        self.port = port
        self.bufferSize = 1024

        # buffer for input packets
        self.inputBuffer = Queue()

        # client list
        self.clients = list()
        self.counter = 0

        # server event hooks
        self.onConnect      = None
        self.onReceive      = None
        self.onTimeout      = None
        self.onServerExit   = None

        # server threads
        self.ioThread        = threading.Thread(target=self.io)
        self.receiverThread  = threading.Thread(target=self.receiver)
        self.senderThread    = threading.Thread(target=self.sender)
        self.processorThread = threading.Thread(target=self.processor)

    # socket initialization
    def initSocket(self):
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            ##self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 21024)
            self.socket.bind((self.addr, self.port))
        except socket.error:
            print("Unable to bind socket!")
            self.running = False

    # server startup
    def start(self):
        print("Starting up the server...")
        self.running = True

        # initializing the socket
        self.initSocket()

        # starting up the threads
        if self.running:
            self.ioThread.start()
            self.receiverThread.start()
            self.senderThread.start()
            self.processorThread.start()

            print("Server started succesfully on: "+str(self.addr)+":"+str(self.port))

    # server stopping
    def stop(self):
        self.running = False
        self.breakOutSocket()
        self.socket.close()

        self.receiverThread.join()
        self.senderThread.join()
        self.processorThread.join()

        self.onServerExit()

    ###################
    # SERVICE THREADS #
    ###################

    # Command thread
    def io(self):
        while(self.running):
            time.sleep(0.2)

            command = input()
            if command == "exit":
                print("Stopping the server")
                self.stop()

            elif command == "clients":
                if(len(self.clients) == 0):
                    print("No clients connected")
                else:
                    for client in self.clients:
                        print("==== Client(id: "+str(client.id)+", addr: "+str(client.addr)+") ====")
                        print("Data in: "+str(client.data_per_sec/1000)+" KB/s, Packets out: "+str(client.packets_out_per_sec)+"/s, Packets in: "+str(client.packets_in_per_sec)+"/s")

            elif command == "stat":
                print("Received "+str(self.counter)+" packets")
            else:
                print("Unknown command")

    # Receiving thread
    def receiver(self):
        while(self.running):
            try:
                packet = self.socket.recvfrom(self.bufferSize)
                self.inputBuffer.put(packet)
            except socket.error as error:
                pass # BECAUSE WE DON*T WANT TO CRASH
                #print("Server socket encountered an error")
                #print(str(error))
                #self.running = False

    # Sending thread
    def sender(self):
        while(self.running):
            time.sleep(0.02)
            # processing the outputBuffer
            for client in self.clients:
                while not client.outputBuffer.empty():
                    packet = client.outputBuffer.get()
                    self.socket.sendto(packet.encode(), client.addr)

    # Process clients
    def processor(self):
        while(self.running):
            time.sleep(0.01)
            # sending all packets to clients
            self.forwardPackets()

            # processing all the clients
            for client in self.clients:
                if(not client.process()):
                    # timeout handling
                    # sending an event to main control
                    self.onTimeout(self, client.id)

                    # remove client
                    self.clients.remove(client)

    # Goes through the inputBuffer
    # and sent the packets to the clients
    # they belong to
    def forwardPackets(self):

        while not self.inputBuffer.empty():

            rawPacket = self.inputBuffer.get()
            rawPayload = rawPacket[0]
            rawAddr    = rawPacket[1]

            # checking if we have already
            # received data from the client
            existingClient = False
            for client in self.clients:
                if(client.addr == rawAddr):
                    client.receive(rawPayload)
                    existingClient = True
                    break

            # if client is new, add a new
            # handler to the clients list
            if(existingClient == False):

                client = ClientHandler(self, rawAddr)
                client.receive(rawPayload)
                self.clients.append(client)

                # sending an event to main control
                self.onConnect(self, client)



    ####################
    # HELPER FUNCTIONS #
    ####################

    def breakOutSocket(self):
        packet = Packet()
        packet.setPayload(bytes("bye", "utf-8"))

        self.socket.sendto(packet.encode(), (self.addr, self.port))
        print("Socket closed")


    def generateClientId(self):
        # ihanata purkkaa
        reserved = False
        while(True):
            id = random.randint(10000,65536)

            for client in self.clients:
                if client.id == id:
                    reserved = True
                    break

            if(reserved == False):
                break

        return id
