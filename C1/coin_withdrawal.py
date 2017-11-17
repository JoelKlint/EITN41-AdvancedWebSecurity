import random
import hashlib
import sys

def extended_gcd(aa, bb):
    lastremainder, remainder = abs(aa), abs(bb)
    x, lastx, y, lasty = 0, 1, 1, 0
    while remainder:
        lastremainder, (quotient, remainder) = remainder, divmod(lastremainder, remainder)
        x, lastx = lastx - quotient*x, x
        y, lasty = lasty - quotient*y, y
    return lastremainder, lastx * (-1 if aa < 0 else 1), lasty * (-1 if bb < 0 else 1)

def modinv(a, m):
	g, x, y = extended_gcd(a, m)
	if g != 1:
		raise ValueError
	return x % m

class Shared:
    def _hex_to_int(hex):
        return int(hex, 16)

    def _f_func(a, b):
        return 6**3 + 13 + Shared._hex_to_int(a) + Shared._hex_to_int(b)

    def _h_func(a, b):
        c = int(str(a) + str(b))
        return hashlib.sha1(bytearray(c)).hexdigest()

    def _x_func(quad):
        return Shared._h_func(quad['a'], quad['c'])

    def _y_func(quad, ID, n):
        return Shared._h_func(quad['a']^ID, quad['d'])

    def calc_B(quad, e, n, ID):
        x = Shared._x_func(quad)
        y = Shared._y_func(quad, ID, n)
        result = (pow(quad['r'], e, n) * Shared._f_func(x, y)) % n
        if result == 0:
            print("B IS 0!!!")
            print("f: {}".format(Share._f_func(x, y)))
            print("r: {}".format(quad['r']))
            print("e: ".format(e))
            print("n: {}".format(n))
        return result

    def get_indicies_from_array(array, indicies):
        return [array[i] for i in indicies]

class Alice:
    def __init__(self, conf):
        self.e = conf['e']
        self.k = conf['k']
        self.n = conf['n']
        self.ID = conf['ID']
        self.secret_R = list(range(2 * self.k))

    def _generate_random_int(self):
        return random.randint(1, self.n)

    def generate_2k_numbers(self):
        result = []
        for i in range(2 * self.k):
            result.append({
                'a': self._generate_random_int(),
                'c': self._generate_random_int(),
                'd': self._generate_random_int(),
                'r': self._generate_random_int()
            })
        a1 = result[0]['a']
        print("[Alice] A1 is: {}".format(a1))
        print("[Alice] A1 mod ID is: {}".format(a1^self.ID))
        self.quads = result

    def _calc_B(self, quad):
        return Shared.calc_B(quad, self.e, self.n, self.ID)

    def calculate_all_B(self):
        self.B = list(map(lambda quad: self._calc_B(quad), self.quads))
        print("[Alice] B: {}".format(self.B))

    def get_B(self):
        return self.B

    def expose_quad(self, index):
        self.secret_R.remove(index)
        return self.quads[index]

    def extract_serial_number(self, sign):
        quads = Shared.get_indicies_from_array(self.quads, self.secret_R)
        prod = 1
        for quad in quads:
            prod *= quad['r'] % self.n
        prod = prod % self.n
        serial_nr = (modinv(prod, self.n) * sign) % self.n
        print("[Alice] Serial number: {}".format(serial_nr))
        return serial_nr

class Bank:
    def __init__(self, conf):
        self.e = conf['e']
        self.d = conf['d']
        self.n = conf['n']
        self.ID = conf['ID']

    def set_B(self, B):
        self.B = B

    def pick_half_of_all_indicies(self):
        k = int(len(self.B) / 2)
        a = list(range(2 * k))
        random.shuffle(a)
        self.R = a[:k]
        self.Rinv = a[k:]
        print("[Bank] picked indicies: {}".format(self.R))

    def _calc_B(self, quad):
        return Shared.calc_B(quad, self.e, self.n, self.ID)

    def get_R(self):
        return self.R

    def verify_Bi(self, index, quad):
        temp_B = self._calc_B(quad)
        print("[Bank] Verifying B{} - {}".format(index, temp_B))
        if temp_B == self.B[index]:
            return True
        else:
            return False

    def sign_blindly(self):
        unverified_B = Shared.get_indicies_from_array(self.B, self.Rinv)
        prod = 1
        for B in unverified_B:
            prod *= pow(B, self.d, self.n)
        self.blind_signature = prod % self.n
        print("[Bank] Signature: {}".format(self.blind_signature))

    def get_blind_signature(self):
        return self.blind_signature
    

global_p = 193
global_q = 103
global_n = global_p * global_q
global_e = 19

phi_n = (global_p-1) * (global_q-1)
global_d = modinv(global_e, phi_n)

global_k = 10
global_ID = 1337

print("___RSA params___")
print("p: {}".format(global_p))
print("q: {}".format(global_q))
print("n: {}".format(global_n))
print("e: {}".format(global_e))
print("d: {}".format(global_d))
print()
print("k: {}".format(global_k))
print("ID: {}".format(global_ID))
print()

alice_conf = {
    "e": global_e,
    "n": global_n,
    "ID": global_ID,
    "k": global_k
}

bank_conf = {
    "e": global_e,
    "n": global_n,
    "ID": global_ID,
    "d": global_d
}

alice = Alice(alice_conf)
bank = Bank(bank_conf)

# Alice
alice.generate_2k_numbers()
alice.calculate_all_B()
B = alice.get_B()

# Bank
bank.set_B(B)
bank.pick_half_of_all_indicies()

# Bank verifies Alice
for i in bank.get_R():
    quad = alice.expose_quad(i)
    alice_is_honest = bank.verify_Bi(i, quad)
    if not alice_is_honest:
        print("Alice is a cheater")
        sys.exit(1)
    
# Bank
bank.sign_blindly()
signature = bank.get_blind_signature()

serial_nr = alice.extract_serial_number(signature)