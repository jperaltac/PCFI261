#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt


def count_neighbors(grid):
    neighbors = np.zeros_like(grid, dtype=int)
    for di in (-1, 0, 1):
        for dj in (-1, 0, 1):
            if di == 0 and dj == 0:
                continue
            neighbors += np.roll(np.roll(grid, di, axis=0), dj, axis=1)
    return neighbors


def step(grid):
    neighbors = count_neighbors(grid)
    born = (grid == 0) & (neighbors == 3)
    survive = (grid == 1) & ((neighbors == 2) | (neighbors == 3))
    return (born | survive).astype(int)


def seed_glider(size=60):
    grid = np.zeros((size, size), dtype=int)
    pattern = np.array([[0, 1, 0], [0, 0, 1], [1, 1, 1]], dtype=int)
    grid[2:5, 2:5] = pattern
    return grid


def seed_r_pentomino(size=60):
    grid = np.zeros((size, size), dtype=int)
    cx = size // 2
    cy = size // 2
    pattern = np.array([[0, 1, 1], [1, 1, 0], [0, 1, 0]], dtype=int)
    grid[cx - 1:cx + 2, cy - 1:cy + 2] = pattern
    return grid


def simulate(initial, steps=120):
    history = [initial.copy()]
    grid = initial.copy()
    for _ in range(steps):
        grid = step(grid)
        history.append(grid.copy())
    return history


def plot_snapshots(history, times=(0, 20, 60, 120), outfile="life_evolution.png"):
    fig, axes = plt.subplots(2, 2, figsize=(8, 8))

    for ax, t in zip(axes.flat, times):
        ax.imshow(history[t], cmap="binary", interpolation="nearest")
        ax.set_title(f"t = {t}")
        ax.set_xticks([])
        ax.set_yticks([])

    fig.suptitle("Juego de la Vida de Conway")
    plt.tight_layout()
    plt.savefig(outfile, dpi=160)


if __name__ == "__main__":
    history = simulate(seed_r_pentomino(), steps=120)
    plot_snapshots(history)
