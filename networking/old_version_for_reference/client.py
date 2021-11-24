# ################################################################ #
# This class is used to handle all the client side communications  #
# ################################################################ #

import threading
import time
import socket

from .packet import Packet

class Client:
    def __init__(self, addr, port):
        self.running = True
        self.socket = None
        self.addr = addr
        self.port = port

        self.inputBuffer = list()
        self.outputBuffer = list()

        self.seqIn = 0
        self.seqOut = 0
        self.packetTime = 0

        # events
        self.onReceive = None
        self.onTimeout = None
        self.onDisconnect = None

        # initializing the socket
        self.initSocket()

        # initializing communication threads
        self.clientSender = ClientSender(self)
        self.clientReceiver = ClientReceiver(self)
        self.clientSender.start()
        self.clientReceiver.start()

    def initSocket(self):
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.socket.connect((self.addr, self.port))
        except socket.error:
            print("Error in creating the socket!")

    def sendPacket(self, packet):
        self.seqOut = self.seqOut + 1
        packet.seq = self.seqOut
        self.outputBuffer.append(packet)

class ClientSender(threading.Thread):
    def __init__(self, client):
        super().__init__()
        self.client = client

    def run(self):
        while(self.client.running):
            for packet in self.client.outputBuffer:
                self.client.socket.sendto(packet.encode(), (self.client.addr, self.client.port))
                self.client.outputBuffer.remove(packet)

class ClientReceiver(threading.Thread):
    def __init__(self, client):
        super().__init__()
        self.client = client

    def run(self):
        while(self.client.running):
            rawPacket = self.client.socket.recvfrom(1024)
            packet_payload = rawPacket[0]
            packet = Packet()
            packet.decode(packet_payload)
            self.client.inputBuffer.append(packet)
            self.client.onReceive(packet)
