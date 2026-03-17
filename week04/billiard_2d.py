import numpy as np


def reflect_walls(position, velocity, box_size=1.0):
    for axis in (0, 1):
        if position[axis] < 0.0:
            position[axis] = 0.0
            velocity[axis] *= -1.0
        elif position[axis] > box_size:
            position[axis] = box_size
            velocity[axis] *= -1.0
    return position, velocity


def velocity_verlet_particle(position, velocity, acc, dt):
    pos_new = position + velocity * dt + 0.5 * acc * dt**2
    vel_half = velocity + 0.5 * acc * dt
    vel_new = vel_half + 0.5 * acc * dt
    return pos_new, vel_new


def simulate_billiard(n_steps=4000, dt=2e-3, g=9.81):
    box = 1.0
    pos = np.array([[0.2, 0.8], [0.7, 0.4]], dtype=float)
    vel = np.array([[0.7, 0.1], [-0.5, 0.4]], dtype=float)
    acc = np.array([0.0, -g], dtype=float)

    history = np.zeros((n_steps, 2, 2))

    for step in range(n_steps):
        for i in range(2):
            pos[i], vel[i] = velocity_verlet_particle(pos[i], vel[i], acc, dt)
            pos[i], vel[i] = reflect_walls(pos[i], vel[i], box_size=box)

        history[step] = pos

    return history


if __name__ == "__main__":
    traj = simulate_billiard()
    print("Trayectoria calculada con forma:", traj.shape)
