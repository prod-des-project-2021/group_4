import socket
import threading
import time
from queue import Queue

class Client:

    #######################
    # Initializing client #
    #######################
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.running = True
        self.bufferSize = 8192

        self.inputBuffer = Queue()
        self.outputBuffer = Queue()

        self.seqIn  = 0
        self.seqOut = 0

        # init the socket
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.socket.connect((ip, port))
        except socket.error:
            print("Unable to start connection")
            self.running = False

        # init threads
        self.receiverThread = threading.Thread(target=self.receiver)
        self.senderThread = threading.Thread(target=self.sender)

    #############
    # Interface #
    #############

    # starting up the client
    def start(self):
        self.receiverThread.start()
        self.senderThread.start()

    def stop(self):
        self.running = False

    def send(self, packet):
        self.outputBuffer.put(packet)

    ####################
    # Receiving thread #
    ####################
    def receiver(self):
        while(self.running):
            try:
                packet = self.socket.recvfrom(self.bufferSize)
                self.inputBuffer.put(packet)
            except socket.error:
                print("Client socket encountered an error")
                self.running = False

    ##################
    # Sending thread #
    ##################
    def sender(self):
        while(self.running):
            time.sleep(0.01)
            while not self.outputBuffer.empty():
                packet = self.outputBuffer.get()
                self.socket.sendto(packet.encode(), (self.ip, self.port))
