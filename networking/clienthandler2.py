from queue import Queue
import time
import struct
import threading
from .packet2 import Packet

class ClientHandler:
    ##############################
    # Initializing ClientHandler #
    ##############################
    def __init__(self, service, addr):
        self.inputBuffer = Queue()
        self.outputBuffer = Queue()
        self.ackBuffer = list()

        self.service = service # handle to server

        self.addr       = addr # tuple(ip, port)
        self.seqIn      = 0
        self.seqOut     = 0
        self.timeout    = 0 # when last packet was received
        self.id         = service.generateClientId() # each client must have unique id

        # useful numbers
        self.received_packets = 0
        self.sent_packets = 0
        self.received_data = 0
        self.sent_data = 0

        self.packets_in_per_sec = 0
        self.packets_out_per_sec = 0
        self.data_per_sec = 0
        self.data_per_sec_out = 0

        self.last_process = time.perf_counter()

    ###########################################
    # Sending packets to the client(global)   #
    # It adds the packet(valid Packet class)  #
    # to clients outputBuffer                 #
    ###########################################
    def send(self, packet):
        self.sent_packets += 1
        self.sent_data += packet.size

        packet.seq = self.seqOut
        self.seqOut = self.seqOut + 1
        self.outputBuffer.put(packet)


    #######################################
    # Incoming packets from client        #
    # Each packet has to be passed in raw #
    # form through this function          #
    #######################################
    def receive(self, raw): # Receiving raw data, must be decoded
        self.received_packets += 1
        self.received_data += len(raw)

        # setting the time when packet is received
        self.timeout = time.perf_counter()

        # decoding the packet
        packet = Packet()
        valid = packet.decode(raw)

        # if packet is invalid, just drop it
        if(not valid):
            return

        # checking if packet is older than last received
        # if it is and there is no priority, just drop it
        if(packet.seq <= self.seqIn and packet.priority == 0):
            return

        # ping packet
        if(packet.type == 4):
            response = Packet()
            response.type = 5 # PONG
            self.send(response)
            return

        # packet types over 10 are user controlled
        # so here we pass the control back to user
        if(packet.type > 10):
            # if everything is ok, push the packet to input queue
            self.seqIn = packet.seq
            self.inputBuffer.put(packet)


    ###########################################
    # Processing buffers                      #
    # This function is called from main       #
    # server thread and it handles processing #
    # input and ack messages                  #
    # It also informs the server about timeouts
    # with return value(False = timeout)      #
    ###########################################
    def process(self):
        self.calculateStatistics()

        while not self.inputBuffer.empty():
            packet = self.inputBuffer.get()

            # sending the packet to main control
            self.service.onReceive(self.service, self, packet)

        # if client has timed out, return false
        # and give control to the main thread
        if(time.perf_counter() > self.timeout + 3.0):
            return False

        return True

    ####################
    # Helper functions #
    ####################

    def calculateStatistics(self):
        # processing the numbers
        if(time.perf_counter() > self.last_process + 1.0):
            self.data_per_sec = self.received_data
            self.data_per_sec_out = self.sent_data
            self.packets_out_per_sec = self.sent_packets
            self.packets_in_per_sec = self.received_packets

            self.sent_data = 0
            self.received_data = 0
            self.sent_packets = 0
            self.received_packets = 0

            self.last_process = time.perf_counter()
