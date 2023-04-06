import bpy
import numpy as np

from linen.blender.frame import add_frames
from linen.blender.path import add_growing_path, add_path
from linen.blender.render_setups import setup_white_background_XZ_camera
from linen.blender.robotics.robotiq import add_animated_robotiq
from linen.grasping.slide_grasp import slide_grasp_position_trajectory, slide_grasp_trajectory

speed = 0.025
hover_height = 0.06
approach_margin = 0.02
approach_distance = 0.1

approach_direction = np.array([1.0, 0.0, 0.0])
grasp_location = approach_distance * approach_direction
approach_angle = np.pi / 4

position_trajectory = slide_grasp_position_trajectory(
    grasp_location, approach_direction, approach_distance, hover_height, speed
)

pose_trajectory = slide_grasp_trajectory(
    grasp_location, approach_direction, approach_distance, approach_angle, hover_height, speed
)

# Visualization
bpy.ops.object.delete()

red = (1.0, 0.0, 0.0)
soft_yellow = (1.0, 0.8, 0.1)

add_path(position_trajectory, color=red, points_per_second=2)
add_growing_path(position_trajectory, color=soft_yellow)
add_animated_robotiq(pose_trajectory, closed=False)
add_frames([pose_trajectory.start, pose_trajectory.end], size=0.04)

camera = setup_white_background_XZ_camera(ortho_scale=0.5)
camera.location.z = 0.09
