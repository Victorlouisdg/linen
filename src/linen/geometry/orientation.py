import numpy as np
from airo_typing import Vector3DType
from scipy.spatial.transform import Rotation


def flat_orientation(gripper_forward_direction: Vector3DType) -> np.ndarray:
    """Creates an orientation matrix where the gripper opens in the global up direction.

    Args:
        gripper_forward_direction: The direction the gripper should point, (expected to lie in the xy-plane).

    Returns:
        A 3x3 rotation matrix.
    """
    Z = gripper_forward_direction / np.linalg.norm(gripper_forward_direction)
    X = np.array([0, 0, 1])
    Y = np.cross(Z, X)
    return np.column_stack([X, Y, Z])


def top_down_orientation(gripper_open_direction: Vector3DType) -> np.ndarray:
    """Creates an orientation matrix where the gripper points downwards.

    Args:
        gripper_open_direction: The direction the gripper should open, (expected to lie in the xy-plane).

    Returns:
        A 3x3 rotation matrix.
    """
    X = gripper_open_direction / np.linalg.norm(gripper_open_direction)
    Z = np.array([0, 0, -1])
    Y = np.cross(Z, X)
    return np.column_stack([X, Y, Z])


def pitch_gripper_orientation(orientation: np.ndarray, pitch_angle: float) -> np.ndarray:
    """Rotate the gripper over its local Y axis by the given angle.

    Args:
        orientation: The 3x3 orientation matrix of the gripper before the rotation.
        pitch_angle: The angle to rotate the gripper by.

    Returns:
        The 3x3 orientation matrix of the gripper after the rotation.
    """
    local_Y = orientation[:, 1]
    rotation_local_Y = Rotation.from_rotvec(pitch_angle * local_Y).as_matrix()
    orientation = rotation_local_Y @ orientation
    return orientation
