import numpy as np
from airo_typing import Vector3DType
from scipy.spatial.transform import Rotation


def rotate_vector(vector: Vector3DType, axis: Vector3DType, angle: float) -> Vector3DType:
    """
    Rotate a vector around an axis by a given angle.

    Args:
        vector: The vector to rotate.
        axis: The axis to rotate around, which will be normalized.
        angle: The angle in radians to rotate by.

    Returns:
        The rotated vector.
    """
    unit_axis = axis / np.linalg.norm(axis)
    rotation = Rotation.from_rotvec(angle * unit_axis)
    return rotation.apply(vector)


def rotate_point(point: Vector3DType, center: Vector3DType, axis: Vector3DType, angle: float):
    """
    Rotate a point around an axis by a given angle.

    Args:
        point: The point to rotate.
        center: The center of the rotation.
        axis: The axis to rotate around, which will be normalized.
        angle: The angle in radians to rotate by.

    Returns:
        The rotated point.
    """
    unit_axis = axis / np.linalg.norm(axis)
    rotation = Rotation.from_rotvec(angle * unit_axis)
    return center + rotation.apply(point - center)


def rotate_orientation(orientation: np.ndarray, axis: Vector3DType, angle: float):
    """
    Rotate a 3x3 orientation matrix around an axis by a given angle.

    Args:
        orientation: The 3x3 orientation matrix to rotate.
        axis: The axis to rotate around, which will be normalized.
        angle: The angle in radians to rotate by.

    Returns:
        The rotated orientation matrix.
    """
    unit_axis = axis / np.linalg.norm(axis)
    rotation = Rotation.from_rotvec(angle * unit_axis)
    return rotation.as_matrix() @ orientation


def rotate_pose(pose: np.ndarray, center: Vector3DType, axis: Vector3DType, angle: float):
    """
    Rotate a 4x4 pose matrix around an axis by a given angle.

    Args:
        pose: The 4x4 pose matrix to rotate.
        center: The center of the rotation.
        axis: The axis to rotate around, which will be normalized.
        angle: The angle in radians to rotate by.

    Returns:
        The rotated pose matrix.
    """
    center_pose = np.identity(4)
    center_pose[:3, 3] = center

    unit_axis = axis / np.linalg.norm(axis)
    rotation = Rotation.from_rotvec(angle * unit_axis)
    homogeneous_rotation = np.identity(4)
    homogeneous_rotation[:3, :3] = rotation.as_matrix()
    return center_pose @ homogeneous_rotation @ np.linalg.inv(center_pose) @ pose
