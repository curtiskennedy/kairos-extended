"""
Experimental setup utilizes 4 distributions:

BENIGN DISTRIBUTION

DRIFTING DISTRIBUTION

DRIFTED DISTRIBUTION

THREAT DISTRIBUTION

Each distribution is a normal distribution with mean, variance, max cutoff, min cutoff

The benign distribution has some overlap with the drifting distribution, which has some overlap with the drifted distribution

The drifted distribution, the benign distribution, and the threat distribution have no overlap
"""
import torch
import matplotlib.pyplot as plt
import numpy as np


class NormalDistribution:
    def __init__(self, mean, variance, max, min) -> None:
        """initialize a normal distribution with mean, variance, max cutoff, min cutoff"""
        self.mean = mean
        self.std = variance
        self.max = max
        self.min = min

    def sample(self, N: int) -> list:
        samples = []
        while len(samples) < N:
            sample = torch.normal(mean=self.mean, std=self.std, size=(1,))
            if self.min < sample.item() < self.max:
                samples.append(sample.item())
        return samples
    
    def visualize(self, N: int, filename: str, bins: int, title: str) -> None:
        samples = self.sample(N)
        plt.hist(samples, bins=bins, edgecolor='black')
        plt.xlabel('Value')
        plt.ylabel('Frequency')
        plt.title(title)
        plt.savefig(filename)


class BENIGN(NormalDistribution):
    def __init__(self) -> None:
        mean = 25
        std = 10
        max = 50
        min = 0
        super().__init__(mean,std,max,min)

class DRIFTING(NormalDistribution):
    def __init__(self) -> None:
        mean = 100
        std = 30
        max = 150
        min = 25
        super().__init__(mean,std,max,min)

class DRIFTED(NormalDistribution):
    def __init__(self) -> None:
        mean = 20
        std = 3
        max = 30
        min = 10
        super().__init__(mean,std,max,min)

class THREAT(NormalDistribution):
    def __init__(self) -> None:
        mean = 500
        std = 100
        max = 700
        min = 300
        super().__init__(mean,std,max,min)

def is_threat(vec):
    for num in vec[0]:
        if not (300 < num < 700):
            return False
    return True


if __name__ == "__main__":
    print("TESTING DISTRIBUTIONS.PY")
    # N = NormalDistribution(10, 2, 20, 0)
    B = BENIGN()
    B.visualize(100000, 'Benign.png', 100, 'Benign')

    D1 = DRIFTING()
    D1.visualize(100000, 'Drifting.png', 100, 'Drifting')

    # D2 = DRIFTED()
    # D2.visualize(1000, 'Drifted.png', 40, 'Drifted')

    T = THREAT()
    T.visualize(100000, 'Threat.png', 100, 'Threat')