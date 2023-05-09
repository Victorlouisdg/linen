import airo_blender as ab
import bpy
import numpy as np
from scipy.spatial.transform import Rotation

from linen.blender.path import add_linen_trajectory_visualization
from linen.blender.plane import add_plane
from linen.blender.render_setups import setup_cycles, setup_white_background
from linen.blender.robotics.robotiq import add_animated_robotiq
from linen.elemental.move_backwards import move_gripper_backwards_trajectory
from linen.folding.ordered_keypoints import get_counterclockwise_ordered_keypoints
from linen.geometry.orientation import top_down_orientation
from linen.grasping.slide_grasp import slide_grasp_trajectory
from linen.grasping.towel.towel_grasps import towel_aligned_grasps, towel_edges_adjacent_to_edge
from linen.path.concatenate import concatenate_trajectories
from linen.path.linear import linear_slerp_trajectory
from linen.path.reparametrization.synchronize import synchronize

bpy.ops.object.delete()

table = add_plane(0.8, 1.4)
table.location.z = -0.02

towel_width, towel_length = 0.5, 0.7
towel = add_plane(towel_width, towel_length)
towel.location.z = table.location.z

towel.location.x += 0.1
towel.location.y += 0.3
towel.rotation_euler.z += -np.pi / 6

bpy.context.view_layer.update()

# Determine only fold line from original keypoints
keypoints_3D = [towel.matrix_world @ v.co for v in towel.data.vertices]
ordered_keypoints = get_counterclockwise_ordered_keypoints(keypoints_3D)

grasped_edge = 2

grasp_depth = 0.05
grasp_right, grasp_left = towel_aligned_grasps(ordered_keypoints, grasp_depth=grasp_depth, grasped_edge=grasped_edge)
grasp_location_left, grasp_approach_direction_left = grasp_left
grasp_location_right, grasp_approach_direction_right = grasp_right


height_offset = 0.025
grasp_location_left[2] += height_offset
grasp_location_right[2] += height_offset

approach_angle = np.pi / 4
approach_margin = 0.03
approach_distance = grasp_depth + approach_margin

grasp_trajectory_left = slide_grasp_trajectory(
    grasp_location_left,
    grasp_approach_direction_left,
    approach_angle=approach_angle,
    approach_distance=approach_distance,
)
grasp_trajectory_right = slide_grasp_trajectory(
    grasp_location_right,
    grasp_approach_direction_right,
    approach_angle=approach_angle,
    approach_distance=approach_distance,
)

# Prefling locations
distance_between_grasps = np.linalg.norm(grasp_location_left - grasp_location_right)
middle_between_robots = np.array([0.0, 0.0, 0.0])

lift_x = distance_between_grasps / 2

lift_distance_y = 0.8
lift_y_direction = np.array([0, -1, 0])

lift_height = 0.8

lift_location_left = middle_between_robots + [lift_x, 0.0, lift_height] + lift_distance_y * lift_y_direction
lift_location_right = middle_between_robots + [-lift_x, 0.0, lift_height] + lift_distance_y * lift_y_direction


gripper_direction_left = np.array([0, -1, 0])
gripper_direction_right = np.array([0, -1, 0])

# Fix twisting problem
if np.dot(grasp_approach_direction_left, lift_y_direction) < 0:
    gripper_direction_left *= -1

if np.dot(grasp_approach_direction_right, lift_y_direction) < 0:
    gripper_direction_right *= -1

topdown_orientation_left = top_down_orientation(gripper_direction_left)
topdown_orientation_right = top_down_orientation(gripper_direction_right)


angle_x = -np.pi / 2
global_x = np.array([1, 0, 0])
rotation_global_x = Rotation.from_rotvec(angle_x * global_x).as_matrix()

lift_orientation_left = rotation_global_x @ topdown_orientation_left
lift_orientation_right = rotation_global_x @ topdown_orientation_right

lift_pose_left = np.identity(4)
lift_pose_left[:3, :3] = lift_orientation_left
lift_pose_left[:3, 3] = lift_location_left

