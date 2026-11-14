# CV1 Assignment 1: Thin Lens Equation, Geometric Transformations, and OpenCV Basics

## Overview

This assignment covers three fundamental topics in Computer Vision:

1. **Thin Lens Equation**: Understanding optical properties and image formation
2. **Geometric Transformations**: Translation, rotation, rigid transforms, affine transforms, and projective transforms
3. **OpenCV Fundamentals**: Working with Mat container, image operations (filtering, blending, brightness/contrast, histogram equalization)

## Structure

The project follows a **Test-Driven Development (TDD)** approach:

```
Assignment1/
├── LEARNING_GUIDE.md          (this file - theory and examples)
├── requirements.txt           (Python dependencies)
├── tests/                     (comprehensive test suite)
│   ├── test_thin_lens.py     (thin lens equation tests)
│   ├── test_transformations.py (geometric transforms tests)
│   └── test_opencv_basics.py   (OpenCV operations tests)
├── src/                       (your implementation goes here)
│   ├── __init__.py
│   ├── thin_lens.py          (thin lens functions - TO IMPLEMENT)
│   ├── transformations.py    (geometric transform functions - TO IMPLEMENT)
│   └── opencv_operations.py  (OpenCV operations - TO IMPLEMENT)
└── data/                      (sample images and data)
```

### Workflow

1. **Read the theory** in this guide and the PDF slides
2. **Examine the tests** to understand what needs to be implemented
3. **Run the tests** - they will initially be SKIPPED (marked with `@unittest.skip`)
4. **Implement the methods** in `src/` following the docstring contracts
5. **Verify tests pass** ✓
6. **Move to next section**

### How to Run Tests

**VS Code:**
- Click the Test Explorer icon (flask) → Run Tests

**Command line:**
```bash
cd /home/work/Develop/Master/CV1/Assignment1

# Run all tests
python -m pytest tests/ -v

# Run specific test file
python -m pytest tests/test_thin_lens.py -v

# Run specific test
python -m pytest tests/test_thin_lens.py::TestThinLensEquation::test_focal_length_calculation -v
```

---

## Section 1: Thin Lens Equation

### Theory

The **thin lens equation** relates object distance, image distance, and focal length:

$$\frac{1}{f} = \frac{1}{s_o} + \frac{1}{s_i}$$

Where:
- **f**: focal length (property of the lens)
- **s_o**: object distance (distance from object to lens)
- **s_i**: image distance (distance from lens to image)

#### Key Points

- All distances are measured from the lens center
- **Real object**: s_o > 0
- **Real image**: s_i > 0 (located on opposite side of lens from object)
- **Virtual image**: s_i < 0
- **Converging lens** (convex): f > 0
- **Diverging lens** (concave): f < 0

#### Magnification

The **magnification** is:

$$m = -\frac{s_i}{s_o}$$

- |m| > 1: image is magnified (larger)
- |m| < 1: image is reduced (smaller)
- m < 0: image is inverted
- m > 0: image is upright

### Examples

**Example 1: Real object, converging lens, real image**
- Object distance: s_o = 30 cm
- Focal length: f = 10 cm
- Solve for s_i:
  - 1/f = 1/s_o + 1/s_i
  - 1/10 = 1/30 + 1/s_i
  - 1/s_i = 1/10 - 1/30 = 3/30 - 1/30 = 2/30 = 1/15
  - **s_i = 15 cm** (real image, inverted)
  - **m = -15/30 = -0.5** (reduced, inverted)

**Example 2: Virtual image (diverging lens)**
- Object distance: s_o = 20 cm
- Focal length: f = -10 cm (concave lens)
- Solve for s_i:
  - 1/(-10) = 1/20 + 1/s_i
  - 1/s_i = -1/10 - 1/20 = -2/20 - 1/20 = -3/20
  - **s_i = -20/3 ≈ -6.67 cm** (virtual image)
  - **m = -(-6.67)/20 ≈ 0.333** (reduced, upright)

### Implementation Tasks

**File: `src/thin_lens.py`**

Implement these functions (see tests for exact signatures):

