from unittest import TestCase, TestSuite, TextTestRunner

import hashlib


BASE58_ALPHABET = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'

def hash160(s):
    return hashlib.new('ripemd160', hashlib.sha256(s).digest()).digest()

def hash256(s):
    return hashlib.sha256(hashlib.sha256(s).digest()).digest()

def encode_base58(s):
    count = 0
    for c in s:
        if c == 0:
            count += 1
        else:
            break
    num = int.from_bytes(s, 'big')
    prefix = '1' * count
    result = ''
    while num > 0:
        num, mod = divmod(num, 58)
        result = BASE58_ALPHABET[mod] + result
    return prefix + result

def encode_base58_checksum(b):
    return encode_base58(b + hash256(b)[:4])

def decode_base58(s):
    num = 0
    for c in s:
        num *= 58
        num += BASE58_ALPHABET.index(c)
    combined = num.to_bytes(25, byteorder='big')
    checksum = combined[-4:]
    if hash256(combined[:-4])[:4] != checksum:
        raise ValueError('bad address: {} {}'.format(checksum, hash256(combined[:-4])[:4]))
    return combined[1:-4]

# Var ints to help with serialization of transaction inputs and outputs
def read_varint(s):
    i = s.read(1)[0]
    if i == 0xfd:
        return int.from_bytes(s.read(2), 'little')
    elif i == 0xfe:
        return int.from_bytes(s.read(4), 'little')
    elif i == 0xff:
        return int.from_bytes(s.read(8), 'little')
    else:
        return i

def encode_varint(i):
    if i < 0xfd:
        return i.to_bytes(1, 'little')
    elif i < 0x10000:
        return b'\xfd' + i.to_bytes(2, 'little')
    elif i < 0x100000000:
        return b'\xfe' + i.to_bytes(4, 'little')
    elif i < 0x10000000000000000:
        return b'\xff' + i.to_bytes(8, 'little')
    else:
        raise ValueError('integer too large: {}'.format(i))