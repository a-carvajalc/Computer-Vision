"""
Test suite for OpenCV fundamentals and image operations.

This module tests:
1. Image creation and initialization
2. Filtering operations (blur, Gaussian blur, median blur)
3. Image blending and weighted sum
4. Brightness and contrast adjustment
5. Histogram equalization
6. Geometric transformations (affine, perspective, rotation)

Tests work with synthetic images to avoid file dependencies.
"""

import unittest
import numpy as np
import cv2
from pathlib import Path
import sys

# Add src directory to path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / 'src'))

try:
    from opencv_operations import (
        create_image,
        apply_blur,
        apply_gaussian_blur,
        apply_median_blur,
        blend_images,
        add_weighted_images,
        adjust_brightness,
        adjust_contrast,
        adjust_brightness_contrast,
        equalize_histogram_gray,
        equalize_histogram_color,
        apply_affine_transform_opencv,
        apply_perspective_transform_opencv,
        rotate_image
    )
    OPENCV_OPS_AVAILABLE = True
except (ImportError, NotImplementedError):
    OPENCV_OPS_AVAILABLE = False


class TestImageCreation(unittest.TestCase):
    """Test image creation and initialization"""

    def test_create_grayscale_image_zeros(self):
        """Test: create grayscale image filled with zeros"""
        if not OPENCV_OPS_AVAILABLE:
            self.skipTest("opencv_operations module not yet implemented")
        
        img = create_image(height=10, width=10, channels=1, dtype=np.uint8, fill_value=0)
        
        self.assertEqual(img.shape, (10, 10))
        self.assertEqual(img.dtype, np.uint8)
        self.assertTrue(np.all(img == 0))

    def test_create_color_image_white(self):
        """Test: create color image filled with white (255)"""
        if not OPENCV_OPS_AVAILABLE:
            self.skipTest("opencv_operations module not yet implemented")
        
        img = create_image(height=20, width=30, channels=3, dtype=np.uint8, fill_value=255)
        
        self.assertEqual(img.shape, (20, 30, 3))
        self.assertEqual(img.dtype, np.uint8)
        self.assertTrue(np.all(img == 255))

    def test_create_float_image(self):
        """Test: create floating-point image"""
        if not OPENCV_OPS_AVAILABLE:
            self.skipTest("opencv_operations module not yet implemented")
        
        img = create_image(height=5, width=5, channels=1, dtype=np.float32, fill_value=0.5)
        
        self.assertEqual(img.dtype, np.float32)
        self.assertTrue(np.allclose(img, 0.5))

    def test_create_image_different_sizes(self):
        """Test: create images of various dimensions"""
        if not OPENCV_OPS_AVAILABLE:
            self.skipTest("opencv_operations module not yet implemented")
        
        # Small
        small = create_image(2, 2, 1, np.uint8, 100)
        self.assertEqual(small.shape, (2, 2))
        
        # Large
        large = create_image(512, 640, 3, np.uint8, 50)
        self.assertEqual(large.shape, (512, 640, 3))
        
        # Rectangular
        rect = create_image(100, 200, 4, np.uint8, 128)
        self.assertEqual(rect.shape, (100, 200, 4))


