import airo_blender as ab
import bpy
import numpy as np
from mathutils import Matrix

from linen.blender.curve import add_discrete_curve_mesh, skin
from linen.blender.frame import add_frames
from linen.blender.points import add_points
from linen.path.path import Path
from linen.path.split import split_pose_path


def add_path(path: Path, points_per_second: int = 10, endpoint=True, radius=0.004, color=None) -> bpy.types.Object:
    """Visualizes a position path as small spheres.

    Args:
        path: The position path to visualize.
        points_per_second: The number of points to add per second of the path's duration.
        endpoint: Whether to include the endpoint of the path, useful for visualizing consecutive paths.
        radius: The radius of the spheres.
        color: Color of the spheres.

    Returns:
        The object from which all spheres are instanced.
    """
    n = max(2, int(points_per_second * path.duration))
    points = [path(t) for t in np.linspace(path.start_time, path.end_time, n, endpoint=endpoint)]
    point_template = add_points(points, radius, color)
    return point_template


def add_pose_path(path: Path, num_poses: int = 2, endpoint=True, size=0.1) -> bpy.types.Object:
    """Visualizes a pose path as a series of frames.

    Args:
        path: The pose path to visualize.
        num_poses: The number of poses to visualize.
        endpoint: Whether to include the endpoint of the path, useful for visualizing consecutive paths.
        size: The size of the frames.

    Returns:
        The object from which all frames are instanced.
    """
    times = np.linspace(path.start_time, path.end_time, num_poses, endpoint=endpoint)
    poses = [path(t) for t in times]
    frame_template = add_frames(poses, size)
    return frame_template


def animate_object_along_path(object: bpy.types.Object, pose_path: Path) -> None:
    """Animates an object along a pose path. The amount of frames required for the animation is determined by the
    duration of the pose path and the scene's frame rate.

    Args:
        object: The object to animate.
        pose_path: The pose path to animate the object along.
    """
    fps = bpy.context.scene.render.fps
    frame_interval = 1 / fps
    num_frames = int(np.ceil(pose_path.duration / frame_interval))

    bpy.context.scene.frame_set(1)

    for i in range(num_frames):
        bpy.context.scene.frame_set(i + 1)
        t = i * frame_interval
        pose = pose_path(pose_path.start_time + t)
        object.matrix_world = Matrix(pose)
        bpy.context.view_layer.update()
        object.keyframe_insert(data_path="location")
        object.keyframe_insert(data_path="rotation_euler")

    bpy.context.scene.frame_set(1)
    bpy.context.scene.frame_start = 1
    bpy.context.scene.frame_end = num_frames


def add_growing_path(path, radius=0.005, color=None):
    fps = bpy.context.scene.render.fps
    frame_interval = 1 / fps
    num_frames = int(np.ceil(path.duration / frame_interval))

    curve_points = [path(t) for t in np.linspace(path.start_time, path.end_time, num_frames)]
    curve_mesh = add_discrete_curve_mesh(curve_points)

    if color is not None:
        ab.add_material(curve_mesh, color=color)

    build_modifier = curve_mesh.modifiers.new(name="Build", type="BUILD")
    build_modifier.frame_start = 1
    build_modifier.frame_duration = num_frames
    skin(curve_mesh, radius=radius)


def add_linen_trajectory_visualization(
    pose_trajectory: Path, num_poses: int = 2, points_per_second: int = 10, pose_size: float = 0.1
) -> bpy.types.Object:
    _, position_trajectory = split_pose_path(pose_trajectory)

    red = (1.0, 0.0, 0.0)
    soft_yellow = (1.0, 0.8, 0.1)

    add_path(position_trajectory, points_per_second=points_per_second, color=red)
    add_growing_path(position_trajectory, color=soft_yellow)
    add_pose_path(pose_trajectory, num_poses=num_poses, size=pose_size)
