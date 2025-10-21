from unittest import TestCase
from random import randint
from ECDSA.PrivateKey import PrivateKey
from ECDSA.spec256k1_constants import N

class PrivateKeyTest(TestCase):

    def test_sign(self):
        pk = PrivateKey(randint(0, N))
        z = randint(0, 2**256)
        sig = pk.sign(z)
        self.assertTrue(pk.point.verify(z, sig))