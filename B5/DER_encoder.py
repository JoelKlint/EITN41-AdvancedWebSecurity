import base64
def bits_to_int(our_bits):
    return int(our_bits, 2)

def int_to_hex(our_int):
    return hex(our_int)[2:]

def hex_to_int(our_hex):
    return int(our_hex, 16)

def int_to_bits(our_bits, chars = 0):
    return "{0:b}".format(our_bits).zfill(chars)

def length_Long_Definite_Form(V):
    bytes_in_V_int = int(len(V) / 2)
    bytes_in_V_hex = int_to_hex(bytes_in_V_int)

    L = "---LENGTH-GOES-HERE-LDF---"

    # Do not allow half octets
    if len(bytes_in_V_hex) % 2 != 0:
        bytes_in_V_hex = "0" + bytes_in_V_hex

    if len(bytes_in_V_hex) > 2 or int_to_bits(bytes_in_V_int, 8)[0] == "1":
        bytes_in_L_int = int(len(bytes_in_V_hex) / 2)
        bytes_in_L_bits = int_to_bits(bytes_in_L_int, 7)
        bytes_in_L_bits = "1" + bytes_in_L_bits
        bytes_in_L_hex = int_to_hex(bits_to_int(bytes_in_L_bits))
        L = bytes_in_L_hex + bytes_in_V_hex
    else:
        L = bytes_in_V_hex

    return L

def DER_encode(integer, LDF=True):
    # print()
    T = "02"

    V = ""

    # # Pad V so it becomes even octets
    V = hex(integer)[2:]
    V_bits = "0" + int_to_bits(hex_to_int(V))
    if len(V_bits) % 8 != 0:
        missing_chars = 8 - (len(V_bits) % 8)
        V_bits = "0" * missing_chars + V_bits

    V_length = int(len(V_bits) / 8)
    V = int_to_hex(bits_to_int(V_bits))
    while V_length > len(V)/2:
        V = "0" + V


    L = "---LENGTH-GOES-HERE---"

    # Short definite form
    if V_length <= 127:
        # print("SDF")
        L = hex(V_length)[2:]
        if len(L) % 2 == 1:
            L = "0" + str(L)
        else:
            L = str(L)
    else:
        if LDF:
            # print("LDF")
            L = length_Long_Definite_Form(V)
        else:
            # print("LIF")
            # MUST BE HEX
            L = "10000000"
            V += "0" * 8 * 2

    # print("T: {}".format(T))
    # print("L: {}".format(L))
    # print("V: {}".format(V))
    return T + L + V

def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = egcd(b % a, a)
        return (g, x - (b // a) * y, y)

def modinv(a, m):
    g, x, y = egcd(a, m)
    if g != 1:
        raise Exception('modular inverse does not exist')
    else:
        return x % m

def ass_3(p, q, e=65537):
    VERSION = 0
    n = p * q
    d = modinv(e, (p-1) * (q-1))
    exp1 = d % (p-1)
    exp2 = d % (q-1)
    coefficient = modinv(q, p)

    print("Version: {}".format(VERSION))
    print("n: {}".format(n))
    print("e: {}".format(e))
    print("d: {}".format(d))
    print("p: {}".format(p))
    print("q: {}".format(q))
    print("exponent1: {}".format(exp1))
    print("exponent2: {}".format(exp2))
    print("coefficient: {}".format(coefficient))

    DER_VERSION = DER_encode(VERSION)
    DER_n = DER_encode(n)
    DER_e = DER_encode(e)
    DER_d = DER_encode(d)
    DER_p = DER_encode(p)
    DER_q = DER_encode(q)
    DER_exp1 = DER_encode(exp1)
    DER_exp2 = DER_encode(exp2)
    DER_coefficient = DER_encode(coefficient)

    print()
    print("DER VERSION: {}".format(DER_VERSION))
    print("DER n: {}".format(DER_n))
    print("DER e: {}".format(DER_e))
    print("DER d: {}".format(DER_d))
    print("DER p: {}".format(DER_p))
    print("DER q: {}".format(DER_q))
    print("DER exponent1: {}".format(DER_exp1))
    print("DER exponent2: {}".format(DER_exp2))
    print("DER coefficient: {}".format(DER_coefficient))

    print()
    RSA_V = DER_VERSION + DER_n + DER_e + DER_d + DER_p + DER_q + DER_exp1 + DER_exp2 + DER_coefficient

    RSA_priv_key = DER_encode(hex_to_int(RSA_V))
    RSA_priv_key = "30" + RSA_priv_key[2:]

    print()
    print(RSA_priv_key)
    print()
    print(base64.b64encode(bytearray.fromhex(RSA_priv_key)))

ass_3(
    139721121696950524826588106850589277149201407609721772094240512732263435522747938311240453050931930261483801083660740974606647762343797901776568952627044034430252415109426271529273025919247232149498325412099418785867055970264559033471714066901728022294156913563009971882292507967574638004022912842160046962763, 
    141482624370070397331659016840167171669762175617573550670131965177212458081250216130985545188965601581445995499595853199665045326236858265192627970970480636850683227427420000655754305398076045013588894161738893242561531526805416653594689480170103763171879023351810966896841177322118521251310975456956247827719
)

# integer = 2530368937
# integer = 161863091426469985001358176493540241719547661391527305133576978132107887717901972545655469921112454527920502763568908799229786534949082469136818503316047702610019730504769581772016806386178260077157969035841180863069299401978140025225333279044855057641079117234814239380100022886557142183337228046784055073741
# print(DER_encode(integer))
