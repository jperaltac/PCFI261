NEIGHBORHOODS = [format(k, "03b") for k in range(7, -1, -1)]


def rule_bits(rule):
    return np.array([(rule >> k) & 1 for k in range(8)], dtype=np.uint8)


def step_rule184(row):
    row = np.asarray(row, dtype=np.uint8)
    left = np.roll(row, 1)
    center = row
    right = np.roll(row, -1)
    index = 4 * left + 2 * center + right
    return rule_bits(184)[index]


def evolve_rule184(initial_row, steps):
    row = np.asarray(initial_row, dtype=np.uint8)
    history = np.zeros((steps, len(row)), dtype=np.uint8)
    history[0] = row
    for t in range(steps - 1):
        history[t + 1] = step_rule184(history[t])
    return history


def random_row(size, density, rng_seed=0):
    rng = np.random.default_rng(rng_seed)
    return (rng.random(size) < density).astype(np.uint8)


def traffic_flow(history):
    current = history[:-1]
    movable = (current == 1) & (np.roll(current, -1, axis=1) == 0)
    return movable.mean(axis=1)

####################################################

def plot_history(history, title="Regla 184", ax=None):
    cmap = ListedColormap(["white", "#111827"])
    created = ax is None
    if created:
        fig, ax = plt.subplots(figsize=(9, 4))
    ax.imshow(history, cmap=cmap, interpolation="nearest", aspect="auto", origin="upper")
    ax.set_xlabel("posición")
    ax.set_ylabel("tiempo")
    ax.set_title(title)
    if created:
        plt.tight_layout()
        plt.show()

row = np.zeros(24, dtype=np.uint8)
row[4] = 1
history = evolve_rule184(row, steps=18)
plot_history(history, title="Un auto: representación espacio-tiempo")

####################################################

ROAD_COLOR = "#2f2f2f"
LANE_MARK_COLOR = "#f7f3d7"
CELL_LINE_COLOR = "#616161"
CAR_BODY = "#2563eb"
CAR_ROOF = "#93c5fd"
LIGHT_RED = "#dc2626"
LIGHT_GREEN = "#16a34a"


def draw_road_frame(ax, row, t=0, title="", light_position=None, light_state=None,
                    annotate_cells=False, show_time=True):
    row = np.asarray(row, dtype=np.uint8)
    n = len(row)

    ax.clear()
    ax.set_xlim(0, n)
    ax.set_ylim(0, 1)
    ax.set_aspect('equal')
    ax.axis('off')

    ax.add_patch(Rectangle((0, 0.2), n, 0.6, facecolor=ROAD_COLOR, edgecolor='none'))
    ax.plot([0, n], [0.5, 0.5], color=LANE_MARK_COLOR, linewidth=2, linestyle=(0, (8, 8)), alpha=0.55)

    for i in range(n + 1):
        ax.plot([i, i], [0.2, 0.8], color=CELL_LINE_COLOR, linewidth=0.6, alpha=0.35)

    for i, value in enumerate(row):
        if value == 1:
            x0 = i + 0.08
            ax.add_patch(Rectangle((x0, 0.31), 0.84, 0.22, facecolor=CAR_BODY, edgecolor='black', linewidth=1.0))
            ax.add_patch(Rectangle((x0 + 0.18, 0.46), 0.38, 0.10, facecolor=CAR_ROOF, edgecolor='black', linewidth=0.8))
            ax.add_patch(Circle((x0 + 0.20, 0.29), 0.045, color='black'))
            ax.add_patch(Circle((x0 + 0.64, 0.29), 0.045, color='black'))

    if light_position is not None:
        color = LIGHT_GREEN if light_state else LIGHT_RED
        ax.plot([light_position + 0.5, light_position + 0.5], [0.80, 0.98], color="#444444", linewidth=3)
        ax.add_patch(Rectangle((light_position + 0.37, 0.90), 0.26, 0.08, facecolor="#2b2b2b", edgecolor='black'))
        ax.add_patch(Circle((light_position + 0.50, 0.94), 0.025, color=color))
        ax.text(light_position + 0.5, 1.02, "semáforo", ha='center', va='bottom', fontsize=9)

    if annotate_cells:
        for i in range(n):
            ax.text(i + 0.5, 0.12, str(i), ha='center', va='center', fontsize=7, color="#555555")

    if show_time:
        ax.text(0.02, 1.05, f"t = {t}", transform=ax.transAxes, ha='left', va='bottom', fontsize=11)

    if title:
        ax.set_title(title, pad=16)

#################################################
#################################################
#################################################

def animate_road(history, interval=500, title="Regla 184 animada",
                 light_position=None, light_series=None,
                 annotate_cells=False, figsize=(12, 2.7)):
    history = np.asarray(history, dtype=np.uint8)
    steps, size = history.shape

    fig, ax = plt.subplots(figsize=figsize)

    def update(frame):
        light_state = None
        if light_series is not None:
            light_state = bool(light_series[frame])
        draw_road_frame(
            ax,
            history[frame],
            t=frame,
            title=title,
            light_position=light_position,
            light_state=light_state,
            annotate_cells=annotate_cells,
        )
        return []

    anim = FuncAnimation(fig, update, frames=steps, interval=interval, blit=False, repeat=True)
    plt.close(fig)
    return anim


def display_animation(anim):
    display(HTML(anim.to_jshtml()))


def save_animation_gif(anim, filename="gifs/regla184.gif", fps=3):
    anim.save(filename, writer="pillow", fps=fps)
    print(f"GIF guardado en: {filename}")
    return filename


def save_animation_mp4(anim, filename="videos/regla184.mp4", fps=3):
    try:
        anim.save(filename, writer="ffmpeg", fps=fps)
        print(f"MP4 guardado en: {filename}")
        return filename
    except Exception as exc:
        print("No se pudo guardar MP4 con ffmpeg.")
        print(exc)
        return None

#######################################
#######################################
#######################################

