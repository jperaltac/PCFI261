#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt


def initial_condition(x, center=0.5, width=0.08):
    return np.exp(-((x - center) ** 2) / (2.0 * width ** 2))


def diffuse_1d(nx=201, steps=800, D=1.0, dt=1.0e-5, length=1.0):
    dx = length / (nx - 1)
    r = D * dt / dx**2
    if r > 0.5:
        raise ValueError(f"Esquema inestable: r={r:.3f} > 0.5")

    x = np.linspace(0.0, length, nx)
    u = initial_condition(x)
    snapshots = [u.copy()]

    for n in range(steps):
        u_new = u.copy()
        u_new[1:-1] = u[1:-1] + r * (u[2:] - 2.0 * u[1:-1] + u[:-2])

        # Flujo nulo en los bordes.
        u_new[0] = u_new[1]
        u_new[-1] = u_new[-2]

        u = u_new

        if n in {49, 199, 799}:
            snapshots.append(u.copy())

    return x, snapshots


def main():
    x, snapshots = diffuse_1d()
    labels = ["t0", "t1", "t2", "t3"]

    plt.figure(figsize=(7, 4.5))
    for profile, label in zip(snapshots, labels):
        plt.plot(x, profile, label=label)

    plt.xlabel("x")
    plt.ylabel("u(x,t)")
    plt.title("Difusion 1D: suavizado de un pulso inicial")
    plt.legend()
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()
