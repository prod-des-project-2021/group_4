import socket
import threading
import time
from collections import deque

from .packet2 import Packet

class Client:

    #######################
    # Initializing client #
    #######################
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.running = True
        self.bufferSize = 1024

        self.inputBuffer = deque()
        self.outputBuffer = deque()

        self.seqIn  = 0
        self.seqOut = 0

        # event hooks
        self.onReceive = None

        self.send_time = time.perf_counter()
        self.receive_time = time.perf_counter()

        self.socket_lock = threading.Lock()

        # init the socket
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.socket.sendto(Packet().encode(), (self.ip, self.port))
        except socket.error:
            print("Unable to start connection")
            self.running = False

        # init threads
        self.receiverThread = threading.Thread(target=self.receiver)
        self.senderThread = threading.Thread(target=self.sender)
        self.processorThread = threading.Thread(target=self.processor)
    #############
    # Interface #
    #############

    # starting up the client
    def start(self):
        self.receiverThread.start()
        self.senderThread.start()
        #self.processorThread.start()

    def stop(self):
        self.running = False
        self.receiverThread.join()
        self.senderThread.join()

    def send(self, packet):
        packet.seq = self.seqOut
        self.seqOut = self.seqOut + 1
        self.outputBuffer.append(packet.encode())

    ####################
    # Receiving thread #
    ####################
    def receiver(self):
        while(self.running):
            #time.sleep(0.01)
            try:
                raw = self.socket.recvfrom(self.bufferSize)
                self.receive_time = time.perf_counter()

                packet = Packet()
                packet.decode(raw[0])

                #self.inputBuffer.append(packet)
                self.onReceive(self, packet)
            except socket.error:
                print("Server closed the connection, probably...")
                self.running = False

    ##################
    # Sending thread #
    ##################
    def sender(self):
        while(self.running):
            time.sleep(0.02)

            while self.outputBuffer:
                self.send_time = time.perf_counter()
                packet = self.outputBuffer.popleft()
                self.socket.sendto(packet, (self.ip, self.port))

            # if we haven't sent anything in a while, send a ping packet
            if(not self.outputBuffer and self.send_time + 0.2 < time.perf_counter()):
                ping = Packet()
                ping.type = 4
                self.send(ping)

    #####################
    # Processing thread #
    #####################
    def processor(self):
        while(self.running):
            #time.sleep(0.005)
            while self.inputBuffer:
                packet = self.inputBuffer.popleft()
                self.onReceive(self, packet)
