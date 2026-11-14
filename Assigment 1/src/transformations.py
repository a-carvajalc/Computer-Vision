"""
Geometric Transformations

This module implements 2D and 3D geometric transformations:
- Translation
- Rotation (2D and 3D around different axes)
- Affine transformations (linear + translation)
- Projective transformations (homography)

All transformation matrices are in homogeneous coordinates where applicable.
"""

import numpy as np

# TODO: Implement the following functions


def translation_matrix_2d(tx, ty):
    """
    Create a 2D translation matrix in homogeneous coordinates.
    
    Args:
        tx (float): Translation in x direction
        ty (float): Translation in y direction
    
    Returns:
        np.ndarray: 3x3 translation matrix
            [[1, 0, tx],
             [0, 1, ty],
             [0, 0, 1]]
    
    Example:
        >>> T = translation_matrix_2d(2, 3)
        >>> point = np.array([1, 1, 1])
        >>> result = T @ point
        >>> print(result[:2])
        [3, 4]  # Point translated by (2, 3)
    """
    tx = float(tx)
    ty = float(ty)
    return np.array([
        [1, 0, tx],
        [0, 1, ty],
        [0, 0, 1]
    ])
  


def apply_translation_2d(points, tx, ty):
    """
    Apply 2D translation to points.
    
    Args:
        points (np.ndarray): Array of shape (N, 2) containing points (x, y)
        tx (float): Translation in x
        ty (float): Translation in y
    
    Returns:
        np.ndarray: Translated points, same shape as input
    
    Example:
        >>> points = np.array([[0, 0], [1, 1]])
        >>> result = apply_translation_2d(points, 2, 3)
        >>> print(result)
        [[2, 3],
         [3, 4]]
    """
    points = np.asarray(points, dtype=float)
    translated_points = points + np.array([tx, ty])
    return translated_points


def rotation_matrix_2d(angle_rad):
    """
    Create a 2D rotation matrix.
    
    Args:
        angle_rad (float): Rotation angle in radians (counterclockwise positive)
    
    Returns:
        np.ndarray: 2x2 rotation matrix
            [[cos(θ), -sin(θ)],
             [sin(θ),  cos(θ)]]
    
    Properties:
        - R^T * R = I (orthogonal)
        - det(R) = 1
        - R(θ) * R(-θ) = I (invertible)
    
    Example:
        >>> R = rotation_matrix_2d(np.pi / 2)  # 90° rotation
        >>> point = np.array([1, 0])
        >>> result = R @ point
        >>> print(np.round(result, 10))
        [0, 1]  # Point rotated 90° counterclockwise
    """
    angle_rad = float(angle_rad)
    c = np.cos(angle_rad)
    s = np.sin(angle_rad)
    return np.array([
        [c, -s],
        [s,  c]
    ])


def apply_rotation_2d(points, angle_rad):
    """
    Apply 2D rotation to points around the origin.
    
    Args:
        points (np.ndarray): Array of shape (N, 2) containing points (x, y)
        angle_rad (float): Rotation angle in radians
    
    Returns:
        np.ndarray: Rotated points, same shape as input
    
    Example:
        >>> points = np.array([[1, 0], [0, 1]])
        >>> result = apply_rotation_2d(points, np.pi / 4)  # 45° rotation
        >>> print(np.round(result, 10))
        [[√2/2, √2/2],
         [-√2/2, √2/2]]
    """
    points = np.asarray(points, dtype=float)
    R = rotation_matrix_2d(angle_rad)
    rotated_points = points @ R.T
    return rotated_points


def rotation_matrix_3d_x(angle_rad):
    """
    Create a 3D rotation matrix around the X-axis.
    
    Args:
        angle_rad (float): Rotation angle in radians around X-axis
    
    Returns:
        np.ndarray: 3x3 rotation matrix
            [[1,      0,       0],
             [0, cos(θ), -sin(θ)],
             [0, sin(θ),  cos(θ)]]
    
    Properties:
        - Leaves X coordinate unchanged
        - Rotates in YZ plane
    
    Example:
        >>> R = rotation_matrix_3d_x(np.pi / 2)
        >>> point = np.array([1, 0, 0])
        >>> result = R @ point
        >>> print(np.round(result, 10))
        [1, 0, 0]  # X unchanged
    """
    angle_rad = float(angle_rad)
    c = np.cos(angle_rad)
    s = np.sin(angle_rad)
    return np.array([
        [1, 0, 0],
        [0, c, -s],
        [0, s,  c]
    ])


