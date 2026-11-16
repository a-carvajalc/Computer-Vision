"""Exercise 5 - Canny edges (with explicit Gaussian smoothing) and tools to compare them with the Gabor output."""
import numpy as np
import cv2


def canny_edges(gray, low, high, blur_ksize=5, blur_sigma=1.4, l2=True):
    """Gaussian smoothing (skipped if blur_ksize == 0), then Canny.

    gray       -- (H, W) uint8
    low, high  -- hysteresis thresholds on the gradient magnitude
    blur_ksize -- odd kernel size of the Gaussian smoothing, 0 = no smoothing
    blur_sigma -- standard deviation of the smoothing
    l2         -- True: L2 gradient magnitude
    Returns an (H, W) uint8 edge map with values 0 and 255.
    """
    assert gray.ndim == 2 and gray.dtype == np.uint8, f"gray must be 2-D uint8, got {gray.shape} {gray.dtype}"
    assert low >= 0 and high >= 0, f"thresholds must be non-negative, got {low} {high}"
    assert blur_ksize ==0 or blur_ksize % 2 == 1, f"blur_ksize must be odd or 0, got {blur_ksize}"

    if blur_ksize > 0:
        gray = cv2.GaussianBlur(gray, (blur_ksize, blur_ksize), blur_sigma)   #Must apply the blur first, otherwise the Canny edge detection will be too sensitive to noise
    return cv2.Canny(gray, low, high, L2gradient=l2)                          

def auto_thresholds(gray, s=0.33):
    """Median heuristic: low = int(max(0, (1-s) m)), high = int(min(255, (1+s) m)), m = median grey. Returns (low, high)."""

    m = np.median(gray) 
    low = int(max(0, (1 - s) * m))
    high = int(min(255, (1 + s) * m))
    return low, high


def overlay_edges(img, edges, color=(0, 0, 255)):
    """New BGR image: img (BGR, or grey converted to BGR) with `color` where edges > 0. The input is not modified."""
    if img.ndim == 2: # Gray image, convert to BGR
        img_bgr = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
    else:
        img_bgr = img.copy()

    img_bgr[edges > 0] = color  #apply the mask on the image

    return img_bgr
