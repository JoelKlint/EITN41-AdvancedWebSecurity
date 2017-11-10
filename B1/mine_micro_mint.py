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

    def mean_value(self, iterations, sim_count):
        totalt_iterations = sum(iterations)
        return total_iterations/ self.sim_count

    def confidence_interval(self, iterations, mean_value, sim_count):
        for iteration in iterations:
            standard_deviation_sum += ((iteration - mean_value)**2)**1/2
        standard_deviation = standard_deviation_sum_tot / len(iterations)
        interval = {"lower": mean_value - standard_deviation / self.sim_count**1/2),
                    "upper": mean_value + standard_deviation / self.sim_count**1/2}
        return interval

    def start(self):
        total_iterations = 0
        iterations = []
        for _ in range(sim_count):
            iterations.append(self.simulate_once())
        self.average_iterations = mean_value(iterations, sim_count)
        confidence_interval = confidence_interval(self, iterations)
        )


# Simulation config
u = 16
k = 2
c = 1
sim_count = 10

simulator = Simulator(u, k, c, sim_count)
simulator.start()
