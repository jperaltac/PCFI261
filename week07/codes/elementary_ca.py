#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt


def rule_bits(rule):
    return np.array([(rule >> k) & 1 for k in range(8)], dtype=int)


def evolve(rule, size=151, steps=100, seed="single", p=0.5):
    bits = rule_bits(rule)
    grid = np.zeros((steps, size), dtype=int)

    if seed == "single":
        grid[0, size // 2] = 1
    elif seed == "random":
        rng = np.random.default_rng(7)
        grid[0] = (rng.random(size) < p).astype(int)
    else:
        raise ValueError("seed debe ser 'single' o 'random'")

    for t in range(steps - 1):
        left = np.roll(grid[t], 1)
        center = grid[t]
        right = np.roll(grid[t], -1)
        index = 4 * left + 2 * center + right
        grid[t + 1] = bits[index]

    return grid


def plot(rule=30, size=151, steps=100, seed="single", outfile="eca_rule30.png"):
    grid = evolve(rule, size=size, steps=steps, seed=seed)
    plt.figure(figsize=(7, 5))
    plt.imshow(grid, cmap="binary", interpolation="nearest", origin="upper")
    plt.title(f"Autómata celular elemental, regla {rule}")
    plt.xlabel("Sitio")
    plt.ylabel("Tiempo")
    plt.tight_layout()
    plt.savefig(outfile, dpi=160)


if __name__ == "__main__":
    plot()
