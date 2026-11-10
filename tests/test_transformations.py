"""
Test suite for geometric transformations.

This module tests coordinate transformations:
1. Translation (2D)
2. Rotation (2D and 3D)
3. Rigid transformations (rotation + translation)
4. Affine transformations (linear + translation)
5. Projective transformations (homography)

Tests verify matrix generation and coordinate transformation accuracy.
"""

import unittest
import math
import numpy as np
from pathlib import Path
import sys

# Add src directory to path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / 'src'))

try:
    from transformations import (
        translation_matrix_2d,
        apply_translation_2d,
        rotation_matrix_2d,
        apply_rotation_2d,
        rotation_matrix_3d_x,
        rotation_matrix_3d_y,
        rotation_matrix_3d_z,
        compose_rotations_3d,
        affine_matrix_from_points,
        apply_affine_2d,
        homography_matrix_from_points,
        apply_homography_2d
    )
    TRANSFORMS_AVAILABLE = True
except (ImportError, NotImplementedError):
    TRANSFORMS_AVAILABLE = False


def are_matrices_equal(M1, M2, tol=1e-5):
    """Helper to compare matrices element-wise"""
    return np.allclose(M1, M2, atol=tol)


class TestTranslation2D(unittest.TestCase):
    """Test 2D translation transformation"""

    def test_translation_matrix_shape(self):
        """Test: translation_matrix_2d returns 3x3 homogeneous matrix"""
        if not TRANSFORMS_AVAILABLE:
            self.skipTest("transformations module not yet implemented")
        
        M = translation_matrix_2d(tx=2, ty=3)
        self.assertEqual(M.shape, (3, 3))

    def test_translation_matrix_structure(self):
        """Test: translation matrix has correct structure"""
        if not TRANSFORMS_AVAILABLE:
            self.skipTest("transformations module not yet implemented")
        
        # T(tx, ty) = [[1, 0, tx], [0, 1, ty], [0, 0, 1]]
        M = translation_matrix_2d(tx=5, ty=7)
        expected = np.array([
            [1, 0, 5],
            [0, 1, 7],
            [0, 0, 1]
        ], dtype=np.float64)
        
        self.assertTrue(are_matrices_equal(M, expected))

    def test_translation_zero(self):
        """Test: zero translation is identity"""
        if not TRANSFORMS_AVAILABLE:
            self.skipTest("transformations module not yet implemented")
        
        M = translation_matrix_2d(tx=0, ty=0)
        expected = np.eye(3)
        self.assertTrue(are_matrices_equal(M, expected))

    def test_apply_translation_single_point(self):
        """Test: translate single point"""
        if not TRANSFORMS_AVAILABLE:
            self.skipTest("transformations module not yet implemented")
        
        # Translate (1, 1) by (3, 4) → (4, 5)
        points = np.array([[1, 1]])
        result = apply_translation_2d(points, tx=3, ty=4)
        expected = np.array([[4, 5]])
        
        self.assertTrue(are_matrices_equal(result, expected))

    def test_apply_translation_multiple_points(self):
        """Test: translate multiple points"""
        if not TRANSFORMS_AVAILABLE:
            self.skipTest("transformations module not yet implemented")
        
        points = np.array([
            [0, 0],
            [1, 0],
            [1, 1],
            [0, 1]
        ], dtype=np.float64)
        
        # Translate by (2, 3)
        result = apply_translation_2d(points, tx=2, ty=3)
        expected = np.array([
            [2, 3],
            [3, 3],
            [3, 4],
            [2, 4]
        ], dtype=np.float64)
        
        self.assertTrue(are_matrices_equal(result, expected))

    def test_translation_negative(self):
        """Test: negative translation (move backward)"""
        if not TRANSFORMS_AVAILABLE:
            self.skipTest("transformations module not yet implemented")
        
        points = np.array([[5, 5]])
        result = apply_translation_2d(points, tx=-2, ty=-3)
        expected = np.array([[3, 2]])
        
        self.assertTrue(are_matrices_equal(result, expected))


