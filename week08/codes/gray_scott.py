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


def initialize(n=160, noise=0.02, seed=7):
    rng = np.random.default_rng(seed)

    U = np.ones((n, n), dtype=float)
    V = np.zeros((n, n), dtype=float)

    s = 12
    c = n // 2
    U[c - s : c + s, c - s : c + s] = 0.50
    V[c - s : c + s, c - s : c + s] = 0.25

    U += noise * rng.standard_normal((n, n))
    V += noise * rng.standard_normal((n, n))

    return np.clip(U, 0.0, 1.2), np.clip(V, 0.0, 1.2)


def gray_scott(
    n=160,
    steps=4000,
    Du=0.16,
    Dv=0.08,
    F=0.035,
    k=0.062,
    dt=1.0,
):
    U, V = initialize(n=n)

    for _ in range(steps):
        Lu = laplacian(U)
        Lv = laplacian(V)
        reaction = U * V * V

        U += dt * (Du * Lu - reaction + F * (1.0 - U))
        V += dt * (Dv * Lv + reaction - (F + k) * V)

        U = np.clip(U, 0.0, 1.5)
        V = np.clip(V, 0.0, 1.5)

    return U, V


def main():
    U, V = gray_scott()

    fig, axes = plt.subplots(1, 2, figsize=(9, 4))
    im0 = axes[0].imshow(U, cmap="viridis", origin="lower")
    axes[0].set_title("Campo U")
    axes[0].set_xticks([])
    axes[0].set_yticks([])
    fig.colorbar(im0, ax=axes[0], fraction=0.046)

    im1 = axes[1].imshow(V, cmap="magma", origin="lower")
    axes[1].set_title("Campo V")
    axes[1].set_xticks([])
    axes[1].set_yticks([])
    fig.colorbar(im1, ax=axes[1], fraction=0.046)

    fig.suptitle("Modelo de Gray-Scott: formacion de patrones")
    fig.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()
