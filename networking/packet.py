class Packet():
    def __init__(self):
        self.protocol_header = "SPUDP01"
        self.priority = 0
        self.seq     = None
        self.payload = None

        # packet priority
        # 0 - don't care
        # 1 - must be ACKED


    def decode(self, raw):
        pass

    def encode(self):
        return bytes(self.priority)
