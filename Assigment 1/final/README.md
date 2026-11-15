# CV1 Assignment 1: Computer Vision Fundamentals

**Computer Vision I** · Máster en Intelixencia Artificial · Universidade da Coruña · 2026/27
**Group:** Guilherme Guerra Martins · Maira Alejandra Carvajal Chaparro

This folder holds the code and the image behind our report for Assignment 1. Exercises 1 and 2 are theoretical (proof and derivation), so they are only in the report. Exercises 3 to 6 are implemented as small Python modules in `helpers/`, and they all run on our own photo in `data/`.

## 📋 Contents

| Exercise | Topic | Where |
| --- | --- | --- |
| 1 | A rigid change of coordinates preserves distances and angles | Report (proof) |
| 2 | Rotation matrices about the x-axis and the y-axis | Report (derivation) |
| 3 | Photo of a cluttered scene, resized to 448×336, read and shown with OpenCV | `helpers/a1_image.py` |
| 4 | Gabor filter at 4 orientations, combined by the per-pixel maximum, 3 parameter sets | `helpers/a1_gabor.py` |
| 5 | Canny edge detector, compared with the Gabor result | `helpers/a1_canny.py` |
| 6 | Gaussian and Laplacian pyramids | `helpers/a1_pyramids.py` |

## 🗂️ Structure

```
Assignment 1/
├── README.md                 # This file
├── data/
│   ├── my_scene.png          # Original photo, 5712×4284 pixels
│   └── scene_448x336.png     # The resized scene used by Exercises 3 to 6
└── helpers/
    ├── a1_image.py           # Ex. 3 + shared tools: load, resize, grey, display, save
    ├── a1_gabor.py           # Ex. 4: Gabor kernel, filter bank, max combination
    ├── a1_canny.py           # Ex. 5: Canny with explicit blur, threshold heuristic, overlay
    └── a1_pyramids.py        # Ex. 6: Gaussian pyramid, Laplacian pyramid, reconstruction
```

## ⚡ Quick start

### 1. Install the dependencies

Python 3.10 or newer, with:

```bash
pip install opencv-python numpy matplotlib
```

Use `opencv-python`, not `opencv-python-headless`: the headless build has no `cv2.imshow`.

### 2. Import the modules

Run Python from this folder and add `helpers/` to the import path:

```python
import sys
sys.path.insert(0, "helpers")

import numpy as np
import cv2
import a1_image as im
import a1_gabor as gab
import a1_canny as can
import a1_pyramids as pyr

SCENE = im.load_bgr("data/scene_448x336.png")   # (336, 448, 3) uint8, BGR
GRAY = im.to_gray(SCENE)                        # (336, 448) uint8
```

### 3. Run each exercise

**Exercise 3: resize, read and show**

```python
photo = im.load_bgr("data/my_scene.png")             # (4284, 5712, 3)
scene = im.resize_to(photo, (448, 336))              # (width, height), INTER_AREA
cv2.imwrite("data/scene_448x336.png", scene)
im.show_with_opencv(scene, "Scene")                  # closes on a key or with the X
```

**Exercise 4: Gabor at 4 orientations, three parameter sets**

```python
THETAS = np.deg2rad([0, 45, 90, 135])
SET_1 = {"ksize": 13, "sigma": 2.0, "lambd": 4.0,  "gamma": 0.5, "psi": 0.0}   # fine
SET_2 = {"ksize": 25, "sigma": 4.0, "lambd": 8.0,  "gamma": 0.5, "psi": 0.0}   # medium
SET_3 = {"ksize": 49, "sigma": 8.0, "lambd": 16.0, "gamma": 0.5, "psi": 0.0}   # coarse

GABOR_MAX = gab.combine_max(np.abs(gab.gabor_bank(GRAY, SET_1, THETAS)))     # (336, 448) float32
```

**Exercise 5: Canny, and the comparison with Gabor**

