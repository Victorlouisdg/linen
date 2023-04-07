import numpy as np
from airo_typing import Vector3DType
from syncloth.paths.path import Path

from linen.geometry.project import project_point_on_line
from linen.geometry.rotate import rotate_orientation, rotate_point, rotate_pose


def circular_arc_position_path(
    start: Vector3DType, center: Vector3DType, axis: Vector3DType, max_angle: float
) -> Path:
    """
    A path of points on a circular arc in function of angle, created by rotating a start point.

    Args:
        start: The start position, the point that will be rotated.
        center: The center of the rotation.
        axis: The axis to rotate around, which will be normalized.
        max_angle: The maximum angle in radians to rotate by. Determines the length of the path.

    Returns:
        The path of positions in function of angle.
    """

    def function(angle: float) -> Vector3DType:
        return rotate_point(start, center, axis, angle)

    return Path(function, start_time=0.0, end_time=max_angle)


def circular_arc_orientation_path(start_orientation, axis, max_angle: float) -> Path:
    """
    A path of orientations on a circular arc in function of angle, created by rotating a start orientation.

    Args:
        start_orientation: The start orientation, the orientation that will be rotated.
        axis: The axis to rotate around, which will be normalized.
        max_angle: The maximum angle in radians to rotate by.

    Returns:
        The path of orientations in function of angle.
    """

    def function(angle: float) -> np.ndarray:
        return rotate_orientation(start_orientation, axis, angle)

    return Path(function, start_time=0.0, end_time=max_angle)


def circular_arc_path(start_pose: np.ndarray, center: Vector3DType, axis: Vector3DType, max_angle: float) -> Path:
    """
    A path of poses on a circular arc in function of angle, created by rotating a start pose.

    Args:
        start_pose: The start pose, the pose that will be rotated.
        center: The center of the rotation.
        axis: The axis to rotate around, which will be normalized.
        max_angle: The maximum angle in radians to rotate by. Determines the length of the path.

    Returns:
        The path of poses in function of angle.
    """

    def function(angle: float) -> np.ndarray:
        return rotate_pose(start_pose, center, axis, angle)

    return Path(function, start_time=0.0, end_time=max_angle)


def circular_arc_position_trajectory(
    start: Vector3DType,
    center: Vector3DType,
    axis: Vector3DType,
    max_angle: float,
    speed: float,
) -> Vector3DType:
    """
    A trajectory of points on a circular arc in function of time, created by rotating a start point.

    Args:
        start: The start position, the point that will be rotated.
        center: The center of the rotation.
        axis: The axis to rotate around, which will be normalized.
        max_angle: The maximum angle in radians to rotate by. Determines the length of the path.
        speed: The speed in meters per second.

    Returns:
        The trajectory of positions in function of time.
    """
    start_projected = project_point_on_line(start, (center, axis))
    radius = np.linalg.norm(start_projected - start)

    # If we use angle = time, the speed along the path is 1 radius/s.
    # If we use angle = time / radius, the speed along the path is 1 m/s.
    # If we use angle = speed * (time / radius), we get a path with the desired speed.
    def function(time: float) -> Vector3DType:
        angle = speed * (time / radius)
        return rotate_point(start, center, axis, angle)

    # Duration is length / speed, the length of a circular arc is the central angle times the radius.
    end_time = (radius * max_angle) / speed

    return Path(function, start_time=0.0, end_time=end_time)


def circular_arc_trajectory(
    start: np.ndarray,
    center: Vector3DType,
    axis: Vector3DType,
    max_angle: float,
    speed: float,
) -> Vector3DType:
    """
    A trajectory of poses on a circular arc in function of time, created by rotating a start pose.

    Args:
        start: The start pose, the pose that will be rotated.
        center: The center of the rotation.
        axis: The axis to rotate around, which will be normalized.
        max_angle: The maximum angle in radians to rotate by. Determines the length of the path.
        speed: The speed in meters per second.

    Returns:
        The trajectory of poses in function of time.
    """
    start_position = start[:3, 3]
    start_projected = project_point_on_line(start_position, (center, axis))
    radius = np.linalg.norm(start_projected - start_position)

    # If we use angle = time, the speed along the path is 1 radius/s.
    # If we use angle = time / radius, the speed along the path is 1 m/s.
    # If we use angle = speed * (time / radius), we get a path with the desired speed.
    def function(time: float) -> Vector3DType:
        angle = speed * (time / radius)
        return rotate_pose(start, center, axis, angle)

    # Duration is length / speed, the length of a circular arc is the central angle times the radius.
    end_time = (radius * max_angle) / speed

    return Path(function, start_time=0.0, end_time=end_time)
