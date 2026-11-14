"""
OpenCV Image Operations

This module implements common image processing operations:
- Image creation and initialization
- Filtering (blur, Gaussian blur, median blur)
- Image blending and weighted operations
- Brightness and contrast adjustment
- Histogram equalization
- Geometric transformations using OpenCV

All functions work with numpy arrays in uint8 or float32 format.
"""

import numpy as np
import cv2

# TODO: Implement the following functions


def create_image(height, width, channels, dtype, fill_value):
    """
    Create an image (numpy array) initialized with a specific value.
    
    Args:
        height (int): Number of rows
        width (int): Number of columns
        channels (int): Number of channels
            - 1: grayscale
            - 3: BGR color
            - 4: BGRA with alpha
        dtype: NumPy data type (np.uint8, np.float32, np.float64)
        fill_value (int/float): Initial value for all pixels
    
    Returns:
        np.ndarray: Image array of shape (height, width) for single channel
                   or (height, width, channels) for multichannel
    
    Example:
        >>> img = create_image(10, 10, 3, np.uint8, 255)
        >>> img.shape
        (10, 10, 3)
        >>> np.all(img == 255)
        True
    """
    if channels == 1:
        return np.full((height, width), fill_value, dtype=dtype)
    else:
        return np.full((height, width, channels), fill_value, dtype=dtype)


def apply_blur(image, kernel_size):
    """
    Apply a simple box blur (averaging filter) to the image.
    
    Args:
        image (np.ndarray): Input image
        kernel_size (tuple): Kernel dimensions (height, width)
            - Must be odd numbers: (3, 3), (5, 5), (7, 7), etc.
    
    Returns:
        np.ndarray: Blurred image, same shape as input
    
    Uses cv2.blur() internally.
    
    Example:
        >>> img = np.random.randint(0, 256, (50, 50, 3), dtype=np.uint8)
        >>> blurred = apply_blur(img, (5, 5))
        >>> blurred.shape
        (50, 50, 3)
    """
    return cv2.blur(image, kernel_size)


def apply_gaussian_blur(image, kernel_size, sigma):
    """
    Apply Gaussian blur to the image.
    
    Gaussian blur is smoother than box blur and better for removing noise.
    
    Args:
        image (np.ndarray): Input image
        kernel_size (tuple): Kernel dimensions (height, width)
            - Must be odd numbers
        sigma (float): Standard deviation for Gaussian kernel
            - Larger σ = more blur
    
    Returns:
        np.ndarray: Blurred image, same shape as input
    
    Uses cv2.GaussianBlur() internally.
    
    Example:
        >>> img = np.random.randint(0, 256, (100, 100, 3), dtype=np.uint8)
        >>> blurred = apply_gaussian_blur(img, (5, 5), 1.0)
    """
    return cv2.GaussianBlur(image, kernel_size, sigma)


def apply_median_blur(image, kernel_size):
    """
    Apply median blur to the image.
    
    Excellent for removing salt-and-pepper noise while preserving edges.
    
    Args:
        image (np.ndarray): Input image
        kernel_size (int): Kernel size (must be odd: 3, 5, 7, etc.)
    
    Returns:
        np.ndarray: Denoised image, same shape as input
    
    Uses cv2.medianBlur() internally.
    
    Example:
        >>> img = np.random.randint(0, 256, (50, 50, 3), dtype=np.uint8)
        >>> denoised = apply_median_blur(img, 5)
    """
    return cv2.medianBlur(image, kernel_size)


def blend_images(src1, src2, alpha):
    """
    Blend two images with linear interpolation.
    
    Args:
        src1 (np.ndarray): First image
        src2 (np.ndarray): Second image (must be same shape and type as src1)
        alpha (float): Blending factor in range [0, 1]
            - alpha = 1.0: 100% src1
            - alpha = 0.0: 100% src2
            - alpha = 0.5: 50% blend
    
    Returns:
        np.ndarray: Blended image
            dst = alpha * src1 + (1 - alpha) * src2
    
    Example:
        >>> img1 = np.full((10, 10, 3), [255, 0, 0], dtype=np.uint8)  # Red
        >>> img2 = np.full((10, 10, 3), [0, 255, 0], dtype=np.uint8)  # Green
        >>> blended = blend_images(img1, img2, 0.5)
        >>> blended[0, 0]  # Should be roughly [127, 127, 0] (yellow)
    """
    return cv2.addWeighted(src1, alpha, src2, 1 - alpha, 0)