```python
print(can.auto_thresholds(GRAY))                         # median heuristic: (99, 196) on our scene
CANNY = can.canny_edges(GRAY, 10, 120)                   # blur 5×5, sigma 1.4, then Canny
overlay = can.overlay_edges(im.to_uint8(GABOR_MAX), CANNY)   # Canny edges in red over Gabor
```

**Exercise 6: Gaussian and Laplacian pyramids**

```python
G = pyr.gaussian_pyramid(GRAY, 4)      # G_0 ... G_4, from 336×448 to 21×28
L = pyr.laplacian_pyramid(G)           # L_0 ... L_4, signed float32, L_4 = G_4
rebuilt = pyr.reconstruct(L)           # equals GRAY up to rounding
```

**Showing and saving results**

```python
fig = im.show_images([GRAY, im.to_uint8(GABOR_MAX), CANNY], ["Scene", "Gabor max", "Canny"], cols=3)
im.save_figure(fig, "canny_vs_gabor.png", dpi=200)
```

## 🧩 Function reference

| Module | Function | What it does |
| --- | --- | --- |
| `a1_image` | `load_bgr(path)` | Reads a colour image as (H, W, 3) uint8 BGR, and raises `FileNotFoundError` when OpenCV cannot read it |
| | `resize_to(img, size=(448, 336))` | Resizes to `(width, height)` with `INTER_AREA` (averaging, no aliasing when shrinking) |
| | `to_gray(img)` | BGR to grey (H, W) uint8, a grey input is returned as a copy |
| | `to_uint8(arr)` | Min-max stretch of any array to 0–255, for display only |
| | `show_images(images, titles, cols, figsize)` | Grid of images with Matplotlib (BGR shown in true colours), returns the figure |
| | `show_with_opencv(img, window)` | Native OpenCV window until a key is pressed or the window is closed |
| | `save_figure(fig, path, dpi)` | Saves a Matplotlib figure or an image array |
| `a1_gabor` | `gabor_kernel(ksize, sigma, theta, lambd, gamma, psi)` | One square float32 Gabor kernel (angles in radians) |
| | `gabor_bank(gray, params, thetas)` | One signed response per orientation, (K, H, W) float32 (uint8 input divided by 255) |
| | `combine_max(responses)` | Per-pixel maximum over the orientations, (H, W) float32 |
| `a1_canny` | `canny_edges(gray, low, high, blur_ksize=5, blur_sigma=1.4, l2=True)` | Gaussian blur (skipped if `blur_ksize=0`), then Canny, 0/255 uint8 edge map |
| | `auto_thresholds(gray, s=0.33)` | Starting thresholds from the median grey level: ((1−s)·m, (1+s)·m) |
| | `overlay_edges(img, edges, color=(0, 0, 255))` | New BGR image with the edges painted in `color`, the input is not modified |
| `a1_pyramids` | `gaussian_pyramid(img, levels)` | G_0 = image as float32, each next level = `cv2.pyrDown` (blur, then every other pixel) |
| | `laplacian_pyramid(gauss)` | L_i = G_i − `pyrUp`(G_i+1) at the size of G_i, top level = copy of G_N |
| | `reconstruct(lap)` | Rebuilds G_0 from the top level down: G_i = `pyrUp`(G_i+1) + L_i |

## 📝 Notes

- **BGR order.** OpenCV reads and writes images as BGR. Only `show_images` converts to RGB, and only for display.
- **Sizes.** NumPy shapes are (height, width), while OpenCV sizes (`resize`, `pyrUp`'s `dstsize`) are (width, height).
- **Types.** Gabor responses and Laplacian levels are signed, so they are float32. Convert with `im.to_uint8` only to display them.
- **Canny thresholds** apply to the gradient magnitude, which goes above 255. On our scene we used (10, 120) after a 5×5 blur with σ = 1.4.
- **Odd sizes.** `laplacian_pyramid` and `reconstruct` always pass `dstsize`, so they work for any image size.