def rotation_matrix_3d_y(angle_rad):
    """
    Create a 3D rotation matrix around the Y-axis.
    
    Args:
        angle_rad (float): Rotation angle in radians around Y-axis
    
    Returns:
        np.ndarray: 3x3 rotation matrix
            [[cos(θ),  0, sin(θ)],
             [0,       1, 0],
             [-sin(θ), 0, cos(θ)]]
    
    Properties:
        - Leaves Y coordinate unchanged
        - Rotates in XZ plane
    """
    angle_rad = float(angle_rad)
    c = np.cos(angle_rad)
    s = np.sin(angle_rad)
    return np.array([
        [c, 0, s],
        [0, 1, 0],
        [-s, 0, c]
    ])


def rotation_matrix_3d_z(angle_rad):
    """
    Create a 3D rotation matrix around the Z-axis.
    
    Args:
        angle_rad (float): Rotation angle in radians around Z-axis
    
    Returns:
        np.ndarray: 3x3 rotation matrix
            [[cos(θ), -sin(θ), 0],
             [sin(θ),  cos(θ), 0],
             [0,       0,      1]]
    
    Properties:
        - Leaves Z coordinate unchanged
        - Rotates in XY plane
    """
    angle_rad = float(angle_rad)
    c = np.cos(angle_rad)
    s = np.sin(angle_rad)
    return np.array([
        [c, -s, 0],
        [s,  c, 0],
        [0,  0, 1]
    ])


def compose_rotations_3d(phi, theta, eta):
    """
    Compose three rotation matrices: R_x(φ) * R_y(θ) * R_z(η)
    
    Note: Rotation matrices do NOT commute!
    R_x * R_y * R_z ≠ R_z * R_y * R_x in general
    
    Args:
        phi (float): Rotation angle around X-axis in radians
        theta (float): Rotation angle around Y-axis in radians
        eta (float): Rotation angle around Z-axis in radians
    
    Returns:
        np.ndarray: 3x3 composed rotation matrix
    
    Example:
        >>> R = compose_rotations_3d(np.pi/6, np.pi/4, np.pi/3)
        >>> # R is orthogonal: R^T * R = I
        >>> assert np.allclose(R.T @ R, np.eye(3))
    """
    R_x = rotation_matrix_3d_x(phi)
    R_y = rotation_matrix_3d_y(theta)
    R_z = rotation_matrix_3d_z(eta)
    return R_x @ R_y @ R_z


def affine_matrix_from_points(src_points, dst_points):
    """
    Compute affine transformation matrix from point correspondences.
    
    An affine transformation has 6 degrees of freedom and can represent
    rotation, scaling, shearing, and translation in any combination.
    
    Args:
        src_points (np.ndarray): Source points, shape (3, 2)
            - Must be exactly 3 non-collinear points
        dst_points (np.ndarray): Destination points, shape (3, 2)
            - Correspondence to src_points
    
    Returns:
        np.ndarray: 2x3 affine transformation matrix M such that:
            dst = M @ [src_x, src_y, 1]^T
    
    Raises:
        ValueError: If points are collinear or invalid shape
    
    Example:
        >>> src = np.array([[0, 0], [1, 0], [0, 1]], dtype=np.float32)
        >>> dst = np.array([[1, 1], [3, 1], [1, 3]], dtype=np.float32)
        >>> M = affine_matrix_from_points(src, dst)
        >>> # M encodes scale by 2 and translate by (1, 1)
    """
    src_points = np.asarray(src_points, dtype=float)
    dst_points = np.asarray(dst_points, dtype=float)

    if src_points.shape != (3, 2) or dst_points.shape != (3, 2):
        raise ValueError("src_points and dst_points must be of shape (3, 2)")

    # Construct the augmented matrix for affine transformation
    A = np.zeros((6, 6))
    b = np.zeros(6)
    for i in range(3):
        x, y = src_points[i]
        u, v = dst_points[i]
        A[2*i] = [x, y, 1, 0, 0, 0]
        A[2*i+1] = [0, 0, 0, x, y, 1]
        b[2*i] = u
        b[2*i+1] = v

    try:
        params = np.linalg.solve(A, b)
    except np.linalg.LinAlgError:
        raise ValueError("Points are collinear or invalid")

    M = params.reshape(2, 3)
    return M


