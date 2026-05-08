#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt


def laplacian(Z):
    return (
        np.roll(Z, 1, axis=0)
        + np.roll(Z, -1, axis=0)
        + np.roll(Z, 1, axis=1)
        + np.roll(Z, -1, axis=1)
        - 4.0 * Z
    )


def diffuse_2d(n=120, steps=400, D=0.25, dt=0.1, dx=1.0):
    r = D * dt / dx**2
    if r > 0.25:
        raise ValueError(f"Esquema potencialmente inestable en 2D: r={r:.3f} > 0.25")

    Z = np.zeros((n, n), dtype=float)
    Z[n // 2 - 8 : n // 2 + 8, n // 2 - 8 : n // 2 + 8] = 1.0

    for _ in range(steps):
        Z += r * laplacian(Z)

    return Z


def main():
    Z = diffuse_2d()
    plt.figure(figsize=(5.5, 5.0))
    plt.imshow(Z, cmap="inferno", origin="lower")
    plt.colorbar(label="u(x,y)")
    plt.title("Difusion 2D desde una mancha inicial")
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()
