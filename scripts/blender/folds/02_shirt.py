from linen.elemental.move_backwards import move_gripper_backwards_trajectory
from linen.folding.fold_lines.shirt import shirt_sleeve_and_side_fold_line
import airo_blender as ab
import bpy
from linen.geometry.intersect import intersect_lines
from linen.geometry.project import project_point_on_line
from linen.grasping.edge_grasps import orthogonal_insetted_edge_grasps
from linen.grasping.shirt.shirt_grasps import shirt_sleeve_and_waist_grasps
from linen.path.reparametrization.speed import scale_speed
import numpy as np

from linen.blender.curve import add_discrete_curve, add_line_segment
from linen.blender.path import add_linen_trajectory_visualization
from linen.blender.plane import add_plane
from linen.blender.render_setups import setup_cycles, setup_white_background
from linen.blender.robotics.robotiq import add_animated_robotiq
from linen.folding.fold_lines.towel import towel_fold_line
from linen.folding.ordered_keypoints import get_counterclockwise_ordered_keypoints
from linen.folding.trajectories.circular_fold import circular_fold_trajectory
from linen.grasping.slide_grasp import slide_grasp_trajectory
from linen.grasping.towel.towel_grasps import towel_aligned_grasps
from linen.path.concatenate import concatenate_trajectories
from linen.path.linear import linear_constant_orientation_trajectory
from synthetic_cloth_data.geometric_templates import TshirtMeshConfig, create_tshirt_vertices


bpy.ops.object.delete()

table = add_plane(0.8, 1.4)
table.location.z = -0.001


vertices, keypoints = create_tshirt_vertices(TshirtMeshConfig())
keypoints_3D = keypoints.values()


add_discrete_curve(vertices, closed=True)

grasp_depth = 0.05
height_offset = 0.025
approach_angle = np.pi / 4
approach_margin = 0.03
approach_distance = grasp_depth + approach_margin
shirt_left_side = False
middle_fold = True

if middle_fold:
    waist_left = keypoints["waist_left"]
    waist_right = keypoints["waist_right"]
    neck_left = keypoints["neck_left"]
    neck_right = keypoints["neck_right"]

    fold_line_left = shirt_sleeve_and_side_fold_line(keypoints, left=True, offset_from_armpit_fraction=1.0/5)
    fold_line_right = shirt_sleeve_and_side_fold_line(keypoints, left=False, offset_from_armpit_fraction=1.0/5)

    waist_left_to_right = waist_right - waist_left
    waist_left_to_right /= np.linalg.norm(waist_left_to_right)

    waist_line = (waist_left, waist_left_to_right)

    fold_line_left_point = fold_line_left[0]
    fold_line_right_point = fold_line_right[0]

    waist_left_fold_point = project_point_on_line(fold_line_left_point, waist_line)
    waist_right_fold_point = project_point_on_line(fold_line_right_point, waist_line)
    

    neck_left_to_right = neck_right - neck_left
    neck_left_to_right /= np.linalg.norm(neck_left_to_right)
    
    left_to_right = neck_left_to_right + waist_left_to_right
    left_to_right /= np.linalg.norm(left_to_right)

    fold_line_direction = -left_to_right

    neck_middle = (neck_left + neck_right) / 2
    waist_middle = (waist_left + waist_right) / 2
    shirt_middle = (neck_middle + waist_middle) / 2

    fold_line = (shirt_middle, fold_line_direction)

    # calculate grasps
    grasp_left, grasp_right = orthogonal_insetted_edge_grasps(
        waist_left_fold_point, waist_right_fold_point, grasp_depth=grasp_depth, inset=0.03
    )

    print(grasp_left, grasp_right)

else:
    fold_line = shirt_sleeve_and_side_fold_line(keypoints, left=shirt_left_side, offset_from_armpit_fraction=1.0/5)
    sleeve_grasp, waist_grasp = shirt_sleeve_and_waist_grasps(keypoints, grasp_depth=grasp_depth, waist_inset=0.03, left=shirt_left_side)

    if shirt_left_side:
        grasp_left = sleeve_grasp
        grasp_right = waist_grasp
    else:
        grasp_left = waist_grasp
        grasp_right = sleeve_grasp

grasp_location_left, grasp_direction_left = grasp_left
grasp_location_right, grasp_direction_right = grasp_right

grasp_location_left[2] += height_offset
grasp_location_right[2] += height_offset

grasp_trajectory_left = slide_grasp_trajectory(
    grasp_location_left, grasp_direction_left, approach_angle=approach_angle, approach_distance=approach_distance
)
grasp_trajectory_right = slide_grasp_trajectory(
    grasp_location_right, grasp_direction_right, approach_angle=approach_angle, approach_distance=approach_distance
)

fold_arc_trajectory_left = circular_fold_trajectory(
    grasp_location_left, grasp_direction_left, fold_line, start_pitch_angle=approach_angle, speed=0.1
)

fold_arc_trajectory_right = circular_fold_trajectory(
    grasp_location_right, grasp_direction_right, fold_line, start_pitch_angle=approach_angle, speed=0.1
)

duration_left = fold_arc_trajectory_left.duration
duration_right = fold_arc_trajectory_right.duration

if duration_left > duration_right:
    # slow down right
    factor = duration_right / duration_left
    fold_arc_trajectory_right = scale_speed(fold_arc_trajectory_right, factor)
elif duration_right > duration_left:
    # slow down left
    factor = duration_left / duration_right
    fold_arc_trajectory_left = scale_speed(fold_arc_trajectory_left, factor)


retreat_trajectory_left = move_gripper_backwards_trajectory(fold_arc_trajectory_left.end, grasp_depth, 0.1)
retreat_trajectory_right = move_gripper_backwards_trajectory(fold_arc_trajectory_right.end, grasp_depth, 0.1)

trajectory_left = concatenate_trajectories([grasp_trajectory_left, fold_arc_trajectory_left, retreat_trajectory_left])
trajectory_right = concatenate_trajectories(
    [grasp_trajectory_right, fold_arc_trajectory_right, retreat_trajectory_right]
)

# # Visualization
fold_line_point, fold_line_direction = fold_line
fold_line_start = fold_line_point - fold_line_direction 
fold_line_end = fold_line_point + fold_line_direction
fold_line_object = add_line_segment(fold_line_start, fold_line_end)
ab.add_material(fold_line_object, [1.000000, 0.404182, 0.011072, 1.000000])

add_linen_trajectory_visualization(trajectory_left, pose_size=0.05)
add_linen_trajectory_visualization(trajectory_right, pose_size=0.05)

add_animated_robotiq(trajectory_left, closed=False)
add_animated_robotiq(trajectory_right, closed=False)

setup_cycles()
setup_white_background()

camera = bpy.context.scene.camera
camera.location = (1.91, -1.13, 0.62)
camera.rotation_euler = list(np.deg2rad([77.2, 0, 59.1]))
