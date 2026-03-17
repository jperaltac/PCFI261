import numpy as np


def lennard_jones_force(r_vec, epsilon=1.0, sigma=1.0, r_cut=2.5):
    r = np.linalg.norm(r_vec)
    if r == 0.0 or r > r_cut:
        return np.zeros_like(r_vec)

    sr6 = (sigma / r) ** 6
    sr12 = sr6 * sr6
    prefactor = 24 * epsilon * (2 * sr12 - sr6) / (r * r)
    return prefactor * r_vec


def compute_accelerations(positions, mass=1.0):
    n = len(positions)
    acc = np.zeros_like(positions)

    for i in range(n):
        for j in range(i + 1, n):
            r_ij = positions[j] - positions[i]
            f_ij = lennard_jones_force(r_ij)
            acc[i] += f_ij / mass
            acc[j] -= f_ij / mass

    return acc


def velocity_verlet_step(positions, velocities, acc, dt, mass=1.0):
    pos_new = positions + velocities * dt + 0.5 * acc * dt**2
    acc_new = compute_accelerations(pos_new, mass=mass)
    vel_new = velocities + 0.5 * (acc + acc_new) * dt
    return pos_new, vel_new, acc_new


def initialize_two_particles():
    positions = np.array([
        [0.0, 0.0],
        [1.2, 0.0],
    ], dtype=float)
    velocities = np.array([
        [0.15, 0.00],
        [-0.15, 0.00],
    ], dtype=float)
    return positions, velocities


def detect_contact(positions, radius=0.06):
    r_12 = np.linalg.norm(positions[1] - positions[0])
    return r_12 < 2 * radius


def randomize_directions(velocities, speed=0.2, rng=None):
    if rng is None:
        rng = np.random.default_rng(42)

    for i in range(len(velocities)):
        angle = rng.uniform(0.0, 2 * np.pi)
        velocities[i, 0] = speed * np.cos(angle)
        velocities[i, 1] = speed * np.sin(angle)

    return velocities


def run_demo(n_steps=1000, dt=1e-3):
    positions, velocities = initialize_two_particles()
    acc = compute_accelerations(positions)

    for _ in range(n_steps):
        positions, velocities, acc = velocity_verlet_step(
            positions, velocities, acc, dt
        )

        if detect_contact(positions):
            velocities = randomize_directions(velocities)

    return positions, velocities


if __name__ == "__main__":
    x, v = run_demo()
    print("Posiciones finales:\n", x)
    print("Velocidades finales:\n", v)
