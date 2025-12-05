from random import randint
import hashlib
import hmac

from ECDSA.S256Point import S256Point
from ECDSA.spec256k1_constants import gx, gy, N
from ECDSA.Signature import Signature

from ECDSA.helper import encode_base58_checksum

class PrivateKey:
    def __init__(self, secret):
        self.secret = secret
        self.point = secret * S256Point(gx, gy) #public key point
    
    def hex(self):
        return '{:x}'.format(self.secret).zfill(64)
    
    def sign(self, z):
        k = self.deterministic_k(z)
        r = (k * S256Point(gx, gy)).x.num
        k_inv = pow(k, N - 2, N)
        s = (z + r * self.secret) * k_inv % N

        if s > N / 2: # low-S normalization
            s = N - s
        return Signature(r, s)
    
    # RCF 6979 deterministic k generation
    def deterministic_k(self, z):
        k = b'\x00' * 32
        v = b'\x01' * 32
        if z > N:
            z -= N
        z_bytes = z.to_bytes(32, 'big')
        secret_bytes = self.secret.to_bytes(32, 'big')
        s256 = hashlib.sha256

        k = hmac.new(k, v + b'\x00' + secret_bytes + z_bytes, s256).digest()
        v = hmac.new(k, v, s256).digest()
        k = hmac.new(k, v + b'\x01' + secret_bytes + z_bytes, s256).digest()
        v = hmac.new(k, v, s256).digest()

        while True:
            v = hmac.new(k, v, s256).digest()
            candidate = int.from_bytes(v, 'big')
            if 1 <= candidate < N:
                return candidate
            k = hmac.new(k, v + b'\x00', s256).digest()
            v = hmac.new(k, v, s256).digest()
    
    def wif(self, compressed=True, testnet=False):
        secret_bytes = self.secret.to_bytes(32, 'big')
        if testnet:
            prefix = b'\xef'
        else:
            prefix = b'\x80'
        if compressed:
            suffix = b'\x01'
        else:
            suffix = b''
        return encode_base58_checksum(prefix + secret_bytes + suffix)