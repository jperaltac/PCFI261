#!/usr/bin/env python3

import matplotlib.pyplot as plt
import numpy as np

mu = 2.0
sigma = 1.5
N = 100000

x = np.linspace(mu - 4 * sigma, mu + 4 * sigma, 400)
pdf = np.exp(-0.5 * ((x - mu) / sigma) ** 2) / (np.sqrt(2 * np.pi) * sigma)

data = np.random.normal(mu, sigma, N)

plt.hist(data, bins=50, density=True, alpha=0.6, label="Muestras")
plt.plot(x, pdf, "r-", linewidth=2, label="Densidad teórica")
plt.xlabel("x")
plt.ylabel("densidad")
plt.legend()
plt.show()
