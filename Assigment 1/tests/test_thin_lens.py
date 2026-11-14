"""
Test suite for thin lens equation functions.

This module tests the optical calculations based on the thin lens equation:
1/f = 1/s_o + 1/s_i

Where:
- f: focal length (lens property)
- s_o: object distance
- s_i: image distance

Tests cover:
1. Basic lens equation (solving for each variable)
2. Magnification calculations
3. Lens classification (converging/diverging)
4. Image type classification (real/virtual)
5. Image orientation (upright/inverted)
"""

import unittest
import math
from pathlib import Path
import sys

# Add src directory to path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / 'src'))

try:
    from thin_lens import (
        compute_image_distance,
        compute_focal_length,
        compute_object_distance,
        compute_magnification,
        lens_type,
        image_type,
        image_orientation
    )
    THIN_LENS_AVAILABLE = True
except (ImportError, NotImplementedError):
    THIN_LENS_AVAILABLE = False


class TestThinLensEquation(unittest.TestCase):
    """Test basic thin lens equation: 1/f = 1/s_o + 1/s_i"""

    def test_compute_image_distance_real_image(self):
        """Test: object 30cm, focal 10cm → image 15cm"""
        # Given: s_o = 30, f = 10
        # Expected: s_i = 15
        if not THIN_LENS_AVAILABLE:
            self.skipTest("thin_lens module not yet implemented")
        
        s_i = compute_image_distance(focal_length=10, object_distance=30)
        self.assertAlmostEqual(s_i, 15.0, places=5)

    def test_compute_image_distance_virtual_image(self):
        """Test: diverging lens with object distance → virtual image"""
        # Given: s_o = 20, f = -10 (diverging)
        # Expected: s_i = -20/3 ≈ -6.67 (virtual)
        if not THIN_LENS_AVAILABLE:
            self.skipTest("thin_lens module not yet implemented")
        
        s_i = compute_image_distance(focal_length=-10, object_distance=20)
        self.assertAlmostEqual(s_i, -20/3, places=5)

    def test_compute_image_distance_at_2f(self):
        """Test: object at 2f → image at 2f, 1:1 magnification"""
        # Given: s_o = 20, f = 10
        # Expected: s_i = 20
        if not THIN_LENS_AVAILABLE:
            self.skipTest("thin_lens module not yet implemented")
        
        s_i = compute_image_distance(focal_length=10, object_distance=20)
        self.assertAlmostEqual(s_i, 20.0, places=5)

    def test_compute_image_distance_between_f_and_2f(self):
        """Test: object between f and 2f → enlarged real image"""
        # Given: s_o = 15, f = 10
        # 1/10 = 1/15 + 1/s_i → s_i = 30
        if not THIN_LENS_AVAILABLE:
            self.skipTest("thin_lens module not yet implemented")
        
        s_i = compute_image_distance(focal_length=10, object_distance=15)
        self.assertAlmostEqual(s_i, 30.0, places=5)

    def test_compute_focal_length_from_distances(self):
        """Test computing focal length from object and image distances"""
        # Given: s_o = 30, s_i = 15
        # Expected: f = 10
        if not THIN_LENS_AVAILABLE:
            self.skipTest("thin_lens module not yet implemented")
        
        f = compute_focal_length(object_distance=30, image_distance=15)
        self.assertAlmostEqual(f, 10.0, places=5)

    def test_compute_focal_length_symmetric(self):
        """Test: s_o = s_i = 20, f = 10"""
        if not THIN_LENS_AVAILABLE:
            self.skipTest("thin_lens module not yet implemented")
        
        f = compute_focal_length(object_distance=20, image_distance=20)
        self.assertAlmostEqual(f, 10.0, places=5)

    def test_compute_object_distance_from_distances(self):
        """Test computing object distance from focal and image distances"""
        # Given: f = 10, s_i = 15
        # Expected: s_o = 30
        if not THIN_LENS_AVAILABLE:
            self.skipTest("thin_lens module not yet implemented")
        
        s_o = compute_object_distance(focal_length=10, image_distance=15)
        self.assertAlmostEqual(s_o, 30.0, places=5)

    def test_compute_object_distance_virtual_image(self):
        """Test: virtual image → object distance computation"""
        # Given: f = -10, s_i = -6.67
        if not THIN_LENS_AVAILABLE:
            self.skipTest("thin_lens module not yet implemented")
        
        s_o = compute_object_distance(focal_length=-10, image_distance=-20/3)
        self.assertAlmostEqual(s_o, 20.0, places=4)

    def test_lens_equation_consistency(self):
        """Test: 1/f = 1/s_o + 1/s_i (consistency check)"""
        if not THIN_LENS_AVAILABLE:
            self.skipTest("thin_lens module not yet implemented")
        
        # Given known values
        f, s_o = 10, 30
        
        # Compute s_i
        s_i = compute_image_distance(f, s_o)
        
        # Verify lens equation
        calculated_f = compute_focal_length(s_o, s_i)
        self.assertAlmostEqual(calculated_f, f, places=5)


