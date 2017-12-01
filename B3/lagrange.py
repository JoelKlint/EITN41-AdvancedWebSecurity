from scipy import interpolate

# We assume we are ALWAYS person 1

def deactivate_circuit(k, n, private_polynomial, shares, participants, shared_master_points):
    f1_1 = private_polynomial(1)
    shares.insert(0, int(f1_1))
    f_1 = sum(shares)

    master_poly = interpolate.lagrange(
        [1] + participants,
        [f_1] + shared_master_points
    )

    print(master_poly(0))

if __name__ == "__main__":
    k = 5
    n = 8
    private_polynomial = interpolate.lagrange(
        [0, 1, 2, 3, 4, 5, 6, 7, 8], 
        [13, 38, 161, 568, 1565, 3578, 7153, 12956, 21773]
    )
    shares = [75, 75, 54, 52, 77, 54, 43]
    participants = [2, 4, 5, 7]
    shared_master_points = [2782, 30822, 70960, 256422]

    deactivate_circuit(
        k, 
        n, 
        private_polynomial, 
        shares,
        participants,
        shared_master_points
    )