1. `compute_image_distance(focal_length, object_distance)` → image_distance
2. `compute_focal_length(object_distance, image_distance)` → focal_length
3. `compute_object_distance(focal_length, image_distance)` → object_distance
4. `compute_magnification(object_distance, image_distance)` → magnification
5. `lens_type(focal_length)` → "converging" or "diverging"
6. `image_type(image_distance)` → "real" or "virtual"
7. `image_orientation(magnification)` → "upright" or "inverted"

**Expected Test Results:**
- When complete: All tests in `test_thin_lens.py` should pass ✓

---

## Section 2: Geometric Transformations

### Theory

Geometric transformations map 2D/3D coordinates from one space to another.

#### 2.1 Translation

Shifts every point by a fixed vector:

$$\begin{pmatrix} x' \\ y' \end{pmatrix} = \begin{pmatrix} x \\ y \end{pmatrix} + \begin{pmatrix} t_x \\ t_y \end{pmatrix}$$

**In homogeneous coordinates:**

$$\begin{pmatrix} x' \\ y' \\ 1 \end{pmatrix} = \begin{pmatrix} 1 & 0 & t_x \\ 0 & 1 & t_y \\ 0 & 0 & 1 \end{pmatrix} \begin{pmatrix} x \\ y \\ 1 \end{pmatrix}$$

**Degrees of freedom**: 2 (t_x, t_y)

#### 2.2 Rotation (2D)

Rotates points by angle θ around origin:

$$\begin{pmatrix} x' \\ y' \end{pmatrix} = \begin{pmatrix} \cos\theta & -\sin\theta \\ \sin\theta & \cos\theta \end{pmatrix} \begin{pmatrix} x \\ y \end{pmatrix}$$

**Degrees of freedom**: 1 (θ)

#### 2.3 Rotation (3D)

**Around Z-axis:**

$$R_z(\eta) = \begin{pmatrix} \cos\eta & -\sin\eta & 0 \\ \sin\eta & \cos\eta & 0 \\ 0 & 0 & 1 \end{pmatrix}$$

**Around X-axis:**

$$R_x(\phi) = \begin{pmatrix} 1 & 0 & 0 \\ 0 & \cos\phi & -\sin\phi \\ 0 & \sin\phi & \cos\phi \end{pmatrix}$$

**Around Y-axis:**

$$R_y(\theta) = \begin{pmatrix} \cos\theta & 0 & \sin\theta \\ 0 & 1 & 0 \\ -\sin\theta & 0 & \cos\theta \end{pmatrix}$$

**Important**: Rotation matrices do NOT commute! R_x · R_y · R_z ≠ R_z · R_y · R_x

**Degrees of freedom**: 3 (φ, θ, η)

#### 2.4 Rigid Transformation

Combines rotation and translation (no scaling, no shearing):

$$\begin{pmatrix} x' \\ y' \\ z' \end{pmatrix} = R \begin{pmatrix} x \\ y \\ z \end{pmatrix} + \begin{pmatrix} t_x \\ t_y \\ t_z \end{pmatrix}$$

**In homogeneous form:**

$$\begin{pmatrix} x' \\ y' \\ z' \\ 1 \end{pmatrix} = \begin{pmatrix} R & t \\ 0^T & 1 \end{pmatrix} \begin{pmatrix} x \\ y \\ z \\ 1 \end{pmatrix}$$

**Degrees of freedom**: 6 (3 rotation + 3 translation)

#### 2.5 Affine Transformation

Linear transformation + translation:

$$\begin{pmatrix} x' \\ y' \\ 1 \end{pmatrix} = \begin{pmatrix} a_{11} & a_{12} & t_x \\ a_{21} & a_{22} & t_y \\ 0 & 0 & 1 \end{pmatrix} \begin{pmatrix} x \\ y \\ 1 \end{pmatrix}$$

Can represent: rotation, scaling, shearing, translation, and their combinations.

**Degrees of freedom**: 6 (2x2 matrix + 2 translation)

**In OpenCV**: Defined by 3 point pairs (input points → output points)

#### 2.6 Projective Transformation (Homography)

Most general 2D-to-2D linear transformation:

$$\begin{pmatrix} x' \\ y' \\ w' \end{pmatrix} = \begin{pmatrix} h_{11} & h_{12} & h_{13} \\ h_{21} & h_{22} & h_{23} \\ h_{31} & h_{32} & 1 \end{pmatrix} \begin{pmatrix} x \\ y \\ 1 \end{pmatrix}$$