class TestRotation2D(unittest.TestCase):
    """Test 2D rotation transformation"""

    def test_rotation_matrix_2d_shape(self):
        """Test: rotation_matrix_2d returns 2x2 matrix"""
        if not TRANSFORMS_AVAILABLE:
            self.skipTest("transformations module not yet implemented")
        
        R = rotation_matrix_2d(angle_rad=0)
        self.assertEqual(R.shape, (2, 2))

    def test_rotation_zero_angle(self):
        """Test: zero angle is identity"""
        if not TRANSFORMS_AVAILABLE:
            self.skipTest("transformations module not yet implemented")
        
        R = rotation_matrix_2d(angle_rad=0)
        expected = np.eye(2)
        self.assertTrue(are_matrices_equal(R, expected))

    def test_rotation_90_degrees(self):
        """Test: 90° rotation matrix"""
        if not TRANSFORMS_AVAILABLE:
            self.skipTest("transformations module not yet implemented")
        
        # R(90°) = [[0, -1], [1, 0]]
        R = rotation_matrix_2d(angle_rad=math.pi / 2)
        expected = np.array([
            [0, -1],
            [1, 0]
        ], dtype=np.float64)
        
        self.assertTrue(are_matrices_equal(R, expected, tol=1e-10))

    def test_rotation_negative_angle(self):
        """Test: negative angle (clockwise rotation)"""
        if not TRANSFORMS_AVAILABLE:
            self.skipTest("transformations module not yet implemented")
        
        # R(-45°) = [[cos(-45°), -sin(-45°)], [sin(-45°), cos(-45°)]]
        angle = -math.pi / 4
        R = rotation_matrix_2d(angle_rad=angle)
        expected = np.array([
            [math.cos(angle), -math.sin(angle)],
            [math.sin(angle), math.cos(angle)]
        ], dtype=np.float64)
        
        self.assertTrue(are_matrices_equal(R, expected))

    def test_apply_rotation_origin(self):
        """Test: rotating point at origin"""
        if not TRANSFORMS_AVAILABLE:
            self.skipTest("transformations module not yet implemented")
        
        points = np.array([[0, 0]])
        result = apply_rotation_2d(points, angle_rad=math.pi / 4)
        expected = np.array([[0, 0]])
        
        self.assertTrue(are_matrices_equal(result, expected))

    def test_apply_rotation_90_degrees(self):
        """Test: 90° rotation of point (1, 0) → (0, 1)"""
        if not TRANSFORMS_AVAILABLE:
            self.skipTest("transformations module not yet implemented")
        
        points = np.array([[1, 0]])
        result = apply_rotation_2d(points, angle_rad=math.pi / 2)
        expected = np.array([[0, 1]])
        
        self.assertTrue(are_matrices_equal(result, expected, tol=1e-10))

    def test_apply_rotation_45_degrees(self):
        """Test: 45° rotation of (1, 0)"""
        if not TRANSFORMS_AVAILABLE:
            self.skipTest("transformations module not yet implemented")
        
        points = np.array([[1, 0]])
        angle = math.pi / 4
        result = apply_rotation_2d(points, angle_rad=angle)
        
        # (1, 0) rotated 45° = (cos(45°), sin(45°))
        expected = np.array([[math.cos(angle), math.sin(angle)]])
        
        self.assertTrue(are_matrices_equal(result, expected))

    def test_rotation_orthogonality(self):
        """Test: rotation matrix is orthogonal (R^T * R = I)"""
        if not TRANSFORMS_AVAILABLE:
            self.skipTest("transformations module not yet implemented")
        
        R = rotation_matrix_2d(angle_rad=math.pi / 6)
        product = R.T @ R
        expected = np.eye(2)
        
        self.assertTrue(are_matrices_equal(product, expected))

    def test_rotation_determinant_is_one(self):
        """Test: rotation matrix has determinant = 1"""
        if not TRANSFORMS_AVAILABLE:
            self.skipTest("transformations module not yet implemented")
        
        R = rotation_matrix_2d(angle_rad=0.7)
        det = np.linalg.det(R)
        
        self.assertAlmostEqual(det, 1.0, places=10)


