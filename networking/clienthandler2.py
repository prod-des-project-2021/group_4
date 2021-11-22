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
        self.id         = service.generateClientId() # each client must have unique id

    def send(self):
        pass

    def receive(self, raw): # raw UDP packet
        self.seqIn = self.seqIn + 1
        self.timeout = time.perf_counter()
        #self.inputBuffer.put(Packet().decode(raw))

    # returns False on timeout,
    # otherwise True
    def process(self):

        # if client has timed out, return false
        # and give control to the main thread
        if(time.perf_counter() > self.timeout + 3.0):
            return False

        return True