Final coordinates: (x'/w', y'/w')

**Degrees of freedom**: 8 (3x3 matrix with last element fixed)

**In OpenCV**: Defined by 4 point pairs

### Exercises from Lab

**Exercise 1: Translate and Scale**
- Transformation: (x, y) → (1 + 2x, 1 + 2y)
- Question: Express as an affine matrix
- Solution: Combined translation (1, 1) and scale (2, 2)

**Exercise 2: Affine Transformation**
- Transformation: (x, y) → (1 + x + y, 2 + y)
- Question: Compute the affine matrix
- Solution: Translation + Shear

### Implementation Tasks

**File: `src/transformations.py`**

Implement these functions:

1. **Translation**
   - `translation_matrix_2d(tx, ty)` → 3x3 homogeneous matrix
   - `apply_translation_2d(points, tx, ty)` → transformed points

2. **Rotation**
   - `rotation_matrix_2d(angle_rad)` → 2x2 rotation matrix
   - `apply_rotation_2d(points, angle_rad)` → rotated points
   - `rotation_matrix_3d_x(angle_rad)` → 3x3 rotation around X
   - `rotation_matrix_3d_y(angle_rad)` → 3x3 rotation around Y
   - `rotation_matrix_3d_z(angle_rad)` → 3x3 rotation around Z
   - `compose_rotations_3d(phi, theta, eta)` → combined rotation R_x(φ) · R_y(θ) · R_z(η)

3. **Affine Transformation**
   - `affine_matrix_from_points(src_points, dst_points)` → 2x3 affine matrix
   - `apply_affine_2d(points, matrix)` → transformed points

4. **Projective Transformation (Homography)**
   - `homography_matrix_from_points(src_points, dst_points)` → 3x3 homography matrix
   - `apply_homography_2d(points, matrix)` → transformed points (handle normalization)

**Expected Test Results:**
- All tests in `test_transformations.py` should pass ✓

---

## Section 3: OpenCV Fundamentals

### Theory

#### 3.1 Mat Container

OpenCV's `Mat` is the basic n-dimensional array class for images and matrices.

**Key Properties:**
- **data**: Pointer to pixel data (row-major storage)
- **rows, cols**: Dimensions
- **type**: Element type and number of channels (e.g., CV_8UC3)
- **Reference counting**: Automatic memory management
- **Copy semantics**: `=` operator copies header+pointer (shallow), `clone()` copies data (deep)

**Type Format:** `CV_[bits per item][Signed/Unsigned][Type Prefix]C[channels]`

Examples:
- `CV_8UC1`: 8-bit unsigned, 1 channel (grayscale)
- `CV_8UC3`: 8-bit unsigned, 3 channels (BGR color)
- `CV_32FC1`: 32-bit float, 1 channel
- `CV_64FC3`: 64-bit float, 3 channels

#### 3.2 Constructors

```python
import cv2
import numpy as np

# From numpy array
img = cv2.imread("image.jpg")  # Shape: (height, width, 3) for color

# Create empty
empty = cv2.Mat()

# Create with values
img = cv2.Mat((height, width), cv2.CV_8UC3)  # Uninitialized
img = np.zeros((height, width, 3), dtype=np.uint8)  # Black image
img = np.ones((height, width, 3), dtype=np.uint8) * 255  # White image

# Create with specific value
img = np.full((height, width, 3), (0, 0, 255), dtype=np.uint8)  # Red image
```

#### 3.3 Image Filtering

**Blur (Low-pass filter):**
```python
blurred = cv2.blur(src, (kernel_width, kernel_height))
```

**Gaussian Blur:**
```python
blurred = cv2.GaussianBlur(src, (kernel_width, kernel_height), sigma)
```

**Median Blur (salt-and-pepper noise removal):**
```python
denoised = cv2.medianBlur(src, kernel_size)
```

**Edge Detection (Sobel, Canny):**
```python
edges = cv2.Canny(src, threshold1, threshold2)
```

#### 3.4 Image Blending

**Weighted sum of two images (same size and type):**

