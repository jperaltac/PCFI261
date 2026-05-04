#!/usr/bin/env python3

import matplotlib.pyplot as plt
from elementary_ca import evolve


RULES = [30, 90, 110, 184]


def main(outfile="eca_gallery.png"):
    fig, axes = plt.subplots(2, 2, figsize=(10, 8))

    for ax, rule in zip(axes.flat, RULES):
        grid = evolve(rule, size=151, steps=100, seed="single")
        ax.imshow(grid, cmap="binary", interpolation="nearest", origin="upper")
        ax.set_title(f"Regla {rule}")
        ax.set_xticks([])
        ax.set_yticks([])

    fig.suptitle("Comparación de reglas elementales")
    plt.tight_layout()
    plt.savefig(outfile, dpi=160)


if __name__ == "__main__":
    main()
