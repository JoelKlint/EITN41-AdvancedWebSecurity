from random import randint
from hashlib import sha1

def generate_k():
    k = ""
    for i in range(16):
        k += str(randint(0,1))
    return k

def bits_to_int(our_bits):
    return int(our_bits, 2)

def int_to_hex(our_int):
    return hex(our_int)[2:]

def hex_to_int(our_hex):
    return int(our_hex, 16)

def int_to_bits(our_bits):
    return "{0:b}".format(our_bits)