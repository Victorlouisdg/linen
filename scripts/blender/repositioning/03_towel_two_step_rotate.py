import airo_blender as ab
import bpy
import numpy as np
from mathutils import Vector

from linen.blender.path import add_linen_trajectory_visualization
from linen.blender.plane import add_plane
from linen.blender.points import add_points
from linen.blender.render_setups import setup_cycles, setup_white_background
from linen.blender.robotics.robotiq import add_animated_robotiq
from linen.folding.fold_lines.towel import towel_fold_line
from linen.folding.ordered_keypoints import get_counterclockwise_ordered_keypoints
from linen.geometry.rotate import rotate_point
from linen.grasping.slide_grasp import slide_grasp_trajectory
from linen.grasping.towel.towel_grasps import towel_aligned_grasps, towel_twisted_grasps
from linen.path.concatenate import concatenate_trajectories
from linen.path.linear import linear_constant_orientation_trajectory
from linen.repositioning.rotate import rotate_trajectories

bpy.ops.object.delete()

table = add_plane(0.8, 1.4)
table.location.z = -0.02

towel_width, towel_length = 0.5, 0.7
towel = add_plane(towel_width, towel_length)
towel.location.z = table.location.z

bpy.context.view_layer.update()

# Determine only fold line from original keypoints
keypoints_3D = [towel.matrix_world @ v.co for v in towel.data.vertices]
ordered_keypoints = get_counterclockwise_ordered_keypoints(keypoints_3D)
fold_line = towel_fold_line(ordered_keypoints)

# To make the towel look folded, snap the points with positive y to y=0.
for vertex in towel.data.vertices:
    if vertex.co.y > 0.0:
        vertex.co.y = 0.0


keypoints_after_fold_3D = [towel.matrix_world @ v.co for v in towel.data.vertices]
ordered_keypoints_after_fold = get_counterclockwise_ordered_keypoints(keypoints_after_fold_3D)


grasp_depth = 0.05
grasp_left, grasp_right = towel_aligned_grasps(ordered_keypoints_after_fold, grasp_depth=grasp_depth)
grasp_location_left, grasp_direction_left = grasp_left
grasp_location_right, grasp_direction_right = grasp_right

height_offset = 0.025
grasp_location_left[2] += height_offset
grasp_location_right[2] += height_offset

approach_angle = np.pi / 4
approach_margin = 0.03
approach_distance = grasp_depth + approach_margin

grasp_trajectory_left = slide_grasp_trajectory(
    grasp_location_left,
    grasp_direction_left,
    approach_angle=approach_angle,
    approach_distance=approach_distance,
)
grasp_trajectory_right = slide_grasp_trajectory(
    grasp_location_right,
    grasp_direction_right,
    approach_angle=approach_angle,
    approach_distance=approach_distance,
)


def slide_gripper_backwards_trajectory(start_pose: np.ndarray, distance: float, speed: float):
    start_position = start_pose[:3, 3]
    gripper_backwards = -start_pose[:3, 2]  # Z is forward by our convention
    gripper_backwards_projected = gripper_backwards.copy()
    gripper_backwards_projected[2] = 0.0
    gripper_backwards_projected /= np.linalg.norm(gripper_backwards_projected)
    end_position = start_position + distance * gripper_backwards_projected
    orientation = start_pose[:3, :3]
    return linear_constant_orientation_trajectory(start_position, end_position, orientation, speed)


drag_distance = towel_length / 4.0
drag_trajectory_left = slide_gripper_backwards_trajectory(grasp_trajectory_left.end, drag_distance, 0.05)
drag_trajectory_right = slide_gripper_backwards_trajectory(grasp_trajectory_right.end, drag_distance, 0.05)


drag_translation_left = drag_trajectory_left.end[:3, 3] - grasp_trajectory_left.end[:3, 3]
drag_translation_right = drag_trajectory_right.end[:3, 3] - grasp_trajectory_right.end[:3, 3]
drag_translation_estimate = (drag_translation_left + drag_translation_right) / 2

keypoints_after_drag = ordered_keypoints_after_fold + drag_translation_estimate


# Just for visuals
for vertex in towel.data.vertices:
    vertex.co += Vector(drag_translation_estimate)


center = np.zeros(3)

Z_axis = np.array([0, 0, 1])
angle = np.pi / 4
rotated_keypoints = [rotate_point(p, center, Z_axis, angle) for p in keypoints_after_drag]

for vertex in towel.data.vertices:
    vertex.co = Vector(rotate_point(np.array(vertex.co), center, Z_axis, angle))

reordered_keypoints = [rotated_keypoints[-1]] + rotated_keypoints[:-1]
# reordered_keypoints = rotated_keypoints

rotate_grasp_right, rotate_grasp_left = towel_twisted_grasps(
    reordered_keypoints, grasp_depth=grasp_depth, top_grasp_near0=False
)
rotate_grasp_location_left, rotate_grasp_approach_direction_left = rotate_grasp_left
rotate_grasp_location_right, rotate_grasp_approach_direction_right = rotate_grasp_right

rotate_grasp_location_left[2] += height_offset
rotate_grasp_location_right[2] += height_offset


rotate_grasp_trajectory_left = slide_grasp_trajectory(
    rotate_grasp_location_left,
    rotate_grasp_approach_direction_left,
    approach_angle=approach_angle,
    approach_distance=approach_distance,
)

rotate_grasp_trajectory_right = slide_grasp_trajectory(
    rotate_grasp_location_right,
    rotate_grasp_approach_direction_right,
    approach_angle=approach_angle,
    approach_distance=approach_distance,
)

rotate_trajectory_left, rotate_trajectory_right = rotate_trajectories(
    rotate_grasp_trajectory_left.end, rotate_grasp_trajectory_right.end, np.pi / 4
)


trajectory_left = concatenate_trajectories([rotate_grasp_trajectory_left, rotate_trajectory_left])
trajectory_right = concatenate_trajectories([rotate_grasp_trajectory_right, rotate_trajectory_right])


# Visualization
ab.add_material(towel, [0.800000, 0.663141, 0.520608, 1.000000])
towel_thickness = 0.003
towel.location.z += towel_thickness / 2.0
towel.modifiers.new("Solidify", "SOLIDIFY")
towel.modifiers["Solidify"].thickness = 0.003
towel.modifiers["Solidify"].offset = 0.0

orange = [1.0, 0.27, 0.0, 1.0]
center = (rotate_trajectory_left.start[:3, 3] + rotate_trajectory_right.start[:3, 3]) / 2
add_points([center], radius=0.01, color=orange)


add_linen_trajectory_visualization(trajectory_left, pose_size=0.05)
add_linen_trajectory_visualization(trajectory_right, pose_size=0.05)

add_animated_robotiq(trajectory_left, closed=False)
add_animated_robotiq(trajectory_right, closed=False)

setup_cycles()
setup_white_background()

camera = bpy.context.scene.camera
camera.location = (1.91, -1.13, 0.62)
camera.rotation_euler = list(np.deg2rad([77.2, 0, 59.1]))