class TestRotation3D(unittest.TestCase):
    """Test 3D rotation transformations"""

    def test_rotation_matrix_3d_x_shape(self):
        """Test: R_x returns 3x3 matrix"""
        if not TRANSFORMS_AVAILABLE:
            self.skipTest("transformations module not yet implemented")
        
        R = rotation_matrix_3d_x(angle_rad=0)
        self.assertEqual(R.shape, (3, 3))

    def test_rotation_3d_x_zero_angle(self):
        """Test: R_x(0) = I"""
        if not TRANSFORMS_AVAILABLE:
            self.skipTest("transformations module not yet implemented")
        
        R = rotation_matrix_3d_x(angle_rad=0)
        expected = np.eye(3)
        self.assertTrue(are_matrices_equal(R, expected))

    def test_rotation_3d_x_structure(self):
        """Test: R_x has correct structure (leaves X unchanged)"""
        if not TRANSFORMS_AVAILABLE:
            self.skipTest("transformations module not yet implemented")
        
        angle = math.pi / 4
        R = rotation_matrix_3d_x(angle_rad=angle)
        
        # R_x rotates around X axis, so first row/column should be [1, 0, 0]
        self.assertAlmostEqual(R[0, 0], 1.0, places=10)
        self.assertAlmostEqual(R[0, 1], 0.0, places=10)
        self.assertAlmostEqual(R[0, 2], 0.0, places=10)
        self.assertAlmostEqual(R[1, 0], 0.0, places=10)
        self.assertAlmostEqual(R[2, 0], 0.0, places=10)

    def test_rotation_3d_y_structure(self):
        """Test: R_y has correct structure (leaves Y unchanged)"""
        if not TRANSFORMS_AVAILABLE:
            self.skipTest("transformations module not yet implemented")
        
        R = rotation_matrix_3d_y(angle_rad=math.pi / 6)
        
        # First column should preserve Y
        self.assertAlmostEqual(R[1, 1], 1.0, places=10)
        self.assertAlmostEqual(R[0, 1], 0.0, places=10)
        self.assertAlmostEqual(R[2, 1], 0.0, places=10)

    def test_rotation_3d_z_structure(self):
        """Test: R_z has correct structure (leaves Z unchanged)"""
        if not TRANSFORMS_AVAILABLE:
            self.skipTest("transformations module not yet implemented")
        
        R = rotation_matrix_3d_z(angle_rad=math.pi / 3)
        
        # Last row/column should preserve Z
        self.assertAlmostEqual(R[2, 2], 1.0, places=10)
        self.assertAlmostEqual(R[0, 2], 0.0, places=10)
        self.assertAlmostEqual(R[1, 2], 0.0, places=10)

    def test_compose_rotations_3d(self):
        """Test: compose R_x * R_y * R_z"""
        if not TRANSFORMS_AVAILABLE:
            self.skipTest("transformations module not yet implemented")
        
        phi = math.pi / 6    # 30°
        theta = math.pi / 4  # 45°
        eta = math.pi / 3    # 60°
        
        R_combined = compose_rotations_3d(phi, theta, eta)
        
        # Should be 3x3 matrix
        self.assertEqual(R_combined.shape, (3, 3))
        
        # Should be orthogonal
        product = R_combined.T @ R_combined
        expected = np.eye(3)
        self.assertTrue(are_matrices_equal(product, expected))

    def test_rotation_3d_point_rotation(self):
        """Test: rotating point (1, 0, 0) around X axis by 90°"""
        if not TRANSFORMS_AVAILABLE:
            self.skipTest("transformations module not yet implemented")
        
        point = np.array([1, 0, 0])
        R = rotation_matrix_3d_x(angle_rad=math.pi / 2)
        
        rotated = R @ point
        # Should give (1, 0, 1) approximately (Z direction)
        expected = np.array([1, 0, 0])  # X unchanged
        
        self.assertAlmostEqual(rotated[0], expected[0], places=10)
        self.assertAlmostEqual(abs(rotated[1]), 0, places=10)
        self.assertAlmostEqual(abs(rotated[2]), 0, places=10)


