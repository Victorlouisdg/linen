import numpy as np
from airo_typing import Vector3DType

from linen.geometry.orientation import flat_orientation, pitch_gripper_orientation
from linen.path.combine import combine_orientation_and_position_paths
from linen.path.concatenate import concatenate_trajectories
from linen.path.constant import constant_trajectory
from linen.path.linear import linear_trajectory
from linen.path.path import Path


def slide_grasp_position_trajectory(
    grasp_location: Vector3DType,
    approach_direction: Vector3DType,
    approach_distance: float = 0.05,
    hover_height: float = 0.05,
    speed: float = 0.1,
) -> Path:
    """
    The L-shaped position trajectory for a slide grasp. The final position of the trajectory is the grasp location. The
    sliding parh is governed by the approach direction and distance. Before the sliding, the gripper hovers above the
    surface a the hover height, from where it starts moving straight down.

    Args:
        grasp_location: The final position of the slide grasp.
        approach_direction: The direction of the sliding.
        approach_distance: The distance to approach the grasp location from.
        hover_height: The height to hover above the point where the grasp will start.
        speed: The constant speed of the gripper for the entire trajectory.

    Returns:
        The position trajectory for the slide grasp.
    """
    approach_direction /= np.linalg.norm(approach_direction)

    pregrasp_location = grasp_location - approach_distance * approach_direction
    hover_location = pregrasp_location + np.array([0.0, 0.0, hover_height])

    descent_trajectory = linear_trajectory(hover_location, pregrasp_location, speed=speed)
    approach_trajectory = linear_trajectory(pregrasp_location, grasp_location, speed=speed)

    trajectory = concatenate_trajectories([descent_trajectory, approach_trajectory])
    return trajectory


def slide_grasp_orientation(approach_direction, approach_angle) -> np.ndarray:
    """The pitched orientation for a slide grasp.

    Args:
        approach_direction: The direction of the sliding.
        approach_angle: The angle with the table that the gripper makes during the approach.

    Returns:
        The 3x3 orientation matrix.
    """
    approach_direction /= np.linalg.norm(approach_direction)
    orientation = flat_orientation(approach_direction)
    pitched_orientation = pitch_gripper_orientation(orientation, -approach_angle)
    return pitched_orientation


def slide_grasp_trajectory(
    grasp_location: Vector3DType,
    approach_direction: Vector3DType,
    approach_distance: float = 0.05,
    approach_angle: float = np.pi / 4,
    hover_height: float = 0.05,
    speed: float = 0.05,
) -> Path:
    """
    The pose trajectory for a slide grasp. Combines the L-shaped position trajectory and a constant orientation
    trajectory.

    Args:
        grasp_location: The final position of the slide grasp.
        approach_direction: The direction of the sliding.
        approach_distance: The distance to approach the grasp location from.
        approach_angle: The angle with the table that the gripper makes during the approach.
        hover_height: The height to hover above the point where the grasp will start.
        speed: The constant speed of the gripper for the entire trajectory.

    Returns:
        The pose trajectory for the slide grasp.
    """

    position_trajectory = slide_grasp_position_trajectory(
        grasp_location, approach_direction, approach_distance, hover_height, speed
    )

    orientation = slide_grasp_orientation(approach_direction, approach_angle)
    orientation_trajectory = constant_trajectory(orientation, duration=position_trajectory.duration)

    pose_trajectory = combine_orientation_and_position_paths(orientation_trajectory, position_trajectory)
    return pose_trajectory
