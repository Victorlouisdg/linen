import numpy as np

from linen.path.linear import linear_constant_orientation_trajectory


def move_gripper_backwards_trajectory(start_pose: np.ndarray, distance: float, speed: float):
    start_position = start_pose[:3, 3]
    gripper_backwards = -start_pose[:3, 2]  # Z is forward by our convention
    end_position = start_position + distance * gripper_backwards
    orientation = start_pose[:3, :3]
    return linear_constant_orientation_trajectory(start_position, end_position, orientation, speed)
