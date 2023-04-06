import airo_blender as ab
import bpy
import numpy as np
from mathutils import Matrix

from linen.blender.curve import add_discrete_curve, skin
from linen.blender.points import add_points
from linen.path.path import Path


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
    curve_mesh = add_discrete_curve(curve_points)

    if color is not None:
        ab.add_material(curve_mesh, color=color)

    build_modifier = curve_mesh.modifiers.new(name="Build", type="BUILD")
    build_modifier.frame_start = 1
    build_modifier.frame_duration = num_frames
    skin(curve_mesh, radius=radius)
