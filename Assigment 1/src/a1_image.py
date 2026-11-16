"""Exercise 3 and helpers used by every other part: loading, resizing, grey conversion and display."""
import math
import numpy as np
import cv2
import matplotlib.pyplot as plt

def load_bgr(path):
    """Read a colour image from disk. Returns an (H, W, 3) uint8 array in BGR order.

    Raises FileNotFoundError when OpenCV cannot read the file (cv2.imread returns None instead of raising).
    """

    image = cv2.imread(str(path), cv2.IMREAD_COLOR)
    if image is None:
        raise FileNotFoundError(f"Could not read image from {path}")

    return image


def resize_to(img, size=(448, 336)):
    """Resize to size = (width, height), with the interpolation suited to shrinking (T3.5)."""

    resized = cv2.resize(img, size, interpolation=cv2.INTER_AREA)
    return resized


def to_gray(img):
    """BGR (H, W, 3) -> grey (H, W) uint8. A 2-D input is returned as a copy."""

    if img.ndim == 2:
        return img.copy()
    else:
        return cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)



def to_uint8(arr):
    """Linear min-max stretch of any 2-D array to 0..255, as uint8. For DISPLAY only.

    A constant array (max == min) returns an array of zeros.
    """
    min_val = np.min(arr)
    max_val = np.max(arr)

    if max_val == min_val:
        return np.zeros_like(arr, dtype=np.uint8)

    out = (arr - min_val) / (max_val - min_val) * 255
    return np.round(out).astype(np.uint8)

def show_images(images, titles=None, cols=3, figsize=None):
    """Draw a grid of images with Matplotlib and RETURN the figure (no plt.show inside).

    images  -- list of arrays: (H, W, 3) BGR uint8, (H, W) uint8 grey, or (H, W) float
    titles  -- list of strings (same length) or None
    cols    -- images per row
    figsize -- (width, height) in inches, or None for an automatic size
    Colour images in true colours, uint8 grey with limits 0..255, float with automatic limits, axes hidden.
    """
    N = len(images)
    rows = math.ceil(N / cols)
    if figsize is None:
        figsize = (cols * 3, rows * 3)
    fig, axs = plt.subplots(rows, cols, figsize=figsize)
    axs = np.array(axs).reshape(-1)        # flatten, even if rows == 1 or cols == 1
    for k, ax in enumerate(axs):
        if k < N:
            img = images[k]
            if img.ndim == 3 and img.shape[2] == 3:
                ax.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
            elif img.ndim == 2 and img.dtype == np.uint8:
                ax.imshow(img, cmap="gray", vmin=0, vmax=255)
            else:
                ax.imshow(img, cmap="gray")
            if titles is not None:
                ax.set_title(titles[k], fontsize=8)
        ax.axis("off")

    return fig


def show_with_opencv(img, window="image"):
    """Show `img` (BGR or grey) in a native OpenCV window until a key is pressed. Returns the key code."""

    key = -1
    if img.dtype != np.uint8:
        print("⚠️ show_with_opencv: the image is not uint8, it will be converted for display")
        img = to_uint8(img)

    cv2.imshow(window, img)
    while True:
        key = cv2.waitKey(100)                                   # wait 0.1 s for a key
        if key != -1:                                            # a key was pressed
            break
        if cv2.getWindowProperty(window, cv2.WND_PROP_VISIBLE) < 1:   # the window was closed with X
            break
    if cv2.getWindowProperty(window, cv2.WND_PROP_VISIBLE) >= 1:     # still open: close it ourselves
        cv2.destroyWindow(window)
    cv2.waitKey(1)                                               # let the window actually close (macOS)
    return key

def save_figure(fig, path, dpi=150):
    """Save a Matplotlib or image figure to disk with the given DPI. The figure is not closed."""
    if isinstance(fig, plt.Figure):
        fig.savefig(str(path), dpi=dpi, bbox_inches="tight")
    elif isinstance(fig, np.ndarray):
        cv2.imwrite(str(path), fig)
    else:
        raise TypeError(f"save_figure: expected plt.Figure or np.ndarray, got {type(fig).__name__}")
