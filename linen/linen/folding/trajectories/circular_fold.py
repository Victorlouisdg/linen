from typing import Tuple

import numpy as np
from airo_typing import Vector3DType

from linen.geometry.orientation import flat_orientation, pitch_gripper_orientation
from linen.geometry.project import project_point_on_line
from linen.path.circular_arc import circular_arc_orientation_path, circular_arc_position_trajectory
from linen.path.combine import combine_orientation_and_position_paths
from linen.path.path import Path
from linen.path.slerp import slerp_trajectory


def circular_fold_middle_orientation(approach_direction: Vector3DType, fold_line_direction: Vector3DType) -> Path:
    start_orientation_flat = flat_orientation(approach_direction)

    orientation_path = circular_arc_orientation_path(start_orientation_flat, fold_line_direction, np.pi)
    middle_orientation = orientation_path(np.pi / 2)
    return middle_orientation


def circular_fold_end_orientation(approach_direction: Vector3DType, fold_line_direction: Vector3DType) -> Path:
    start_orientation_flat = flat_orientation(approach_direction)

    orientation_path = circular_arc_orientation_path(start_orientation_flat, fold_line_direction, np.pi)
    end_orientation = orientation_path(np.pi)
    return end_orientation


def circular_fold_trajectory(
    grasp_location: Vector3DType,
    approach_direction: Vector3DType,
    fold_line: Tuple[Vector3DType, Vector3DType],
    start_pitch_angle: float = np.pi / 4,
    end_pitch_angle: float = np.pi / 4,
    end_height_offset: float = 0.04,
    speed: float = 0.2,
) -> Path:
    """
    TODO: make doc.

    For towels, you can use linen.folding.fold_lines.towel.towel_fold_line(keypoints) method.

    Args:
        grasp_location: The location of the grasp, i.e. where the gripper closes.
        approach_direction: The approach direction of the gripper.
        fold_line: Point on the fold line and fold line direction.
        start_pitch_angle: The pitch angle of the gripper at the start of the fold.
        end_pitch_angle: The pitch angle of the gripper at the end of the fold.
        end_height_offset: The height offset of the gripper at the end of the fold.
        speed: The constant speed of the gripper alond the fold arc.


    Returns:
        The circular fold trajectory.
    """

    fold_line_point, fold_line_direction = fold_line
    start_height = grasp_location[2] - fold_line_point[2]

    grasp_projected = project_point_on_line(grasp_location, fold_line)
    radius = np.linalg.norm(grasp_projected - grasp_location)
    start_angle_delta = np.arcsin(start_height / radius)
    end_angle_delta = np.arcsin((start_height + end_height_offset) / radius)
    max_angle = np.pi - start_angle_delta - end_angle_delta

    position_trajectory = circular_arc_position_trajectory(grasp_location, *fold_line, max_angle, speed)

    middle_orientation = circular_fold_middle_orientation(approach_direction, fold_line_direction)

    start_orientation_flat = flat_orientation(approach_direction)
    start_orientation = pitch_gripper_orientation(start_orientation_flat, -start_pitch_angle)

    end_orientation = circular_fold_end_orientation(approach_direction, fold_line_direction)
    end_orientation = pitch_gripper_orientation(end_orientation, end_pitch_angle)

    orientations = [start_orientation, middle_orientation, end_orientation]
    times = [0, position_trajectory.duration / 2, position_trajectory.duration]
    orientation_trajectory = slerp_trajectory(times, orientations)

    pose_trajectory = combine_orientation_and_position_paths(orientation_trajectory, position_trajectory)
    return pose_trajectory
