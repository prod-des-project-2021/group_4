import struct

class Packet():
    def __init__(self):
        self.addr = None
        self.port = None
        self.header = "SP"
        self.priority = 0
        self.seq     = 0
        self.type    = 0
        self.payload = b'0x00'
        self.payloadLength = 1
        self.packetLength = 0

    def setPriority(self, priority):
        self.priority = priority

    def setSequence(self, seq):
        self.seq = seq

    def setType(self, type):
        self.type = type

    def setDestination(self, addr, port):
        self.addr = addr
        self.port = port

    def setPayload(self, payload):
        self.payload = payload
        self.payloadLength = len(payload)
        if(self.payloadLength > 1024):
            print("PACKET LIMIT EXCEEDED!")
        self.calculatePacketSize()

    def calculatePacketSize(self):
        size = struct.calcsize('2s h i h i')
        size = size + self.payloadLength
        self.packetLength = size

    def decode(self, raw):

        # fcalculating the size of the static part of the packet
        staticSize = struct.calcsize('2s h i h i')

        # decoding the static part
        decodedPacket = struct.unpack_from('2s h i h i', raw, 0)

        self.header         = decodedPacket[0].decode()
        self.priority       = decodedPacket[1]
        self.seq            = decodedPacket[2]
        self.type           = decodedPacket[3]
        self.payloadLength  = decodedPacket[4]

        # decoding the payload with a variable size
        decodedPayload = struct.unpack_from(str(self.payloadLength)+'s', raw, staticSize)
        self.payload = decodedPayload[0]

        self.calculatePacketSize()

    def encode(self):
        format = '2s h i h i '+str(self.payloadLength)+'s'
        encodedPacket = struct.pack(format,
            bytes(self.header, "utf-8"),
            self.priority,
            self.seq,
            self.type,
            self.payloadLength,
            self.payload
        )

        self.calculatePacketSize()

        return encodedPacket

    def printDebug(self):
        print("Header: "+str(self.header))
        print("Priority: "+str(self.priority))
        print("Sequence no.: "+str(self.seq))
        print("Type: "+str(self.type))
        print("Payload len: "+str(self.payloadLength))
        print("Payload: "+str(self.payload))
        print("Total len: "+str(self.packetLength))

    class Priority:
        NO_ACK_REQUIRED  = 0
        ACK_REQUIRED     = 1

    # packet types from 1 to 10 are reserved for the system
    class Type:
        START_CONNECTION = 1
        CLOSE_CONNECTION = 2
        ACK = 3
        PING = 4
        PONG = 5
