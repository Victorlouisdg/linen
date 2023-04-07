import bpy
import numpy as np

from linen.blender.frame import add_frames
from linen.blender.path import add_growing_path, add_path
from linen.blender.render_setups import setup_white_background_XZ_camera
from linen.blender.robotics.robotiq import add_animated_robotiq
from linen.geometry.rotate import rotate_orientation
from linen.path.combine import combine_orientation_and_position_paths
from linen.path.linear import linear_trajectory
from linen.path.path import Path
from linen.path.speed import scale_speed

speed = 0.1

start = np.zeros(3)
end = np.array([0.0, 0.0, 0.25])

position_trajectory = linear_trajectory(start, end, speed)

gripper_Z = np.array([1.0, 0.0, 0.0])
gripper_X = np.array([0.0, 1.0, 0.0])
gripper_Y = np.cross(gripper_Z, gripper_X)
orientation = np.column_stack([gripper_X, gripper_Y, gripper_Z])


def rotating_orientation_path(start_orientation, axis, end_angle) -> Path:
    def function(angle):
        return rotate_orientation(start_orientation, axis, angle)

    return Path(function, 0.0, end_angle)


orientation_path = rotating_orientation_path(orientation, gripper_Z, np.pi)

factor = orientation_path.duration / position_trajectory.duration
orientation_trajectory = scale_speed(orientation_path, factor)

pose_trajectory = combine_orientation_and_position_paths(orientation_trajectory, position_trajectory)


# Visualization
bpy.ops.object.delete()

red = (1.0, 0.0, 0.0)
soft_yellow = (1.0, 0.8, 0.1)

add_path(position_trajectory, color=red, points_per_second=5)
add_growing_path(position_trajectory, color=soft_yellow)
add_animated_robotiq(pose_trajectory)
add_frames([pose_trajectory.start, pose_trajectory.end], size=0.04)

camera = setup_white_background_XZ_camera(ortho_scale=0.5)
camera.location.z = 0.09
