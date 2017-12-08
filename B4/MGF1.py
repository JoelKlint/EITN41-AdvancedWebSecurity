import math
import hashlib


def I2OSP(number, size):
    if number > 256**size:
        return "number too big"
    return (hex(number)[2:].zfill(2*size))

def MGF1(mgfseed, masklen):
    if masklen > 2**32:
        return "mask too long"
    T = ""
    
    for i in range(0, int(math.ceil(masklen/sha1_output_size_octet))):
        print(I2OSP(i, 4))
        
        T += hashlib.sha1(bytearray.fromhex(mgfseed + I2OSP(i, 4))).hexdigest()

    return T[:int(2*masklen)]


mgfseed = "9b4bdfb2c796f1c16d0c0772a5848b67457e87891dbc8214"
masklen = 21.0
sha1_output_size_octet = 20.0
print(MGF1(mgfseed, masklen))