lift_pose_right = np.identity(4)
lift_pose_right[:3, :3] = lift_orientation_right
lift_pose_right[:3, 3] = lift_location_right


def estimate_towel_length(ordered_keypoints, grasped_edge):
    # Assumes a short edge was grasped
    # Calculate the average length of the two adjacent edges
    edges = [(0, 1), (1, 2), (2, 3), (3, 0)]  # edge 0, 1, 2, 3
    adjacent_edges = towel_edges_adjacent_to_edge(grasped_edge)
    edge0 = edges[adjacent_edges[0]]
    edge1 = edges[adjacent_edges[1]]
    v0 = ordered_keypoints[edge0[0]]
    v1 = ordered_keypoints[edge0[1]]
    v2 = ordered_keypoints[edge1[0]]
    v3 = ordered_keypoints[edge1[1]]
    return (np.linalg.norm(v0 - v1) + np.linalg.norm(v2 - v3)) / 2


laydown_height = 0.05
laydown_y = estimate_towel_length(ordered_keypoints, grasped_edge) / 2 - grasp_depth

laydown_location_left = middle_between_robots + [lift_x, laydown_y, laydown_height]
laydown_location_right = middle_between_robots + [-lift_x, laydown_y, laydown_height]

angle_x_45 = -np.pi / 4
global_x = np.array([1, 0, 0])
rotation_global_x_45 = Rotation.from_rotvec(angle_x_45 * global_x).as_matrix()

laydown_orientation_left = rotation_global_x_45 @ topdown_orientation_left
laydown_orientation_right = rotation_global_x_45 @ topdown_orientation_right

laydown_pose_left = np.identity(4)
laydown_pose_left[:3, :3] = laydown_orientation_left
laydown_pose_left[:3, 3] = laydown_location_left

laydown_pose_right = np.identity(4)
laydown_pose_right[:3, :3] = laydown_orientation_right
laydown_pose_right[:3, 3] = laydown_location_right

lift_trajectory_left = linear_slerp_trajectory(grasp_trajectory_left.end, lift_pose_left, 0.2)
lift_trajectory_right = linear_slerp_trajectory(grasp_trajectory_right.end, lift_pose_right, 0.2)
lift_trajectory_left, lift_trajectory_right = synchronize(lift_trajectory_left, lift_trajectory_right)

laydown_trajectory_left = linear_slerp_trajectory(lift_trajectory_left.end, laydown_pose_left, 0.2)
laydown_trajectory_right = linear_slerp_trajectory(lift_trajectory_right.end, laydown_pose_right, 0.2)
laydown_trajectory_left, laydown_trajectory_right = synchronize(laydown_trajectory_left, laydown_trajectory_right)

retreat_trajectory_left = move_gripper_backwards_trajectory(laydown_trajectory_left.end, grasp_depth, 0.1)
retreat_trajectory_right = move_gripper_backwards_trajectory(laydown_trajectory_right.end, grasp_depth, 0.1)

trajectory_left = concatenate_trajectories(
    [grasp_trajectory_left, lift_trajectory_left, laydown_trajectory_left, retreat_trajectory_left]
)
trajectory_right = concatenate_trajectories(
    [grasp_trajectory_right, lift_trajectory_right, laydown_trajectory_right, retreat_trajectory_right]
)


# Visualization
ab.add_material(towel, [0.800000, 0.663141, 0.520608, 1.000000])
towel_thickness = 0.003
towel.location.z += towel_thickness / 2.0
towel.modifiers.new("Solidify", "SOLIDIFY")
towel.modifiers["Solidify"].thickness = 0.003
towel.modifiers["Solidify"].offset = 0.0

add_linen_trajectory_visualization(trajectory_left, pose_size=0.05)
add_linen_trajectory_visualization(trajectory_right, pose_size=0.05)

add_animated_robotiq(trajectory_left, closed=False)
add_animated_robotiq(trajectory_right, closed=False)

setup_cycles()
setup_white_background()

camera = bpy.context.scene.camera
camera.location = (1.91, -1.13, 0.62)
camera.rotation_euler = list(np.deg2rad([77.2, 0, 59.1]))