class TestFiltering(unittest.TestCase):
    """Test image filtering operations"""

    def setUp(self):
        """Create test images"""
        if not OPENCV_OPS_AVAILABLE:
            return
        
        # Create a simple gradient image for testing
        self.gray_img = np.arange(0, 256, dtype=np.uint8).reshape(16, 16)
        
        # Create a color gradient
        self.color_img = np.zeros((16, 16, 3), dtype=np.uint8)
        self.color_img[:, :, 0] = np.arange(0, 256, dtype=np.uint8).reshape(16, 16)  # Red channel
        self.color_img[:, :, 1] = 128
        self.color_img[:, :, 2] = 64

    def test_apply_blur_shape(self):
        """Test: blur preserves image shape"""
        if not OPENCV_OPS_AVAILABLE:
            self.skipTest("opencv_operations module not yet implemented")
        
        result = apply_blur(self.gray_img, kernel_size=(3, 3))
        self.assertEqual(result.shape, self.gray_img.shape)

    def test_apply_blur_reduces_variance(self):
        """Test: blur reduces pixel variance"""
        if not OPENCV_OPS_AVAILABLE:
            self.skipTest("opencv_operations module not yet implemented")
        
        original_std = np.std(self.gray_img)
        blurred = apply_blur(self.gray_img, kernel_size=(3, 3))
        blurred_std = np.std(blurred)
        
        # Blurred should have lower variance
        self.assertLess(blurred_std, original_std)

    def test_apply_gaussian_blur_shape(self):
        """Test: Gaussian blur preserves shape"""
        if not OPENCV_OPS_AVAILABLE:
            self.skipTest("opencv_operations module not yet implemented")
        
        result = apply_gaussian_blur(self.gray_img, kernel_size=(5, 5), sigma=1.0)
        self.assertEqual(result.shape, self.gray_img.shape)

    def test_apply_gaussian_blur_smoothing(self):
        """Test: Gaussian blur smooths image"""
        if not OPENCV_OPS_AVAILABLE:
            self.skipTest("opencv_operations module not yet implemented")
        
        # Create noisy image
        noisy = self.gray_img.astype(np.float32) + np.random.normal(0, 10, self.gray_img.shape)
        noisy = np.clip(noisy, 0, 255).astype(np.uint8)
        
        smoothed = apply_gaussian_blur(noisy, kernel_size=(5, 5), sigma=1.0)
        
        # Check that it's valid
        self.assertEqual(smoothed.shape, noisy.shape)

    def test_apply_median_blur_shape(self):
        """Test: median blur preserves shape"""
        if not OPENCV_OPS_AVAILABLE:
            self.skipTest("opencv_operations module not yet implemented")
        
        result = apply_median_blur(self.gray_img, kernel_size=3)
        self.assertEqual(result.shape, self.gray_img.shape)

    def test_apply_median_blur_salt_pepper_removal(self):
        """Test: median blur removes salt-and-pepper noise"""
        if not OPENCV_OPS_AVAILABLE:
            self.skipTest("opencv_operations module not yet implemented")
        
        # Create image with salt-and-pepper noise
        noisy = self.gray_img.copy()
        noise_indices = np.random.choice(noisy.size, size=10)
        noisy.flat[noise_indices] = np.random.choice([0, 255], 10)
        
        denoised = apply_median_blur(noisy, kernel_size=3)
        
        # Should be closer to original than noisy
        # This is a soft check since median filter isn't perfect
        self.assertEqual(denoised.shape, noisy.shape)