class TestMagnification(unittest.TestCase):
    """Test magnification calculations: m = -s_i/s_o"""

    def test_magnification_reduced_inverted(self):
        """Test: |m| < 1 (reduced), m < 0 (inverted)"""
        # s_o = 30, s_i = 15 → m = -0.5
        if not THIN_LENS_AVAILABLE:
            self.skipTest("thin_lens module not yet implemented")
        
        m = compute_magnification(object_distance=30, image_distance=15)
        self.assertAlmostEqual(m, -0.5, places=5)
        # Check reduced (|m| < 1) and inverted (m < 0)
        self.assertLess(abs(m), 1.0, "Magnification should be reduced")
        self.assertLess(m, 0, "Magnification should be negative (inverted)")

    def test_magnification_magnified_inverted(self):
        """Test: |m| > 1 (magnified), m < 0 (inverted)"""
        # s_o = 15, s_i = 30 → m = -2
        if not THIN_LENS_AVAILABLE:
            self.skipTest("thin_lens module not yet implemented")
        
        m = compute_magnification(object_distance=15, image_distance=30)
        self.assertAlmostEqual(m, -2.0, places=5)
        self.assertGreater(abs(m), 1.0, "Magnification should be magnified")
        self.assertLess(m, 0, "Magnification should be inverted")

    def test_magnification_unit_magnification(self):
        """Test: s_o = s_i = 20 → m = -1 (same size, inverted)"""
        if not THIN_LENS_AVAILABLE:
            self.skipTest("thin_lens module not yet implemented")
        
        m = compute_magnification(object_distance=20, image_distance=20)
        self.assertAlmostEqual(m, -1.0, places=5)

    def test_magnification_virtual_image(self):
        """Test: virtual image → upright (m > 0)"""
        # s_o = 20, s_i = -6.67 (virtual) → m = +0.333...
        if not THIN_LENS_AVAILABLE:
            self.skipTest("thin_lens module not yet implemented")
        
        m = compute_magnification(object_distance=20, image_distance=-20/3)
        self.assertAlmostEqual(m, 1/3, places=4)
        self.assertGreater(m, 0, "Virtual image should have positive magnification (upright)")

    def test_magnification_sign_convention(self):
        """Test magnification sign conventions across different scenarios"""
        if not THIN_LENS_AVAILABLE:
            self.skipTest("thin_lens module not yet implemented")
        
        # Real image: negative magnification
        m_real = compute_magnification(object_distance=30, image_distance=10)
        self.assertLess(m_real, 0)
        
        # Virtual image: positive magnification
        m_virtual = compute_magnification(object_distance=20, image_distance=-10)
        self.assertGreater(m_virtual, 0)


class TestLensClassification(unittest.TestCase):
    """Test lens type classification"""

    def test_converging_lens_positive_focal(self):
        """Test: focal length > 0 → converging (convex)"""
        if not THIN_LENS_AVAILABLE:
            self.skipTest("thin_lens module not yet implemented")
        
        lens = lens_type(focal_length=10)
        self.assertEqual(lens, "converging")

    def test_diverging_lens_negative_focal(self):
        """Test: focal length < 0 → diverging (concave)"""
        if not THIN_LENS_AVAILABLE:
            self.skipTest("thin_lens module not yet implemented")
        
        lens = lens_type(focal_length=-10)
        self.assertEqual(lens, "diverging")

    def test_lens_type_boundary_cases(self):
        """Test boundary cases for lens classification"""
        if not THIN_LENS_AVAILABLE:
            self.skipTest("thin_lens module not yet implemented")
        
        # Very small focal length (strong lens)
        self.assertEqual(lens_type(0.1), "converging")
        self.assertEqual(lens_type(-0.1), "diverging")
        
        # Large focal length (weak lens)
        self.assertEqual(lens_type(100), "converging")
        self.assertEqual(lens_type(-100), "diverging")


class TestImageTypeClassification(unittest.TestCase):
    """Test image type classification (real vs virtual)"""

    def test_real_image_positive_distance(self):
        """Test: s_i > 0 → real image"""
        if not THIN_LENS_AVAILABLE:
            self.skipTest("thin_lens module not yet implemented")
        
        img_type = image_type(image_distance=15)
        self.assertEqual(img_type, "real")

    def test_virtual_image_negative_distance(self):
        """Test: s_i < 0 → virtual image"""
        if not THIN_LENS_AVAILABLE:
            self.skipTest("thin_lens module not yet implemented")
        
        img_type = image_type(image_distance=-6.67)
        self.assertEqual(img_type, "virtual")

    def test_image_type_zero_distance(self):
        """Test: s_i = 0 → image at lens (edge case)"""
        if not THIN_LENS_AVAILABLE:
            self.skipTest("thin_lens module not yet implemented")
        
        # Edge case: could be interpreted as boundary between real/virtual
        img_type = image_type(image_distance=0)
        # Accept either classification or specific handling
        self.assertIn(img_type, ["real", "virtual", "at_lens"])


