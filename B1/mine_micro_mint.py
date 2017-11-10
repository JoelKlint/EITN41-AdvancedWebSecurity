from random import randrange

class MathStuff:
    def mean_value(samples):
        return sum(samples) / len(samples)

    def calculate_confidence_interval(samples, constant):
        mean_value = MathStuff.mean_value(samples)

        standard_deviation_sum = 0
        for sample in samples:
            standard_deviation_sum += ((sample - mean_value)**2)**1/2
        standard_deviation = standard_deviation_sum / len(samples)

        tail = standard_deviation / len(samples)**1/2
        return {
            "lower": mean_value - constant * tail,
            "upper": mean_value + constant * tail
        }

class Simulator:
    def __init__(self, u, k, c):
        self.u = u
        self.k = k
        self.c = c
        self.lamda = 3.66

    def simulate_once(self):
        bins = [0] * 2**u
        coin_count = 0
        iterations = 0
        while coin_count < c:
            iterations += 1
            bin = randrange(len(bins))
            bins[bin] += 1
            coin_count += 1 if bins[bin] == k else 0

        return iterations

    def calculate_mean_value(self, iterations):
        self.mean_value = MathStuff.mean_value(iterations)

    def calculate_confidence_interval(self, iterations):
        self.confidence_interval = MathStuff.calculate_confidence_interval(iterations, self.lamda)

    def print_report(self):
        print("Mean: {}".format(self.mean_value))
        print("Confidence interval lower: {}".format(self.confidence_interval["lower"]))
        print("Confidence interval upper: {}".format(self.confidence_interval["upper"]))

    def start(self, sim_count):
        total_iterations = 0
        iterations = []
        for _ in range(sim_count):
            iterations.append(self.simulate_once())

        self.calculate_mean_value(iterations)
        self.calculate_confidence_interval(iterations)

        self.print_report()

# Simulation config
u = 20
k = 7
c = 10000
sim_count = 24

simulator = Simulator(u, k, c)
simulator.start(sim_count)
