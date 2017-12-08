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
        T += hashlib.sha1(bytearray.fromhex(mgfseed + I2OSP(i, 4))).hexdigest()

    return T[:int(2*masklen)]

def OAEP_encode(M, seed, L=""):
    lHash = hashlib.sha1(L.encode('utf-8')).hexdigest()
    PS = "".zfill((k - int(len(M)/2) - 40 - 2)*2)
    DB = lHash + PS + "01" + M
    dbMask = MGF1(seed, k-20-1)
    maskedDB = int(DB, 16) ^ int(dbMask, 16)
    maskedDB = hex(maskedDB)[2:]
    seedMask = MGF1(maskedDB, 20)
    maskedSeed = int(seed, 16) ^ int(seedMask, 16)
    maskedSeed = hex(maskedSeed)[2:]
    EM = "00" + maskedSeed + maskedDB
    EM = EM.zfill(256)
    return EM[:256]

def OAEP_decode(EM, L=""):
    lHash = hashlib.sha1(L.encode('utf-8')).hexdigest()
    Y = EM[:2]
    maskedSeed = EM[2:42]
    maskedDB = EM[42:]
    seedMask = MGF1(maskedDB, 20)
    seed = hex(int(maskedSeed, 16) ^ int(seedMask, 16))[2:]
    dbMask = MGF1(seed, 107)
    DB = hex(int(maskedDB, 16) ^ int(dbMask, 16))[2:]
    lHash_prim = DB[:40]
    M = ""
    print(lHash)
    print(lHash_prim)
    print(Y)
    if lHash_prim != lHash or Y != "00":
        M = "decryption error 1"
        return M
    
    for i in range(42, len(DB)):
        if DB[i-2:i] == "01":
            M = DB[i:]
            return M
        elif DB[i-2:i] != "00":
            M = "decryption error 2"
            return M


    
# Input for MGF1
mgfseed = "9b4bdfb2c796f1c16d0c0772a5848b67457e87891dbc8214"
masklen = 21.0
sha1_output_size_octet = 20.0

# Input for OAEP
M = "c107782954829b34dc531c14b40e9ea482578f988b719497aa0687"
seed = "1e652ec152d0bfcd65190ffc604c0933d0423381"
k = 128
EM = "0063b462be5e84d382c86eb6725f70e59cd12c0060f9d3778a18b7aa067f90b2178406fa1e1bf77f03f86629dd5607d11b9961707736c2d16e7c668b367890bc6ef1745396404ba7832b1cdfb0388ef601947fc0aff1fd2dcd279dabde9b10bfc51efc06d40d25f96bd0f4c5d88f32c7d33dbc20f8a528b77f0c16a7b4dcdd8f"


mask = MGF1(mgfseed, masklen)
EM_value = OAEP_encode(M, seed)
decode_value = OAEP_decode(EM)


print("THIS IS MGF1: \n{0}\n\nWITH length: {1}".format(mask, len(mask)))
print("\n----------------------------------------------\n")
print("THIS IS OAEP_encode: \n{0}\n\nWITH length: {1}".format(EM_value, len(EM_value)))
print("\n----------------------------------------------\n")
print("THIS IS OAEP_decode: \n{0}\n\nWITH length: {1}".format(decode_value, len(decode_value)))

