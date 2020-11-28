import bitarray

class Packet:
    def __init__(self, seq, payload):
        self.seq = seq
        self.payload = payload
        self.preamble = [0, 1, 0, 1, 0, 1, 0, 1]

    def make(self):
        ba = bytearray()
        ba.extend(self.preamble)
        ba.extend(self.seq.to_bytes(2, byteorder='big'))
        ba.extend(len(self.payload).to_bytes(1, byteorder='big'))
        ba.extend(self.payload)
        return ba