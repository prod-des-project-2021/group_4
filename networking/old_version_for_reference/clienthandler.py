import threading
from .packet import Packet
import time

# spaghetti bolognese
# needs rewriting

class ClientHandler:
    def __init__(self, service, addr, port):
        self.service    = service # handle to the service
        self.socket     = self.service.socket # handle to the services socket

        self.addr = addr
        self.port = port

        self.seqIn = 0  # sequence number
        self.seqOut = 0 # sequence number for outgoing packet
        self.packetTime = 0

        self.outputBuffer   = list()
        self.inputBuffer    = list()

        self.clientSender = ClientSender(self)
        self.clientReceiver = ClientReceiver(self)

        self.clientSender.start()
        self.clientReceiver.start()

    def addToInputBuffer(self, packet):
        self.inputBuffer.append(packet)

    def sendPacket(self, packet):
        self.outputBuffer.append(packet)


class ClientSender(threading.Thread):
    def __init__(self, clientHandler):
        super().__init__()
        self.clientHandler = clientHandler
        self.socket = clientHandler.service.socket

    def run(self):
        while(self.clientHandler.service.running):
            for packet in self.clientHandler.outputBuffer:
                self.clientHandler.seqOut = self.clientHandler.seqOut + 1
                packet.seq = self.clientHandler.seqOut
                self.socket.sendto(packet.encode(), (self.clientHandler.addr, self.clientHandler.port))
                self.clientHandler.outputBuffer.remove(packet)

class ClientReceiver(threading.Thread):
    def __init__(self, clientHandler):
        super().__init__()
        self.clientHandler = clientHandler

    def run(self):
        while(self.clientHandler.service.running):
            for packet in self.clientHandler.inputBuffer:
                self.clientHandler.packetTime = time.time() / 1000 # last received packet
                self.seqIn = packet.seq

                if packet.type == Packet.Type.START_CONNECTION:
                    self.clientHandler.service.onConnect(self, packet)
                elif packet.type == Packet.Type.CLOSE_CONNECTION:
                    self.clientHandler.service.onDisconnect(self, self)
                else:
                    self.clientHandler.service.onReceive(self.clientHandler.service, self.clientHandler, packet)

                self.clientHandler.inputBuffer.remove(packet)
