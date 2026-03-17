import numpy as np


def euler_step(x, v, a, dt):
    """Un paso de Euler para una partícula 2D."""
    x_next = x + v * dt
    v_next = v + a * dt
    return x_next, v_next


def run_example(n_steps=2000, dt=1e-3):
    x = np.array([0.2, 0.7], dtype=float)
    v = np.array([0.9, -0.3], dtype=float)
    a = np.array([0.0, 0.0], dtype=float)

    traj = np.zeros((n_steps, 2))
    for i in range(n_steps):
        x, v = euler_step(x, v, a, dt)
        traj[i] = x

    return traj


if __name__ == "__main__":
    trajectory = run_example()
    print("Última posición:", trajectory[-1])