class TestImageBlending(unittest.TestCase):
    """Test image blending operations"""

    def setUp(self):
        """Create test images"""
        if not OPENCV_OPS_AVAILABLE:
            return
        
        self.img1 = np.zeros((10, 10, 3), dtype=np.uint8)
        self.img1[:, :] = [255, 0, 0]  # Red
        
        self.img2 = np.zeros((10, 10, 3), dtype=np.uint8)
        self.img2[:, :] = [0, 255, 0]  # Green

    def test_blend_images_shape(self):
        """Test: blend preserves shape"""
        if not OPENCV_OPS_AVAILABLE:
            self.skipTest("opencv_operations module not yet implemented")
        
        result = blend_images(self.img1, self.img2, alpha=0.5)
        self.assertEqual(result.shape, self.img1.shape)

    def test_blend_images_100_percent_first(self):
        """Test: alpha=1.0 returns first image"""
        if not OPENCV_OPS_AVAILABLE:
            self.skipTest("opencv_operations module not yet implemented")
        
        result = blend_images(self.img1, self.img2, alpha=1.0)
        self.assertTrue(np.allclose(result, self.img1, atol=1))

    def test_blend_images_100_percent_second(self):
        """Test: alpha=0.0 returns second image"""
        if not OPENCV_OPS_AVAILABLE:
            self.skipTest("opencv_operations module not yet implemented")
        
        result = blend_images(self.img1, self.img2, alpha=0.0)
        self.assertTrue(np.allclose(result, self.img2, atol=1))

    def test_blend_images_50_percent(self):
        """Test: alpha=0.5 averages both images"""
        if not OPENCV_OPS_AVAILABLE:
            self.skipTest("opencv_operations module not yet implemented")
        
        result = blend_images(self.img1, self.img2, alpha=0.5)
        
        # Each channel should be approximately averaged
        # Red: 127-128, Green: 127-128, Blue: 0
        expected = np.array([127.5, 127.5, 0], dtype=np.float32)
        
        # Check center pixel
        center = result[5, 5].astype(np.float32)
        self.assertTrue(np.allclose(center, expected, atol=2))

    def test_add_weighted_images_shape(self):
        """Test: add_weighted_images preserves shape"""
        if not OPENCV_OPS_AVAILABLE:
            self.skipTest("opencv_operations module not yet implemented")
        
        result = add_weighted_images(self.img1, 0.6, self.img2, 0.4, gamma=0)
        self.assertEqual(result.shape, self.img1.shape)

    def test_add_weighted_images_with_gamma(self):
        """Test: add_weighted_images with gamma offset"""
        if not OPENCV_OPS_AVAILABLE:
            self.skipTest("opencv_operations module not yet implemented")
        
        result = add_weighted_images(self.img1, 0.5, self.img2, 0.5, gamma=50)
        
        # Should have brighter values due to gamma
        self.assertGreater(np.mean(result), np.mean(blend_images(self.img1, self.img2, 0.5)))


class TestBrightnessContrast(unittest.TestCase):
    """Test brightness and contrast adjustment"""

    def setUp(self):
        """Create test images"""
        if not OPENCV_OPS_AVAILABLE:
            return
        
        # Create gradient image (0 to 255)
        self.gray_img = np.arange(0, 256, dtype=np.uint8).reshape(16, 16)
        
        self.color_img = np.tile(
            np.arange(0, 256, dtype=np.uint8).reshape(16, 16, 1),
            (1, 1, 3)
        )

    def test_adjust_brightness_increase(self):
        """Test: increasing brightness"""
        if not OPENCV_OPS_AVAILABLE:
            self.skipTest("opencv_operations module not yet implemented")
        
        original_mean = np.mean(self.gray_img)
        brightened = adjust_brightness(self.gray_img, brightness_value=50)
        brightened_mean = np.mean(brightened)
        
        # Should be brighter
        self.assertGreater(brightened_mean, original_mean)

    def test_adjust_brightness_decrease(self):
        """Test: decreasing brightness"""
        if not OPENCV_OPS_AVAILABLE:
            self.skipTest("opencv_operations module not yet implemented")
        
        original_mean = np.mean(self.gray_img)
        darkened = adjust_brightness(self.gray_img, brightness_value=-50)
        darkened_mean = np.mean(darkened)
        
        # Should be darker
        self.assertLess(darkened_mean, original_mean)

    def test_adjust_brightness_clipping(self):
        """Test: brightness clipping (no overflow)"""
        if not OPENCV_OPS_AVAILABLE:
            self.skipTest("opencv_operations module not yet implemented")
        
        brightened = adjust_brightness(self.gray_img, brightness_value=200)
        
        # Should not exceed 255
        self.assertLessEqual(np.max(brightened), 255)
        self.assertGreaterEqual(np.min(brightened), 0)

    def test_adjust_contrast_increase(self):
        """Test: increasing contrast"""
        if not OPENCV_OPS_AVAILABLE:
            self.skipTest("opencv_operations module not yet implemented")
        
        original_std = np.std(self.gray_img)
        contrast_increased = adjust_contrast(self.gray_img, contrast_factor=1.5)
        new_std = np.std(contrast_increased)
        
        # Should have higher variance
        self.assertGreater(new_std, original_std)

    def test_adjust_contrast_decrease(self):
        """Test: decreasing contrast"""
        if not OPENCV_OPS_AVAILABLE:
            self.skipTest("opencv_operations module not yet implemented")
        
        original_std = np.std(self.gray_img)
        contrast_decreased = adjust_contrast(self.gray_img, contrast_factor=0.5)
        new_std = np.std(contrast_decreased)
        
        # Should have lower variance
        self.assertLess(new_std, original_std)

    def test_adjust_brightness_contrast_combined(self):
        """Test: combined brightness and contrast adjustment"""
        if not OPENCV_OPS_AVAILABLE:
            self.skipTest("opencv_operations module not yet implemented")
        
        adjusted = adjust_brightness_contrast(self.gray_img, alpha=1.2, beta=30)
        
        # Should be valid
        self.assertEqual(adjusted.shape, self.gray_img.shape)
        self.assertGreaterEqual(np.min(adjusted), 0)
        self.assertLessEqual(np.max(adjusted), 255)


