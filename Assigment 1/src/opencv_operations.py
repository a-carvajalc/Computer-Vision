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


def create_image(height, width, channels, dtype, fill_value):
    if channels == 1:
        return np.full((height, width), fill_value, dtype=dtype)
    else:
        return np.full((height, width, channels), fill_value, dtype=dtype)


def apply_blur(image, kernel_size):
    return cv2.blur(image, kernel_size)


def apply_gaussian_blur(image, kernel_size, sigma):
    return cv2.GaussianBlur(image, kernel_size, sigma)


def apply_median_blur(image, kernel_size):
    return cv2.medianBlur(image, kernel_size)


def blend_images(src1, src2, alpha):
    return cv2.addWeighted(src1, alpha, src2, 1 - alpha, 0)


def add_weighted_images(src1, alpha, src2, beta, gamma):
    return cv2.addWeighted(src1, alpha, src2, beta, gamma)


def adjust_brightness(image, brightness_value):
    return cv2.convertScaleAbs(image, alpha=1, beta=brightness_value)


def adjust_contrast(image, contrast_factor):
    return cv2.convertScaleAbs(image, alpha=contrast_factor, beta=0)


def adjust_brightness_contrast(image, alpha, beta):
    return cv2.convertScaleAbs(image, alpha=alpha, beta=beta)


def equalize_histogram_gray(image):
    return cv2.equalizeHist(image)


def equalize_histogram_color(image):
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    hsv[:, :, 2] = cv2.equalizeHist(hsv[:, :, 2])
    return cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)


def apply_affine_transform_opencv(image, src_pts, dst_pts):
    M = cv2.getAffineTransform(src_pts, dst_pts)
    rows, cols = image.shape[:2]
    return cv2.warpAffine(image, M, (cols, rows))


def apply_perspective_transform_opencv(image, src_pts, dst_pts):
    M = cv2.getPerspectiveTransform(src_pts, dst_pts)
    rows, cols = image.shape[:2]
    return cv2.warpPerspective(image, M, (cols, rows))


def rotate_image(image, angle, center=None, scale=1.0):
    if center is None:
        center = (image.shape[1] // 2, image.shape[0] // 2)
    M = cv2.getRotationMatrix2D(center, angle, scale)
    rows, cols = image.shape[:2]
    return cv2.warpAffine(image, M, (cols, rows))