$$\text{dst} = \alpha \cdot \text{src1} + \beta \cdot \text{src2} + \gamma$$

```python
blended = cv2.addWeighted(src1, alpha, src2, beta, gamma)
```

Example:
```python
img1 = cv2.imread("image1.jpg")
img2 = cv2.imread("image2.jpg")
blended = cv2.addWeighted(img1, 0.7, img2, 0.3, 0)  # 70% img1, 30% img2
```

#### 3.5 Brightness and Contrast Adjustment

**Brightness**: Add constant to all pixels
$$\text{new\_pixel} = \text{pixel} + \text{brightness}$$

**Contrast**: Multiply all pixels by factor
$$\text{new\_pixel} = \text{pixel} \times \text{contrast}$$

**Combined:**
$$\text{new\_pixel} = \alpha \times \text{pixel} + \beta$$

Where:
- **α** (alpha): contrast factor (α > 1 increases contrast, 0 < α < 1 decreases)
- **β** (beta): brightness offset

```python
adjusted = cv2.convertScaleAbs(src, alpha=1.2, beta=30)
```

Or using numpy:
```python
adjusted = np.clip(alpha * src + beta, 0, 255).astype(np.uint8)
```

#### 3.6 Histogram Equalization

Redistributes pixel intensities to improve contrast.

**Grayscale:**
```python
equalized = cv2.equalizeHist(src)  # src must be uint8, single channel
```

**Color Image (RGB):**
```python
# Convert to HSV, equalize V channel, convert back
hsv = cv2.cvtColor(src, cv2.COLOR_BGR2HSV)
h, s, v = cv2.split(hsv)
v_eq = cv2.equalizeHist(v)
hsv_eq = cv2.merge([h, s, v_eq])
result = cv2.cvtColor(hsv_eq, cv2.COLOR_HSV2BGR)
```

#### 3.7 Geometric Transformations

**Affine Transformation:**
```python
# Get transformation matrix from 3 point pairs
src_pts = np.array([[x1, y1], [x2, y2], [x3, y3]], dtype=np.float32)
dst_pts = np.array([[x1', y1'], [x2', y2'], [x3', y3']], dtype=np.float32)
affine_matrix = cv2.getAffineTransform(src_pts, dst_pts)  # Returns 2x3 matrix

# Apply to image
warped = cv2.warpAffine(src, affine_matrix, (width, height))
```

**Projective Transformation (Homography):**
```python
# Get transformation matrix from 4 point pairs
src_pts = np.array([[x1, y1], [x2, y2], [x3, y3], [x4, y4]], dtype=np.float32)
dst_pts = np.array([[x1', y1'], [x2', y2'], [x3', y3'], [x4', y4']], dtype=np.float32)
homography = cv2.getPerspectiveTransform(src_pts, dst_pts)  # Returns 3x3 matrix

# Apply to image
warped = cv2.warpPerspective(src, homography, (width, height))
```

**Rotation:**
```python
center = (width // 2, height // 2)
angle = 30  # degrees
scale = 1.0  # no scaling
rot_matrix = cv2.getRotationMatrix2D(center, angle, scale)  # Returns 2x3 matrix
rotated = cv2.warpAffine(src, rot_matrix, (width, height))
```

### Implementation Tasks

**File: `src/opencv_operations.py`**

Implement these functions:

1. **Image Creation**
   - `create_image(height, width, channels, dtype, fill_value)` → Mat

2. **Filtering**
   - `apply_blur(image, kernel_size)` → blurred image
   - `apply_gaussian_blur(image, kernel_size, sigma)` → blurred image
   - `apply_median_blur(image, kernel_size)` → denoised image

3. **Blending**
   - `blend_images(src1, src2, alpha)` → blended image
   - `add_weighted_images(src1, alpha, src2, beta, gamma)` → weighted sum

4. **Brightness/Contrast**
   - `adjust_brightness(image, brightness_value)` → adjusted image
   - `adjust_contrast(image, contrast_factor)` → adjusted image
   - `adjust_brightness_contrast(image, alpha, beta)` → adjusted image

5. **Histogram Equalization**
   - `equalize_histogram_gray(image)` → equalized grayscale image
   - `equalize_histogram_color(image)` → equalized color image (using HSV)

