from random import randint
import hashlib
import itertools

X_LENGTH = 16
K_LENGTH = 16

_all_possible_k = None

def generate_all_possible_k():
    global _all_possible_k
    if(_all_possible_k == None):
        all_vals = list(map(list, itertools.product([0, 1], repeat=K_LENGTH)))
        all_vals = list(map(lambda x: list(map(str, x)), all_vals))
        all_vals = list(map(lambda x: "".join(x), all_vals))
        _all_possible_k = all_vals
    return _all_possible_k

def generate_k():
    k = ""
    for i in range(K_LENGTH):
        k += str(randint(0,1))
    return k

def bits_to_int(our_bits):
    return int(our_bits, 2)

def int_to_hex(our_int):
    return hex(our_int)[2:]

def hex_to_int(our_hex):
    return int(our_hex, 16)

def int_to_bits(our_bits, chars = 16):
    return "{0:b}".format(our_bits).zfill(chars)

def vote(v):
    k = generate_k()
    bit_array = k + str(v)
    int_val = bits_to_int(bit_array)
    hex_val = int_to_hex(int_val).zfill(10)
    hasher = hashlib.sha1()
    hasher.update(bytearray.fromhex(hex_val))
    x_hex = hasher.hexdigest()
    x_int = hex_to_int(x_hex)
    x_bits = int_to_bits(x_int)
    return x_bits[:X_LENGTH], k

def simulate_binding_once():
    true_vote = randint(0, 1)
    fake_vote = 1 - true_vote

    true_x, true_k = vote(true_vote)
    fake_x = "some-random-value-that-will-never-match"
    i = 0
    while fake_x != true_x:
        i += 1
        fake_x, fake_k = vote(fake_vote)
    
    return i

def simulate_bindings(iterations = 100):
    print("--------------------------------")
    print("Starting binding simulation...")
    print("Simulations: {}".format(iterations))

    attemts = []
    for i in range(iterations):
        attemt_count = simulate_binding_once()
        attemts.append(attemt_count)
        print(" - Attemts in iteration {}: {}".format(i+1, attemt_count))

    probability = iterations / sum(attemts)
    print()
    print("Probability of breaking binding property: {}".format(probability))

def simulate_concealing_once():
    alice_x, alice_k, = vote(randint(0, 1))

    found_yes_match = False
    found_no_match = False

    all_k = generate_all_possible_k()
    for i in range(len(all_k)):
        if found_yes_match and found_no_match:
            break
        yes_x, yes_k = vote(1)
        if yes_x == alice_x:
            found_yes_match = True

        no_x, no_k = vote(0)
        if no_x == alice_x:
            found_no_match = True
    
    return not (found_yes_match and found_no_match)


def simulate_concealing(iterations = 100):
    print("--------------------------------")
    print("Starting concealing simulation...")
    print("Simulations: {}".format(iterations))

    broke_concealing_count = 0
    for i in range(iterations):
        broke_concealing = simulate_concealing_once()
        print(" - Broke concealing in iteration {}: {}".format(i+1, broke_concealing))
        if broke_concealing:
            broke_concealing_count += 1
    
    probability = broke_concealing_count / iterations
    print()
    print("Probability of breaking concealing property: {}".format(probability))

if __name__ == '__main__':
    X_LENGTH = 16
    K_LENGTH = 16

    print("bits in V: 1")
    print("bits in K: {}".format(K_LENGTH))
    print("bits in X: {}".format(X_LENGTH))

    simulate_bindings()
    simulate_concealing()