class Packet:

    #####################
    # Packet properties #
    #####################
    def __init__(self):
        self.header     = "SP"
        self.seq        = None
        self.priority   = 0
        self.type       = 0
        self.payload    = b'0x00'
        self.payloadLength = 1

    ####################################
    # Setting the payload              #
    # Payload must be BYTES object     #
    ####################################
    def setPayload(self, payload):
        self.payload = payload
        self.payloadLength = len(payload)

    ###################################
    # Encoding the packet to byteform #
    ###################################
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
        return encodedPacket

    #####################################
    # Decoding the packet from byteform #
    #####################################
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

    ###################
    # DEBUGGING PRINT #
    ###################
    def printDebug(self):
        print("Header: "+str(self.header))
        print("Priority: "+str(self.priority))
        print("Sequence no.: "+str(self.seq))
        print("Type: "+str(self.type))
        print("Payload len: "+str(self.payloadLength))
        print("Payload: "+str(self.payload))
