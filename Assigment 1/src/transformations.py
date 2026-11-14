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

def translation_matrix_2d(tx, ty):
    tx = float(tx)
    ty = float(ty)
    return np.array([
        [1, 0, tx],
        [0, 1, ty],
        [0, 0, 1]
    ])
  


def apply_translation_2d(points, tx, ty):
    points = np.asarray(points, dtype=float)
    translated_points = points + np.array([tx, ty])
    return translated_points


def rotation_matrix_2d(angle_rad):
    angle_rad = float(angle_rad)
    c = np.cos(angle_rad)
    s = np.sin(angle_rad)
    return np.array([
        [c, -s],
        [s,  c]
    ])


def apply_rotation_2d(points, angle_rad):
    points = np.asarray(points, dtype=float)
    R = rotation_matrix_2d(angle_rad)
    rotated_points = points @ R.T
    return rotated_points


def rotation_matrix_3d_x(angle_rad):
    angle_rad = float(angle_rad)
    c = np.cos(angle_rad)
    s = np.sin(angle_rad)
    return np.array([
        [1, 0, 0],
        [0, c, -s],
        [0, s,  c]
    ])


def rotation_matrix_3d_y(angle_rad):
    angle_rad = float(angle_rad)
    c = np.cos(angle_rad)
    s = np.sin(angle_rad)
    return np.array([
        [c, 0, s],
        [0, 1, 0],
        [-s, 0, c]
    ])


def rotation_matrix_3d_z(angle_rad):
    angle_rad = float(angle_rad)
    c = np.cos(angle_rad)
    s = np.sin(angle_rad)
    return np.array([
        [c, -s, 0],
        [s,  c, 0],
        [0,  0, 1]
    ])


def compose_rotations_3d(phi, theta, eta):
    R_x = rotation_matrix_3d_x(phi)
    R_y = rotation_matrix_3d_y(theta)
    R_z = rotation_matrix_3d_z(eta)
    return R_x @ R_y @ R_z


def affine_matrix_from_points(src_points, dst_points):
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
    points = np.asarray(points, dtype=float)
    if affine_matrix.shape != (2, 3):
        raise ValueError("Must be of shape (2, 3)")
    N = points.shape[0]
    points_h = np.hstack([points, np.ones((N, 1))])
    transformed_points = (affine_matrix @ points_h.T).T
    return transformed_points


def homography_matrix_from_points(src_points, dst_points):
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
    points = np.asarray(points, dtype=float)
    if homography_matrix.shape != (3, 3):
        raise ValueError("Must be of shape (3, 3)")
    N = points.shape[0]
    points_h = np.hstack([points, np.ones((N, 1))])
    transformed_points_h = (homography_matrix @ points_h.T).T
    transformed_points = transformed_points_h[:, :2] / transformed_points_h[:, 2, np.newaxis]
    return transformed_points
