# ################################################################ #
# The server main class                                            #
# ################################################################ #

import socket
import threading
import time
from queue import Queue
from .packet import Packet

class Service:
    def __init__(self, addr, port):
        # service variables
        self.running = False
        self.socket = None
        self.addr = addr
        self.port = port
        self.bufferSize = 8192

        # buffer for outgoing packets
        self.outputBuffer = Queue()

        # buffer for input packets
        self.inputBuffer = Queue()

        # client list
        self.clients = list()
        self.counter = 0
        # server event hooks
        self.onConnect      = None
        self.onReceive      = None
        self.onTimeout      = None
        self.onDisconnect   = None
        self.onReconnect    = None

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

    ###################
    # SERVICE THREADS #
    ###################

    # Command thread
    def io(self):
        while(self.running):
            time.sleep(0.05)

            command = input()
            if command == "exit":
                print("Stopping the server")
                self.stop()
            elif command == "test1":
                n = int(input("Number of test packets: "))
                start = time.time()* 1000
                for i in range(0,n):
                    self.testPacket()
                    #time.sleep(0.01)

                end = time.time()* 1000
                total = end - start
                print(str(n)+" packets sent in "+str(total)+"ms")
            elif command == "stat":
                print("Received "+str(self.counter)+" packets")
            else:
                print("Unknown command")

    # Receiving thread
    def receiver(self):
        counter = 0
        while(self.running):
            try:
                packet = self.socket.recvfrom(self.bufferSize)
                self.inputBuffer.put(packet)
                counter = counter + 1
                print(str(counter))
            except socket.error:
                print("Server socket encountered an error")
                self.running = False

    # Sending thread
    def sender(self):
        while(self.running):
            time.sleep(0.05)
            # processing the outputBuffer
            while not self.outputBuffer.empty():
                packet = self.outputBuffer.get()
                self.socket.sendto(packet.encode(), (packet.addr, packet.port))

    # Process clients
    def processor(self):
        while(self.running):
            time.sleep(0.05)
            # sending all packets to clients
            self.forwardPackets()

            for client in self.clients:
                pass

    # Goes through the inputBuffer
    # and sent the packets to the clients
    # they belong to
    def forwardPackets(self):

        while not self.inputBuffer.empty():
            self.counter = self.counter + 1
            rawPacket = self.inputBuffer.get()
            # extracting packet information
            rawPayload = rawPacket[0]
            rawAddr    = rawPacket[1][0]
            rawPort    = rawPacket[1][1]

            packet = Packet()
            packet.setDestination(rawAddr, rawPort)
            packet.decode(rawPayload)



    ####################
    # HELPER FUNCTIONS #
    ####################
    def testPacket(self):
        packet = Packet()
        packet.setPayload(bytes("hello", "utf-8")*25)
        packet.setSequence(1)
        packet.setType(0)
        self.socket.sendto(packet.encode(), (self.addr, self.port))


    def breakOutSocket(self):
        packet = Packet()
        packet.setPayload(bytes("bye", "utf-8"))
        packet.setSequence(1)
        packet.setType(0)
        self.socket.sendto(packet.encode(), (self.addr, self.port))
        print("Socket closed")