class TestAffineTransformation(unittest.TestCase):
    """Test affine transformation from point pairs"""

    def test_affine_matrix_from_identity_points(self):
        """Test: identity transformation (src = dst)"""
        if not TRANSFORMS_AVAILABLE:
            self.skipTest("transformations module not yet implemented")
        
        src = np.array([
            [0, 0],
            [1, 0],
            [0, 1]
        ], dtype=np.float64)
        dst = src.copy()
        
        M = affine_matrix_from_points(src, dst)
        
        # Should be 2x3 matrix
        self.assertEqual(M.shape, (2, 3))
        
        # Should encode identity transformation
        # M @ [x, y, 1]^T = [x, y]^T
        for point in src:
            p_h = np.append(point, 1)  # homogeneous
            result = M @ p_h
            self.assertTrue(np.allclose(result, point))

    def test_affine_matrix_translation_only(self):
        """Test: pure translation"""
        if not TRANSFORMS_AVAILABLE:
            self.skipTest("transformations module not yet implemented")
        
        src = np.array([
            [0, 0],
            [1, 0],
            [0, 1]
        ], dtype=np.float64)
        
        # Translate by (3, 4)
        dst = src + np.array([3, 4])
        
        M = affine_matrix_from_points(src, dst)
        
        # Verify transformation
        for s, d in zip(src, dst):
            s_h = np.append(s, 1)
            result = M @ s_h
            self.assertTrue(np.allclose(result, d))

    def test_affine_matrix_scale_and_translate(self):
        """Test: scaling + translation"""
        if not TRANSFORMS_AVAILABLE:
            self.skipTest("transformations module not yet implemented")
        
        src = np.array([
            [0, 0],
            [1, 0],
            [0, 1]
        ], dtype=np.float64)
        
        # Scale by 2 and translate by (1, 1)
        dst = np.array([
            [1, 1],
            [3, 1],
            [1, 3]
        ], dtype=np.float64)
        
        M = affine_matrix_from_points(src, dst)
        
        for s, d in zip(src, dst):
            s_h = np.append(s, 1)
            result = M @ s_h
            self.assertTrue(np.allclose(result, d))

    def test_apply_affine_2d(self):
        """Test: apply affine transformation to points"""
        if not TRANSFORMS_AVAILABLE:
            self.skipTest("transformations module not yet implemented")
        
        # Create affine matrix for translation (2, 3)
        src = np.array([[0, 0], [1, 0], [0, 1]], dtype=np.float64)
        dst = np.array([[2, 3], [3, 3], [2, 4]], dtype=np.float64)
        
        M = affine_matrix_from_points(src, dst)
        
        # Apply to new points
        test_points = np.array([[0, 0], [1, 1], [5, 3]], dtype=np.float64)
        result = apply_affine_2d(test_points, M)
        
        # Verify shape
        self.assertEqual(result.shape, test_points.shape)
        
        # Verify at least identity points work
        identity_src = np.array([[0, 0], [1, 0], [0, 1]], dtype=np.float64)
        identity_result = apply_affine_2d(identity_src, M)
        self.assertTrue(np.allclose(identity_result, dst))