def add_weighted_images(src1, alpha, src2, beta, gamma):
    """
    Add two images with weights and optional constant.
    
    Args:
        src1 (np.ndarray): First image
        alpha (float): Weight for src1
        src2 (np.ndarray): Second image
        beta (float): Weight for src2
        gamma (float): Constant offset added to result
    
    Returns:
        np.ndarray: Weighted sum image
            dst = alpha * src1 + beta * src2 + gamma
    
    Note: Values are clipped to valid range for the dtype.
    
    Uses cv2.addWeighted() internally.
    
    Example:
        >>> img1 = np.full((10, 10, 3), 100, dtype=np.uint8)
        >>> img2 = np.full((10, 10, 3), 50, dtype=np.uint8)
        >>> result = add_weighted_images(img1, 0.6, img2, 0.4, 10)
        >>> # result ≈ 0.6*100 + 0.4*50 + 10 = 90
    """
    return cv2.addWeighted(src1, alpha, src2, beta, gamma)


def adjust_brightness(image, brightness_value):
    """
    Adjust image brightness by adding a constant to all pixels.
    
    Args:
        image (np.ndarray): Input image
        brightness_value (int/float): Brightness offset
            - Positive: brighter
            - Negative: darker
    
    Returns:
        np.ndarray: Brightness-adjusted image
            result = image + brightness_value
    
    Note: Results are clipped to valid range [0, 255] for uint8 images.
    
    Example:
        >>> img = np.full((10, 10, 3), 100, dtype=np.uint8)
        >>> bright = adjust_brightness(img, 50)
        >>> bright[0, 0]
        150
        
        >>> dark = adjust_brightness(img, -50)
        >>> dark[0, 0]
        50
    """
    return cv2.convertScaleAbs(image, alpha=1, beta=brightness_value)


def adjust_contrast(image, contrast_factor):
    """
    Adjust image contrast by multiplying pixel values.
    
    Args:
        image (np.ndarray): Input image
        contrast_factor (float): Contrast multiplier
            - > 1.0: increase contrast
            - < 1.0: decrease contrast (flatten)
            - = 1.0: no change
    
    Returns:
        np.ndarray: Contrast-adjusted image
            result = image * contrast_factor
    
    Note: Multiplication is applied from the midpoint (128 for uint8).
    Better to adjust from center: new_pixel = (pixel - 128) * factor + 128
    
    Example:
        >>> img = np.arange(0, 256, dtype=np.uint8).reshape(16, 16)
        >>> more_contrast = adjust_contrast(img, 1.5)
        >>> less_contrast = adjust_contrast(img, 0.5)
    """
    return cv2.convertScaleAbs(image, alpha=contrast_factor, beta=0)


def adjust_brightness_contrast(image, alpha, beta):
    """
    Adjust both brightness and contrast.
    
    Args:
        image (np.ndarray): Input image
        alpha (float): Contrast factor (like contrast_factor above)
        beta (int/float): Brightness offset (like brightness_value above)
    
    Returns:
        np.ndarray: Adjusted image
            result = alpha * image + beta
    
    Note: Values are clipped to valid range for the dtype.
    
    Example:
        >>> img = np.full((10, 10, 3), 100, dtype=np.uint8)
        >>> adjusted = adjust_brightness_contrast(img, 1.2, 30)
        >>> # Each pixel: 1.2 * 100 + 30 = 150
    """
    return cv2.convertScaleAbs(image, alpha=alpha, beta=beta)


def equalize_histogram_gray(image):
    """
    Apply histogram equalization to a grayscale image.
    
    Redistributes pixel intensities to spread them across the full range [0, 255],
    improving contrast.
    
    Args:
        image (np.ndarray): Grayscale input image (single channel, uint8)
    
    Returns:
        np.ndarray: Equalized grayscale image
    
    Uses cv2.equalizeHist() internally.
    
    Note: Input must be uint8 and single-channel.
    
    Example:
        >>> img = np.full((50, 50), 100, dtype=np.uint8)
        >>> equalized = equalize_histogram_gray(img)
        >>> # Output will have better contrast
    """
    return cv2.equalizeHist(image)