def apply_affine_2d(points, affine_matrix):
    """
    Apply affine transformation to points.
    
    Args:
        points (np.ndarray): Points to transform, shape (N, 2)
        affine_matrix (np.ndarray): 2x3 affine transformation matrix
    
    Returns:
        np.ndarray: Transformed points, shape (N, 2)
    
    Example:
        >>> M = np.array([[2, 0, 1], [0, 2, 1]])  # Scale 2x and translate (1,1)
        >>> points = np.array([[0, 0], [1, 1]])
        >>> result = apply_affine_2d(points, M)
        >>> print(result)
        [[1, 1],
         [3, 3]]
    """
    points = np.asarray(points, dtype=float)
    if affine_matrix.shape != (2, 3):
        raise ValueError("Must be of shape (2, 3)")
    N = points.shape[0]
    points_h = np.hstack([points, np.ones((N, 1))])
    transformed_points = (affine_matrix @ points_h.T).T
    return transformed_points


def homography_matrix_from_points(src_points, dst_points):
    """
    Compute projective transformation matrix (homography) from point correspondences.
    
    A homography has 8 degrees of freedom and is the most general 2D-to-2D
    linear transformation. It includes affine plus perspective effects.
    
    Args:
        src_points (np.ndarray): Source points, shape (4, 2)
            - Must be exactly 4 points in general position (no 3 collinear)
        dst_points (np.ndarray): Destination points, shape (4, 2)
            - Correspondence to src_points
    
    Returns:
        np.ndarray: 3x3 homography matrix H such that:
            dst = normalize(H @ [src_x, src_y, 1]^T)
        where normalize divides by the last component
    
    Raises:
        ValueError: If points are invalid or degenerate
    
    Example:
        >>> src = np.array([[0,0], [1,0], [1,1], [0,1]], dtype=np.float32)
        >>> dst = np.array([[0,0], [1,0], [1,1], [0,1]], dtype=np.float32)
        >>> H = homography_matrix_from_points(src, dst)
        >>> # H is (up to scale) the identity matrix
    """
    src_points = np.asarray(src_points, dtype=float)
    dst_points = np.asarray(dst_points, dtype=float)

    if src_points.shape != (4, 2) or dst_points.shape != (4, 2):
        raise ValueError("src_points and dst_points must be of shape (4, 2)")

    A = []
    for i in range(4):
        x, y = src_points[i]
        u, v = dst_points[i]
        A.append([-x, -y, -1, 0, 0, 0, u*x, u*y, u])
        A.append([0, 0, 0, -x, -y, -1, v*x, v*y, v])
    A = np.array(A)
    U, S, Vt = np.linalg.svd(A)
    H = Vt[-1].reshape(3, 3)
    if H[2, 2] == 0:
        raise ValueError("Degenerate configuration") # This occurs when the points do not define a valid homography
    H /= H[2, 2]
    return H


def apply_homography_2d(points, homography_matrix):
    """
    Apply projective transformation (homography) to points.
    
    Args:
        points (np.ndarray): Points to transform, shape (N, 2)
        homography_matrix (np.ndarray): 3x3 homography matrix
    
    Returns:
        np.ndarray: Transformed points, shape (N, 2)
            - Coordinates are normalized by the homogeneous w component
    
    Example:
        >>> H = np.eye(3)  # Identity
        >>> points = np.array([[1, 2], [3, 4]])
        >>> result = apply_homography_2d(points, H)
        >>> print(result)
        [[1, 2],
         [3, 4]]
    """
    points = np.asarray(points, dtype=float)
    if homography_matrix.shape != (3, 3):
        raise ValueError("Must be of shape (3, 3)")
    N = points.shape[0]
    points_h = np.hstack([points, np.ones((N, 1))])
    transformed_points_h = (homography_matrix @ points_h.T).T
    transformed_points = transformed_points_h[:, :2] / transformed_points_h[:, 2, np.newaxis]
    return transformed_points
