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
    k = 3
    n = 6
    private_polynomial = interpolate.lagrange(
        [0] + list(range(2, n+1)), 
        [9] + [67, 111, 165, 229, 303]
    )
    shares = [37, 18, 40, 44, 28]
    participants = [4, 5]
    shared_master_points = [1385, 2028]

    deactivate_circuit(
        k, 
        n, 
        private_polynomial, 
        shares,
        participants,
        shared_master_points
    )