def equalize_histogram_color(image):
    """
    Apply histogram equalization to a color image.
    
    For color images, it's better to equalize only the intensity/value channel
    to avoid color shifts. This function:
    1. Converts BGR to HSV
    2. Equalizes the V (value/brightness) channel
    3. Converts back to BGR
    
    Args:
        image (np.ndarray): Color input image (3-channel BGR, uint8)
    
    Returns:
        np.ndarray: Equalized color image
    
    Example:
        >>> img = np.random.randint(0, 256, (100, 100, 3), dtype=np.uint8)
        >>> equalized = equalize_histogram_color(img)
        >>> equalized.shape
        (100, 100, 3)
    """
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    hsv[:, :, 2] = cv2.equalizeHist(hsv[:, :, 2])
    return cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)


def apply_affine_transform_opencv(image, src_pts, dst_pts):
    """
    Apply affine transformation to an image using point correspondences.
    
    Args:
        image (np.ndarray): Input image
        src_pts (np.ndarray): Source points, shape (3, 2) and dtype float32
        dst_pts (np.ndarray): Destination points, shape (3, 2) and dtype float32
    
    Returns:
        np.ndarray: Transformed image, same size as input
    
    Process:
        1. Compute affine matrix from point pairs: cv2.getAffineTransform()
        2. Apply transformation to image: cv2.warpAffine()
    
    Example:
        >>> img = np.ones((100, 100, 3), dtype=np.uint8)
        >>> src = np.array([[0, 0], [100, 0], [0, 100]], dtype=np.float32)
        >>> dst = np.array([[10, 10], [100, 0], [0, 100]], dtype=np.float32)
        >>> result = apply_affine_transform_opencv(img, src, dst)
        >>> result.shape
        (100, 100, 3)
    """
    M = cv2.getAffineTransform(src_pts, dst_pts)
    rows, cols = image.shape[:2]
    return cv2.warpAffine(image, M, (cols, rows))


def apply_perspective_transform_opencv(image, src_pts, dst_pts):
    """
    Apply projective (perspective) transformation to an image using point correspondences.
    
    Args:
        image (np.ndarray): Input image
        src_pts (np.ndarray): Source points, shape (4, 2) and dtype float32
        dst_pts (np.ndarray): Destination points, shape (4, 2) and dtype float32
    
    Returns:
        np.ndarray: Transformed image, same size as input
    
    Process:
        1. Compute homography matrix: cv2.getPerspectiveTransform()
        2. Apply transformation to image: cv2.warpPerspective()
    
    Example:
        >>> img = np.ones((100, 100, 3), dtype=np.uint8)
        >>> src = np.array([[0, 0], [100, 0], [100, 100], [0, 100]], dtype=np.float32)
        >>> dst = np.array([[10, 10], [90, 20], [100, 90], [20, 80]], dtype=np.float32)
        >>> result = apply_perspective_transform_opencv(img, src, dst)
        >>> result.shape
        (100, 100, 3)
    """
    M = cv2.getPerspectiveTransform(src_pts, dst_pts)
    rows, cols = image.shape[:2]
    return cv2.warpPerspective(image, M, (cols, rows))


def rotate_image(image, angle, center=None, scale=1.0):
    """
    Rotate an image by a given angle.
    
    Args:
        image (np.ndarray): Input image
        angle (float): Rotation angle in degrees
            - Positive: counterclockwise
            - Negative: clockwise
        center (tuple): Rotation center (cx, cy)
            - If None: uses image center
        scale (float): Scaling factor (1.0 = no scaling)
    
    Returns:
        np.ndarray: Rotated image, same size as input
    
    Process:
        1. Get rotation matrix: cv2.getRotationMatrix2D()
        2. Apply to image: cv2.warpAffine()
    
    Example:
        >>> img = np.ones((100, 100, 3), dtype=np.uint8)
        >>> rotated = rotate_image(img, angle=30)
        >>> rotated.shape
        (100, 100, 3)
    """
    if center is None:
        center = (image.shape[1] // 2, image.shape[0] // 2)
    M = cv2.getRotationMatrix2D(center, angle, scale)
    rows, cols = image.shape[:2]
    return cv2.warpAffine(image, M, (cols, rows))
