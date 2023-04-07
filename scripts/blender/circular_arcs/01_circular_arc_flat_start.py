import bpy
import numpy as np

from linen.blender.frame import add_frames
from linen.blender.path import add_growing_path, add_path
from linen.blender.render_setups import setup_white_background_XZ_camera
from linen.blender.robotics.robotiq import add_animated_robotiq
from linen.geometry.orientation import flat_orientation
from linen.path.circular_arc import circular_arc_position_trajectory, circular_arc_trajectory

start = np.zeros(3)
center = np.array([0.5, 0.0, 0.0])
axis = np.array([0.0, 1.0, 0.0])
max_angle = np.pi
speed = 0.1

position_trajectory = circular_arc_position_trajectory(start, center, axis, max_angle, speed)

start_pose = np.identity(4)
start_pose[:3, 3] = start
start_pose[:3, :3] = flat_orientation(center)
pose_trajectory = circular_arc_trajectory(start_pose, center, axis, max_angle, speed)

# Visualization
bpy.ops.object.delete()

red = (1.0, 0.0, 0.0)
soft_yellow = (1.0, 0.8, 0.1)

add_path(position_trajectory, color=red, points_per_second=5)
add_growing_path(position_trajectory, color=soft_yellow)
add_animated_robotiq(pose_trajectory)
add_frames([pose_trajectory(t) for t in np.linspace(0, pose_trajectory.duration, 5)], size=0.1)

camera = setup_white_background_XZ_camera(ortho_scale=1.5)
camera.location.x = 0.5
camera.location.z = 0.3
