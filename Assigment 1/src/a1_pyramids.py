"""Exercise 6 - Gaussian and Laplacian pyramids (Burt & Adelson, 1983) with OpenCV's REDUCE (pyrDown) and EXPAND (pyrUp)."""
import numpy as np
import cv2

def gaussian_pyramid(img, levels):
    """[G_0, ..., G_levels]: G_0 = img as float32 (values unchanged), G_{i+1} = REDUCE(G_i). Returns a list."""
    assert levels >= 0, f"levels must be non-negative, got {levels}"

    gauss = [img.astype(np.float32)]
    for _ in range(levels):
        gauss.append(cv2.pyrDown(gauss[-1]))
    return gauss

def laplacian_pyramid(gauss):
    """[L_0, ..., L_N] from a Gaussian pyramid: L_i = G_i - EXPAND(G_{i+1}), L_N = copy of G_N.

    All levels float32 (signed). Same length as `gauss`. Works for odd sizes.
    """
    lap = []
    for i in range(len(gauss) - 1):
        h, w = gauss[i].shape[:2]
        expanded = cv2.pyrUp(gauss[i + 1], dstsize=(w, h))
        lap.append(gauss[i] - expanded)
    lap.append(gauss[-1].copy())
    return lap

def reconstruct(lap):
    """Collapse a Laplacian pyramid back to G_0 (float32)."""
    img = lap[-1].copy()
    for level in reversed(lap[:-1]):
        h, w = level.shape[:2]
        img = cv2.pyrUp(img, dstsize=(w, h)) + level
    return img