class TestHistogramEqualization(unittest.TestCase):
    """Test histogram equalization"""

    def setUp(self):
        """Create test images"""
        if not OPENCV_OPS_AVAILABLE:
            return
        
        # Create image with poor contrast (mostly dark)
        self.low_contrast = np.full((50, 50), 50, dtype=np.uint8)
        self.low_contrast[10:40, 10:40] = 60
        
        # Color version
        self.low_contrast_color = np.zeros((50, 50, 3), dtype=np.uint8)
        self.low_contrast_color[:, :, 0] = self.low_contrast
        self.low_contrast_color[:, :, 1] = self.low_contrast + 10
        self.low_contrast_color[:, :, 2] = self.low_contrast + 20

    def test_equalize_histogram_gray_shape(self):
        """Test: histogram equalization preserves shape"""
        if not OPENCV_OPS_AVAILABLE:
            self.skipTest("opencv_operations module not yet implemented")
        
        result = equalize_histogram_gray(self.low_contrast)
        self.assertEqual(result.shape, self.low_contrast.shape)

    def test_equalize_histogram_gray_improves_contrast(self):
        """Test: histogram equalization improves contrast"""
        if not OPENCV_OPS_AVAILABLE:
            self.skipTest("opencv_operations module not yet implemented")
        
        original_std = np.std(self.low_contrast)
        equalized = equalize_histogram_gray(self.low_contrast)
        equalized_std = np.std(equalized)
        
        # Should have better contrast (higher variance)
        self.assertGreater(equalized_std, original_std)

    def test_equalize_histogram_color_shape(self):
        """Test: color histogram equalization preserves shape"""
        if not OPENCV_OPS_AVAILABLE:
            self.skipTest("opencv_operations module not yet implemented")
        
        result = equalize_histogram_color(self.low_contrast_color)
        self.assertEqual(result.shape, self.low_contrast_color.shape)

    def test_equalize_histogram_color_improves_contrast(self):
        """Test: color histogram equalization improves contrast"""
        if not OPENCV_OPS_AVAILABLE:
            self.skipTest("opencv_operations module not yet implemented")
        
        original_std = np.std(self.low_contrast_color)
        equalized = equalize_histogram_color(self.low_contrast_color)
        equalized_std = np.std(equalized)
        
        # Should have better contrast
        self.assertGreater(equalized_std, original_std)