6. **Geometric Transformations**
   - `apply_affine_transform_opencv(image, src_pts, dst_pts)` → transformed image
   - `apply_perspective_transform_opencv(image, src_pts, dst_pts)` → transformed image
   - `rotate_image(image, angle, center=None, scale=1.0)` → rotated image

**Expected Test Results:**
- All tests in `test_opencv_basics.py` should pass ✓

---

## Section 4: Testing and Validation

### Test Structure

Each test file focuses on one module:

- **test_thin_lens.py**: Optical calculations
- **test_transformations.py**: Matrix operations and coordinate transforms
- **test_opencv_basics.py**: OpenCV image operations

### Running Tests

```bash
# Run all tests
python -m pytest tests/ -v

# Run with coverage
python -m pytest tests/ --cov=src --cov-report=html

# Run specific category
python -m pytest tests/test_thin_lens.py -v
```

### Test Expectations

- Initially: Tests will be SKIPPED (decorator: `@unittest.skip("...")`)
- After implementation: Tests will PASS ✓
- Some tests include numerical tolerances for floating-point comparisons
- Image operation tests may require sample images (provided in `data/`)

---

## Section 5: Summary and Deliverables

### What You Need to Implement

| Module | Functions | Status |
|--------|-----------|--------|
| `thin_lens.py` | 7 functions | TO IMPLEMENT |
| `transformations.py` | 14 functions | TO IMPLEMENT |
| `opencv_operations.py` | 12+ functions | TO IMPLEMENT |

### Quality Checklist

- [ ] All unit tests pass
- [ ] Code follows PEP 8 style guidelines
- [ ] Functions have proper docstrings
- [ ] Edge cases handled (zeros, negative values, etc.)
- [ ] No hardcoded values in functions
- [ ] Type hints for all parameters and returns

### Submission

Include:
1. Completed `src/` directory with all implementations
2. All tests passing
3. Optional: A brief report (1-2 pages) explaining your approach

---

## Appendix: Python/OpenCV Cheat Sheet

### NumPy Basics

```python
import numpy as np

# Create arrays
arr = np.array([[1, 2, 3], [4, 5, 6]])
zeros = np.zeros((3, 3))
ones = np.ones((2, 4))

# Matrix multiplication
result = np.dot(A, B)  # or A @ B
result = np.matmul(A, B)

# Element-wise operations
result = arr * 2  # Multiply by scalar
result = arr / 2
result = arr ** 2  # Power

# Transpose
result = arr.T  # or np.transpose(arr)

# Indexing
element = arr[0, 1]  # Row 0, column 1
row = arr[0, :]  # Entire row 0
col = arr[:, 1]  # Entire column 1

# Reshape
reshaped = arr.reshape((6, 1))

# Concatenate
vstack = np.vstack([arr1, arr2])  # Vertical
hstack = np.hstack([arr1, arr2])  # Horizontal
```

### OpenCV Basics

```python
import cv2
import numpy as np

# Read/write images
img = cv2.imread("image.jpg")  # BGR format
cv2.imwrite("output.jpg", img)

# Get image properties
height, width, channels = img.shape
dtype = img.dtype

# Convert color space
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

# Split/merge channels
b, g, r = cv2.split(img)  # BGR
merged = cv2.merge([b, g, r])

# Resize
resized = cv2.resize(img, (new_width, new_height))

# Crop
roi = img[y1:y2, x1:x2]

# Draw on images
cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)  # Green rectangle
cv2.circle(img, (cx, cy), radius, (255, 0, 0), 2)  # Blue circle
cv2.line(img, (x1, y1), (x2, y2), (0, 0, 255), 2)  # Red line
cv2.putText(img, "Text", (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

# Display
cv2.imshow("Image", img)
cv2.waitKey(0)
cv2.destroyAllWindows()
```

---

## References

- OpenCV Documentation: https://docs.opencv.org/
- NumPy Documentation: https://numpy.org/doc/
- Linear Algebra Tutorials: Khan Academy - Linear Algebra
- Computer Vision Theory: Szeliski "Computer Vision: Algorithms and Applications"

---

**Last Updated:** 2024
**Assignment Version:** CV1 Lab 1
