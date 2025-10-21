from io import BytesIO

class Signature:

    def __init__(self, r, s) -> None:
        self.r = r
        self.s = s
    
    def __repr__(self):
        return 'Signature({:x},{:x})'.format(self.r, self.s)
    
    # Distinguished Encoding Rules (DER) serialization
    def der(self):
        r_bytes = self.r.to_bytes(32, 'big')
        s_bytes = self.s.to_bytes(32, 'big')

        # Remove leading zeros
        r_bytes = r_bytes.lstrip(b'\x00')
        s_bytes = s_bytes.lstrip(b'\x00')

        # If the first byte is >= 0x80, prepend a zero byte
        if r_bytes[0] >= 0x80:
            r_bytes = b'\x00' + r_bytes
        if s_bytes[0] >= 0x80:
            s_bytes = b'\x00' + s_bytes

        der_r = b'\x02' + len(r_bytes).to_bytes(1, 'big') + r_bytes
        der_s = b'\x02' + len(s_bytes).to_bytes(1, 'big') + s_bytes
        der_seq = b'\x30' + (len(der_r) + len(der_s)).to_bytes(1, 'big') + der_r + der_s
        return der_seq

    @classmethod
    def parse(cls, signature_bin):
        s = BytesIO(signature_bin)
        compound = s.read(1)[0]
        if compound != 0x30:
            raise SyntaxError("Bad Signature")
        length = s.read(1)[0]
        if length + 2 != len(signature_bin):
            raise SyntaxError("Bad Signature Length")
        marker = s.read(1)[0]
        if marker != 0x02:
            raise SyntaxError("Bad Signature")
        rlength = s.read(1)[0]
        r = int.from_bytes(s.read(rlength), 'big')
        marker = s.read(1)[0]
        if marker != 0x02:
            raise SyntaxError("Bad Signature")
        slength = s.read(1)[0]
        s = int.from_bytes(s.read(slength), 'big')
        if len(signature_bin) != 6 + rlength + slength:
            raise SyntaxError("Signature too long")
        return cls(r, s)