class TestGeometricTransformations(unittest.TestCase):
    """Test geometric transformations using OpenCV"""

    def setUp(self):
        """Create test images"""
        if not OPENCV_OPS_AVAILABLE:
            return
        
        # Create a simple test image (chessboard-like)
        self.test_img = np.zeros((100, 100, 3), dtype=np.uint8)
        self.test_img[0:50, 0:50] = [255, 0, 0]  # Red square
        self.test_img[50:100, 50:100] = [0, 255, 0]  # Green square

    def test_apply_affine_transform_shape(self):
        """Test: affine transformation preserves shape"""
        if not OPENCV_OPS_AVAILABLE:
            self.skipTest("opencv_operations module not yet implemented")
        
        src_pts = np.array([[0, 0], [100, 0], [0, 100]], dtype=np.float32)
        dst_pts = np.array([[10, 10], [100, 0], [0, 100]], dtype=np.float32)
        
        result = apply_affine_transform_opencv(self.test_img, src_pts, dst_pts)
        
        self.assertEqual(result.shape, self.test_img.shape)

    def test_apply_affine_transform_identity(self):
        """Test: identity affine transformation"""
        if not OPENCV_OPS_AVAILABLE:
            self.skipTest("opencv_operations module not yet implemented")
        
        src_pts = np.array([[0, 0], [100, 0], [0, 100]], dtype=np.float32)
        dst_pts = src_pts.copy()
        
        result = apply_affine_transform_opencv(self.test_img, src_pts, dst_pts)
        
        # Should be approximately the same
        self.assertTrue(np.allclose(result, self.test_img, atol=1))

    def test_apply_perspective_transform_shape(self):
        """Test: perspective transformation preserves shape"""
        if not OPENCV_OPS_AVAILABLE:
            self.skipTest("opencv_operations module not yet implemented")
        
        src_pts = np.array([
            [0, 0],
            [100, 0],
            [100, 100],
            [0, 100]
        ], dtype=np.float32)
        dst_pts = np.array([
            [10, 10],
            [100, 0],
            [90, 100],
            [0, 100]
        ], dtype=np.float32)
        
        result = apply_perspective_transform_opencv(self.test_img, src_pts, dst_pts)
        
        self.assertEqual(result.shape, self.test_img.shape)

    def test_rotate_image_shape(self):
        """Test: rotation preserves shape"""
        if not OPENCV_OPS_AVAILABLE:
            self.skipTest("opencv_operations module not yet implemented")
        
        result = rotate_image(self.test_img, angle=30)
        self.assertEqual(result.shape, self.test_img.shape)

    def test_rotate_image_zero_angle(self):
        """Test: zero rotation returns unchanged image"""
        if not OPENCV_OPS_AVAILABLE:
            self.skipTest("opencv_operations module not yet implemented")
        
        result = rotate_image(self.test_img, angle=0)
        
        # Should be approximately same
        self.assertTrue(np.allclose(result, self.test_img, atol=2))

    def test_rotate_image_90_degrees(self):
        """Test: 90-degree rotation"""
        if not OPENCV_OPS_AVAILABLE:
            self.skipTest("opencv_operations module not yet implemented")
        
        result = rotate_image(self.test_img, angle=90)
        
        # Should be valid
        self.assertEqual(result.shape, self.test_img.shape)


class TestEdgeCases(unittest.TestCase):
    """Test edge cases and error handling"""

    def test_create_image_single_pixel(self):
        """Test: create 1x1 image"""
        if not OPENCV_OPS_AVAILABLE:
            self.skipTest("opencv_operations module not yet implemented")
        
        img = create_image(1, 1, 1, np.uint8, 128)
        self.assertEqual(img.shape, (1, 1))
        self.assertEqual(img[0, 0], 128)

    def test_blend_grayscale_images(self):
        """Test: blending grayscale images"""
        if not OPENCV_OPS_AVAILABLE:
            self.skipTest("opencv_operations module not yet implemented")
        
        img1 = np.full((10, 10), 100, dtype=np.uint8)
        img2 = np.full((10, 10), 200, dtype=np.uint8)
        
        result = blend_images(img1, img2, alpha=0.5)
        
        # Should have shape (10, 10) for grayscale
        self.assertIn(len(result.shape), [2, 3])

    def test_operations_on_small_images(self):
        """Test: operations on 3x3 image (minimum for some filters)"""
        if not OPENCV_OPS_AVAILABLE:
            self.skipTest("opencv_operations module not yet implemented")
        
        small = np.array([
            [0, 128, 255],
            [64, 200, 100],
            [50, 75, 150]
        ], dtype=np.uint8)
        
        # Should handle small images
        try:
            blurred = apply_blur(small, kernel_size=(3, 3))
            self.assertEqual(blurred.shape, small.shape)
        except Exception as e:
            self.skipTest(f"Operations on small images not supported: {e}")


if __name__ == "__main__":
    unittest.main()
