import bpy
import numpy as np

from linen.blender.path import add_growing_path, add_path, add_pose_path
from linen.blender.render_setups import setup_white_background_XZ_camera
from linen.blender.robotics.robotiq import add_animated_robotiq
from linen.folding.trajectories.circular_fold import circular_fold_trajectory
from linen.path.split import split_pose_path

start = np.zeros(3)
center = np.array([0.5, 0.0, 0.0])
axis = np.array([0.0, 1.0, 0.0])
max_angle = np.pi
speed = 0.2
start_pitch_angle = np.pi / 4
end_pitch_angle = np.pi / 6
end_height_offset = 0.1


pose_trajectory = circular_fold_trajectory(
    start,
    center,
    (center, axis),
    start_pitch_angle,
    end_pitch_angle,
    end_height_offset,
    speed,
)

_, position_trajectory = split_pose_path(pose_trajectory)

# Visualization
bpy.ops.object.delete()

red = (1.0, 0.0, 0.0)
soft_yellow = (1.0, 0.8, 0.1)

add_path(position_trajectory, color=red, points_per_second=10)
add_growing_path(position_trajectory, color=soft_yellow)
add_animated_robotiq(pose_trajectory)
add_pose_path(pose_trajectory, num_poses=5)

camera = setup_white_background_XZ_camera(ortho_scale=1.5)
camera.location.x = 0.5
camera.location.z = 0.3
