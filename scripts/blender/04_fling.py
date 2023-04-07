import bpy
import numpy as np

from linen.blender.path import add_growing_path, add_path
from linen.blender.render_setups import setup_white_background_XZ_camera
from linen.path.circular_arc import circular_arc_position_trajectory
from linen.path.concatenate import concatenate_trajectories
from linen.path.linear import linear_trajectory

start = np.zeros(3)
lift_end = np.array([0.0, 0.0, 0.1])
lift_speed = 0.1
lift_position_trajectory = linear_trajectory(start, lift_end, lift_speed)

swing_radius = 0.3
swing_center = lift_end + np.array([0.0, 0.0, swing_radius])
swing_trajectory = circular_arc_position_trajectory(
    lift_end, swing_center, np.array([0, 1, 0]), max_angle=np.pi / 2, speed=0.5
)


fling_center_offset = np.array([0.0, 0.0, 0.1])
fling_center = swing_center + fling_center_offset
print(swing_center, fling_center_offset, fling_center)
fling_start = swing_trajectory.end

fling_trajectory = circular_arc_position_trajectory(
    fling_start, fling_center, np.array([0, -1, 0]), max_angle=0.8 * np.pi, speed=0.5
)

descent_start = fling_trajectory.end
descent_end = np.array([0.1, 0.0, 0.0])
descent_speed = 0.25
descent_trajectory = linear_trajectory(descent_start, descent_end, descent_speed)

position_trajectory = concatenate_trajectories(
    [lift_position_trajectory, swing_trajectory, fling_trajectory, descent_trajectory]
)

# Visualization
bpy.ops.object.delete()

red = (1.0, 0.0, 0.0)
soft_yellow = (1.0, 0.8, 0.1)

add_path(position_trajectory, color=red, points_per_second=10)
add_growing_path(position_trajectory, color=soft_yellow)
# add_animated_robotiq(pose_trajectory)
# add_frames([pose_trajectory.start, pose_trajectory.end], size=0.04)

camera = setup_white_background_XZ_camera(ortho_scale=0.5)
camera.location.z = 0.09
