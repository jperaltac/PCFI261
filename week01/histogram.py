#!/usr/bin/env python3

import matplotlib.pyplot as plt
from random import normalvariate

mu, sigma = 5.0, 2.0

X = [normalvariate(mu, sigma) for i in range(50000)]

plt.hist(X, bins=70)
plt.show()

