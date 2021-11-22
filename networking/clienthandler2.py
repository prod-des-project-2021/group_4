from queue import Queue
import time

class ClientHandler:
    def __init__(self, service, addr):
        self.inputBuffer = Queue()
        self.outputBuffer = Queue()

        self.service = service # handle to server

        self.addr       = addr # tuple(ip, port)
        self.seqIn      = 0
        self.seqOut     = 0
        self.timeout    = 0 # when last packet was received

    def send(self):
        pass

    def receive(self, raw): # raw UDP packet
        self.seqIn = self.seqIn + 1
        self.timeout = int(time.time() / 1000)
        #self.inputBuffer.put(Packet().decode(raw))

    def process(self):
        '''if(packet.type == 1):
            pass
        elif(packet.type == 2):
            pass
        elif(packet.type == 3):
            pass
        elif(packet.type == 4):
            pass
        elif(packet.type == 5):
            pass
        elif(packet.type > 5 and packet.type < 10):
            pass
        else:
            pass'''
