class ClientHandler:
    def __init__(self, service, addr, port):
        self.service    = service # handle to the service
        self.socket     = self.service.socket # handle to the services socket

        self.addr = addr
        self.port = port
        self.seqIn = 0  # sequence number
        self.seqOut = 0 # sequence number for outgoing packet

        self.outputBuffer   = list()
        self.inputBuffer    = list()

    def processPacket(self, packet):
        pass

    def sendPacket(self, packet):
        self.seqOut = self.seqOut + 1

        pass
