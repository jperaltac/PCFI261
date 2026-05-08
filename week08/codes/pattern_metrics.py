#!/usr/bin/env python3

import numpy as np


def active_fraction(field, threshold=0.25):
    return np.mean(field > threshold)


def spatial_std(field):
    return np.std(field)


def radial_profile(field):
    ny, nx = field.shape
    y, x = np.indices((ny, nx))
    cy, cx = ny // 2, nx // 2
    r = np.sqrt((x - cx) ** 2 + (y - cy) ** 2).astype(int)

    tbin = np.bincount(r.ravel(), field.ravel())
    nr = np.bincount(r.ravel())
    return tbin / np.maximum(nr, 1)


def summarize(field):
    return {
        "mean": float(np.mean(field)),
        "std": float(spatial_std(field)),
        "active_fraction": float(active_fraction(field)),
    }
