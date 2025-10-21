from finite_fields.FieldElement import FieldElement
from ECDSA.spec256k1_constants import P

class S256Field(FieldElement):

    def __init__(self, num, prime=None):
        super().__init__(num=num, prime=P)

    def __repr__(self):
        return '{:x}'.format(self.num).zfill(64)
    
    def sqrt(self):
        return self**((P + 1) // 4)

    # zfill(64) pads the hexadecimal string, not the bit string.
    # Each hex digit = 4 bits → 256 bits / 4 = 64 hex digits.
    # So .zfill(64) ensures the printed value always shows exactly 64 hex characters, which corresponds to 256 bits.