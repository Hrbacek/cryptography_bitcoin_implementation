from elliptic_curves.Point import Point
from ECDSA.S256Field import S256Field
from ECDSA.spec256k1_constants import A, B, N, gx, gy, P

from ECDSA.helper import hash160, encode_base58_checksum

# public key point
class S256Point(Point):

    def __init__(self, x, y, a=None, b=None):
        a, b = S256Field(A), S256Field(B)
        if type(x) == int:
            super().__init__(x=S256Field(x), y=S256Field(y), a=a, b=b)
        else:
            super().__init__(x=x, y=y, a=a, b=b)

    def __repr__(self):
        if self.x is None:
            return 'S256Point(infinity)'
        else:
            return 'S256Point({}, {})'.format(self.x, self.y)

    def __rmul__(self, coefficient):
        coef = coefficient % N
        return super().__rmul__(coef)
    
    # SEC format serialization
    # Bitcoin’s secp256k1 prime has the property that p % 4 = 3, which allows us to compute square roots easily.
    # So we only need to implement the y-coordinate calculation for compressed SEC format.
    def sec(self, compressed=True):
        if compressed:
            if self.y.num % 2 == 0:
                return b'\x02' + self.x.num.to_bytes(32, 'big')
            else:
                return b'\x03' + self.x.num.to_bytes(32, 'big')
        else:
            return b'\x04' + self.x.num.to_bytes(32, 'big') + \
                self.y.num.to_bytes(32, 'big')


    def hash160(self, compressed=True):
        return hash160(self.sec(compressed))

    def address(self, compressed=True, testnet=False):
        h160 = self.hash160(compressed)
        if testnet:
            prefix = b'\x6f'
        else:
            prefix = b'\x00'
        return encode_base58_checksum(prefix + h160)

    @classmethod
    def parse(self, sec_bin):
        if sec_bin[0] == 4: # uncompressed format
            x = int.from_bytes(sec_bin[1:33], 'big')
            y = int.from_bytes(sec_bin[33:65], 'big')
            return S256Point(x, y)

        else: # compressed format
            x = S256Field(int.from_bytes(sec_bin[1:33], 'big'))
            alpha = x**3 + S256Field(B)
            beta = alpha.sqrt()
            if (beta.num % 2 == 0 and sec_bin[0] == 2) or (beta.num % 2 == 1 and sec_bin[0] == 3):
                return S256Point(x.num, beta.num)
            else:
                return S256Point(x.num, P - beta.num)

    # r,s,z are integers modulo N, representing scalar values that multiply points on the curve.
    def verify(self, z, sig):
        s_inv = pow(sig.s, N - 2, N)
        u = (z * s_inv) % N
        v = (sig.r * s_inv) % N
        total = u * S256Point(gx, gy) + v * self
        return total.x.num == sig.r
