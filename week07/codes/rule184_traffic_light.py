#!/usr/bin/env python3

import numpy as np
from rule184_traffic import random_row, draw_road_frame


def light_is_green(t, cycle=10, green=4, offset=0):
    phase = (t + offset) % cycle
    return phase < green


def step_rule184_with_light(row, light_position, t, cycle=10, green=4, offset=0):
    row = np.asarray(row, dtype=int)
    next_empty = np.roll(row, -1) == 0
    can_move = (row == 1) & next_empty

    blocked_destinations = np.zeros(len(row), dtype=bool)
    if not light_is_green(t, cycle=cycle, green=green, offset=offset):
        blocked_destinations[light_position] = True

    destination_is_blocked = np.roll(blocked_destinations, 1)
    can_move &= ~destination_is_blocked

    next_row = row.copy()
    next_row[can_move] = 0
    next_row[np.roll(can_move, 1)] = 1
    return next_row, can_move


def evolve_rule184_with_light(initial_row, steps, light_position, cycle=10, green=4, offset=0):
    row = np.asarray(initial_row, dtype=int)
    history = np.zeros((steps, len(row)), dtype=int)
    signal = np.zeros(steps, dtype=int)
    moved_fraction = np.zeros(steps - 1)

    history[0] = row
    signal[0] = int(light_is_green(0, cycle=cycle, green=green, offset=offset))

    for t in range(steps - 1):
        row, moved = step_rule184_with_light(row, light_position, t, cycle=cycle, green=green, offset=offset)
        history[t + 1] = row
        moved_fraction[t] = moved.mean()
        signal[t + 1] = int(light_is_green(t + 1, cycle=cycle, green=green, offset=offset))

    return history, signal, moved_fraction


def snapshot_with_light(row, light_position, light_state, title=""):
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(figsize=(10, 2.6))
    draw_road_frame(ax, row, title=title)
    color = "#16a34a" if light_state else "#dc2626"
    ax.plot([light_position + 0.5, light_position + 0.5], [0.80, 0.98], color="#444444", linewidth=3)
    ax.scatter([light_position + 0.5], [0.94], s=120, c=color, edgecolors="black", zorder=5)
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    row = random_row(size=36, density=0.35, seed=5)
    history, signal, moved = evolve_rule184_with_light(row, steps=24, light_position=20, cycle=10, green=4)
    snapshot_with_light(history[8], light_position=20, light_state=signal[8], title="Regla 184 con semaforo")
    print("Flujo promedio:", moved.mean())
