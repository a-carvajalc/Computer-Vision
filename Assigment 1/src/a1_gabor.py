"""Exercise 4 - Gabor filter bank at several orientations, combined by the pixel-wise maximum."""
import numpy as np
import cv2


def gabor_kernel(ksize, sigma, theta, lambd, gamma, psi=0.0):
    """One square Gabor kernel, (ksize, ksize) float32. Angles in radians. psi is explicit (OpenCV's default is pi/2)."""
    return cv2.getGaborKernel((ksize, ksize), sigma, theta, lambd, gamma, psi, ktype=cv2.CV_32F)


def gabor_bank(gray, params, thetas):
    """Filter a grey image with one Gabor kernel per orientation.

    gray   -- (H, W) array, uint8 (0..255, divided by 255) or float (used as is)
    params -- dict with keys ksize, sigma, lambd, gamma, psi
    thetas -- iterable of orientations in radians
    Returns a (len(thetas), H, W) float32 array of SIGNED responses.
    """

    assert params.keys() == {"ksize", "sigma", "lambd", "gamma", "psi"}, f"wrong keys: {set(params)}"
    assert params["ksize"] % 2 == 1, f"ksize must be odd, got {params['ksize']}"

    if gray.dtype == np.uint8:
        gray = gray.astype(np.float32) / 255.0
    else:
        gray = gray.astype(np.float32)


    responses = []
    for theta in thetas:
        kernel = gabor_kernel(**params, theta=theta)
        resp = cv2.filter2D(gray, cv2.CV_32F, kernel)
        responses.append(resp)

    return np.stack(responses)


def combine_max(responses):
    """Pixel-wise maximum over the first axis of a (K, H, W) array. Returns (H, W) float32."""
    resp = np.stack(responses, axis=0) 
    return resp.max(axis=0).astype(np.float32)
