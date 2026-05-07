#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.colors import ListedColormap
from matplotlib.patches import Rectangle, Circle


def rule_bits(rule):
    return np.array([(rule >> k) & 1 for k in range(8)], dtype=int)


def step_rule184(row):
    row = np.asarray(row, dtype=int)
    left = np.roll(row, 1)
    center = row
    right = np.roll(row, -1)
    index = 4 * left + 2 * center + right
    return rule_bits(184)[index]


def evolve_rule184(initial_row, steps=80):
    row = np.asarray(initial_row, dtype=int)
    history = np.zeros((steps, len(row)), dtype=int)
    history[0] = row
    for t in range(steps - 1):
        history[t + 1] = step_rule184(history[t])
    return history


def random_row(size=60, density=0.3, seed=7):
    rng = np.random.default_rng(seed)
    return (rng.random(size) < density).astype(int)


def traffic_flow(history):
    current = history[:-1]
    movable = (current == 1) & (np.roll(current, -1, axis=1) == 0)
    return movable.mean(axis=1)


def plot_history(history, outfile="rule184_spacetime.png"):
    cmap = ListedColormap(["white", "black"])
    plt.figure(figsize=(7, 4))
    plt.imshow(history, cmap=cmap, interpolation="nearest", origin="upper", aspect="auto")
    plt.title("Regla 184: diagrama espacio-tiempo")
    plt.xlabel("posicion")
    plt.ylabel("tiempo")
    plt.tight_layout()
    plt.savefig(outfile, dpi=160)


def draw_road_frame(ax, row, title=""):
    n = len(row)
    ax.clear()
    ax.set_xlim(0, n)
    ax.set_ylim(0, 1)
    ax.set_aspect("equal")
    ax.axis("off")

    ax.add_patch(Rectangle((0, 0.2), n, 0.6, facecolor="#30343f", edgecolor="none"))
    for i in range(n + 1):
        ax.plot([i, i], [0.2, 0.8], color="gray", linewidth=0.5, alpha=0.4)
    ax.plot([0, n], [0.5, 0.5], color="#f3f1cf", linewidth=2, linestyle=(0, (8, 8)))

    for i, value in enumerate(row):
        if value == 1:
            x0 = i + 0.08
            ax.add_patch(Rectangle((x0, 0.31), 0.84, 0.22, facecolor="#2563eb", edgecolor="black", linewidth=0.8))
            ax.add_patch(Rectangle((x0 + 0.18, 0.46), 0.38, 0.10, facecolor="#93c5fd", edgecolor="black", linewidth=0.6))
            ax.add_patch(Circle((x0 + 0.20, 0.29), 0.04, color="black"))
            ax.add_patch(Circle((x0 + 0.64, 0.29), 0.04, color="black"))

    ax.set_title(title)


def animate_road(history, outfile="rule184_traffic.mp4"):
    fig, ax = plt.subplots(figsize=(10, 2.4))

    def update(frame):
        draw_road_frame(ax, history[frame], title=f"Regla 184, t = {frame}")
        return []

    anim = FuncAnimation(fig, update, frames=len(history), interval=300, blit=False)
    anim.save(outfile, fps=4)


if __name__ == "__main__":
    history = evolve_rule184(random_row(size=60, density=0.35), steps=80)
    plot_history(history)
