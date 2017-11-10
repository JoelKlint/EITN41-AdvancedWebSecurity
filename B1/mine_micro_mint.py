from random import randint
import random

class Simulator:

    def __init__(self, u, k, c, sim_count):
        self.u = u
        self.k = k
        self.c = c
        self.sim_count = sim_count
        self.lamda = 3.66


    def simulate_once(self):
        bins = [0] * 2**u
        coin_count = 0
        iterations = 0
        while coin_count < c:
            iterations += 1
            bin = random.randrange(len(bins))
            bins[bin] += 1
            coin_count += 1 if bins[bin] == k else 0

        return iterations


    def start(self):
        total_iterations = 0
        iterations = []
        for _ in range(sim_count):
            iteration.append(self.simulate_once())
        total_iterations = sum(iteration)
        self.average_iterations = total_iterations / self.sim_count
        confidence_interaval = 0
        for iteration in iterations:
            confidence_interaval_sum

        self.average_iterations + (self.lamda * ())



# Simulation config
u = 16
k = 2
c = 1
sim_count = 10

simulator = Simulator(u, k, c, sim_count)
simulator.start()