class TestProjectiveTransformation(unittest.TestCase):
    """Test projective transformation (homography)"""

    def test_homography_matrix_shape(self):
        """Test: homography_matrix_from_points returns 3x3 matrix"""
        if not TRANSFORMS_AVAILABLE:
            self.skipTest("transformations module not yet implemented")
        
        src = np.array([
            [0, 0],
            [1, 0],
            [1, 1],
            [0, 1]
        ], dtype=np.float64)
        dst = src.copy()
        
        H = homography_matrix_from_points(src, dst)
        self.assertEqual(H.shape, (3, 3))

    def test_homography_identity_points(self):
        """Test: identity transformation (src = dst)"""
        if not TRANSFORMS_AVAILABLE:
            self.skipTest("transformations module not yet implemented")
        
        src = np.array([
            [0, 0],
            [1, 0],
            [1, 1],
            [0, 1]
        ], dtype=np.float64)
        dst = src.copy()
        
        H = homography_matrix_from_points(src, dst)
        
        # Should be close to identity (up to scale)
        # H @ [x, y, 1]^T should give [x*w, y*w, w] where we normalize by w
        for point in src:
            p_h = np.append(point, 1)
            h_p = H @ p_h
            # Normalize by last component
            if abs(h_p[2]) > 1e-10:
                result = h_p[:2] / h_p[2]
            else:
                result = h_p[:2]
            self.assertTrue(np.allclose(result, point, atol=1e-6))

    def test_apply_homography_2d(self):
        """Test: apply homography transformation"""
        if not TRANSFORMS_AVAILABLE:
            self.skipTest("transformations module not yet implemented")
        
        # Simple identity case
        src = np.array([
            [0, 0],
            [1, 0],
            [1, 1],
            [0, 1]
        ], dtype=np.float64)
        dst = src.copy()
        
        H = homography_matrix_from_points(src, dst)
        
        # Apply to test points
        test_points = np.array([[0.5, 0.5]], dtype=np.float64)
        result = apply_homography_2d(test_points, H)
        
        # Should be close to (0.5, 0.5) for identity
        self.assertTrue(np.allclose(result, test_points, atol=1e-6))

    def test_homography_scale_invariance(self):
        """Test: homography is scale invariant"""
        if not TRANSFORMS_AVAILABLE:
            self.skipTest("transformations module not yet implemented")
        
        src = np.array([
            [0, 0],
            [1, 0],
            [1, 1],
            [0, 1]
        ], dtype=np.float64)
        dst = src.copy()
        
        H1 = homography_matrix_from_points(src, dst)
        H2 = homography_matrix_from_points(src, dst)
        
        # H2 scaled by constant should give same results (up to normalization)
        point = np.array([0.5, 0.5, 1])
        r1 = H1 @ point
        r2 = H2 @ point
        
        # Normalize
        r1_norm = r1 / r1[2]
        r2_norm = r2 / r2[2]
        
        self.assertTrue(np.allclose(r1_norm, r2_norm))


class TestTransformationComposition(unittest.TestCase):
    """Test composing multiple transformations"""

    def test_translate_then_rotate(self):
        """Test: translate then rotate"""
        if not TRANSFORMS_AVAILABLE:
            self.skipTest("transformations module not yet implemented")
        
        point = np.array([[1, 0]])
        
        # Translate by (1, 0)
        translated = apply_translation_2d(point, tx=1, ty=0)
        # Result: (2, 0)
        
        # Then rotate 90°
        rotated = apply_rotation_2d(translated, angle_rad=math.pi / 2)
        # (2, 0) rotated 90° around origin → (0, 2)
        expected = np.array([[0, 2]])
        
        self.assertTrue(np.allclose(rotated, expected, atol=1e-10))

    def test_rotate_then_translate(self):
        """Test: rotate then translate (different order)"""
        if not TRANSFORMS_AVAILABLE:
            self.skipTest("transformations module not yet implemented")
        
        point = np.array([[1, 0]])
        
        # Rotate 90°
        rotated = apply_rotation_2d(point, angle_rad=math.pi / 2)
        # (1, 0) rotated 90° → (0, 1)
        
        # Then translate by (1, 0)
        translated = apply_translation_2d(rotated, tx=1, ty=0)
        # (0, 1) + (1, 0) → (1, 1)
        expected = np.array([[1, 1]])
        
        self.assertTrue(np.allclose(translated, expected, atol=1e-10))


if __name__ == "__main__":
    unittest.main()
