from queue import Queue
import time
import struct
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


    ###########################################
    # Sending packets to the client(global)   #
    # It adds the packet(valid Packet class)  #
    # to clients outputBuffer                 #
    ###########################################
    def send(self, packet):
        packet.seq = self.seqOut
        self.seqOut = self.seqOut + 1
        self.outputBuffer.put(packet)

    #######################################
    # Incoming packets from client        #
    # Each packet has to be passed in raw #
    # form through this function          #
    #######################################
    def receive(self, raw): # Receiving raw data, must be decoded

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

        # if packet needs to be acked
        if(packet.priority == 1):
            response = Packet()
            response.type = 3
            response.setPayload(struct.pack("i", packet.seq))
            self.ackBuffer.append(response)

        # acked packet, handle it here
        if(packet.type == 3):
            ack_number = struct.unpack("i", packet.payload)
            for ack in self.ackBuffer:
                pass # do something here
            return

        # ping packet
        if(packet.type == 4):
            response = Packet()
            response.type = 5 # PONG
            self.send(response)
            return

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
        while not self.inputBuffer.empty():
            packet = self.inputBuffer.get()
            print(packet.seq)
        # if client has timed out, return false
        # and give control to the main thread
        if(time.perf_counter() > self.timeout + 5.0):
            return False

        return True