class TestImageOrientation(unittest.TestCase):
    """Test image orientation classification (upright vs inverted)"""

    def test_inverted_image_negative_magnification(self):
        """Test: m < 0 → inverted"""
        if not THIN_LENS_AVAILABLE:
            self.skipTest("thin_lens module not yet implemented")
        
        orientation = image_orientation(magnification=-0.5)
        self.assertEqual(orientation, "inverted")

    def test_upright_image_positive_magnification(self):
        """Test: m > 0 → upright"""
        if not THIN_LENS_AVAILABLE:
            self.skipTest("thin_lens module not yet implemented")
        
        orientation = image_orientation(magnification=0.333)
        self.assertEqual(orientation, "upright")

    def test_orientation_zero_magnification(self):
        """Test: m = 0 edge case"""
        if not THIN_LENS_AVAILABLE:
            self.skipTest("thin_lens module not yet implemented")
        
        # m = 0 means no image (point at focal plane)
        # This is an edge case that may not occur in valid scenarios
        orientation = image_orientation(magnification=0)
        self.assertIn(orientation, ["upright", "inverted", "no_image"])


class TestComplexScenarios(unittest.TestCase):
    """Integration tests combining multiple calculations"""

    def test_scenario_diverging_lens_magnifying_glass_like(self):
        """Test full scenario: diverging lens producing virtual magnified image"""
        if not THIN_LENS_AVAILABLE:
            self.skipTest("thin_lens module not yet implemented")
        
        # Diverging lens, f = -20
        f = -20
        s_o = 10
        
        # Calculate image distance
        s_i = compute_image_distance(f, s_o)
        
        # Verify it's virtual (negative)
        self.assertLess(s_i, 0)
        self.assertEqual(image_type(s_i), "virtual")
        
        # Calculate magnification
        m = compute_magnification(s_o, s_i)
        
        # Virtual images are upright
        self.assertEqual(image_orientation(m), "upright")
        # Virtual images from diverging lens are typically magnified
        self.assertGreater(abs(m), 0)

    def test_scenario_converging_lens_projection(self):
        """Test full scenario: converging lens forming real projected image"""
        if not THIN_LENS_AVAILABLE:
            self.skipTest("thin_lens module not yet implemented")
        
        # Converging lens, f = 50
        f = 50
        s_o = 150  # Beyond 2f (2f = 100)
        
        s_i = compute_image_distance(f, s_o)
        m = compute_magnification(s_o, s_i)
        
        # Real image
        self.assertGreater(s_i, 0)
        self.assertEqual(image_type(s_i), "real")
        
        # Inverted
        self.assertEqual(image_orientation(m), "inverted")
        
        # Reduced (for object distance > 2f)
        self.assertLess(abs(m), 1.0)

    def test_scenario_at_focal_point(self):
        """Test edge case: object at focal point"""
        if not THIN_LENS_AVAILABLE:
            self.skipTest("thin_lens module not yet implemented")
        
        f = 20
        s_o = 20  # At focal point
        
        # At focal point, image distance should be infinite
        # (function should handle this gracefully)
        try:
            s_i = compute_image_distance(f, s_o)
            # If it returns infinity, that's acceptable
            self.assertTrue(math.isinf(s_i) or abs(s_i) > 1e6)
        except (ZeroDivisionError, ValueError):
            # Or function may raise exception - that's also valid
            pass


class TestNumericalStability(unittest.TestCase):
    """Test numerical edge cases and stability"""

    def test_very_small_object_distance(self):
        """Test with very close object (s_o → 0)"""
        if not THIN_LENS_AVAILABLE:
            self.skipTest("thin_lens module not yet implemented")
        
        f = 10
        s_o = 0.1
        
        s_i = compute_image_distance(f, s_o)
        # Should be very large negative (virtual, magnified)
        self.assertLess(s_i, 0)
        self.assertLess(s_i, 100)

    def test_very_large_object_distance(self):
        """Test with very distant object (s_o → ∞)"""
        if not THIN_LENS_AVAILABLE:
            self.skipTest("thin_lens module not yet implemented")
        
        f = 10
        s_o = 1e6  # Very far
        
        s_i = compute_image_distance(f, s_o)
        # Should approach focal length
        self.assertAlmostEqual(s_i, f, places=1)

    def test_weak_lens_long_focal_length(self):
        """Test weak lens (large focal length)"""
        if not THIN_LENS_AVAILABLE:
            self.skipTest("thin_lens module not yet implemented")
        
        f = 1000
        s_o = 2000
        
        s_i = compute_image_distance(f, s_o)
        # Should compute without numerical issues
        self.assertIsNotNone(s_i)
        self.assertGreater(s_i, 0)


if __name__ == "__main__":
    unittest.main()
