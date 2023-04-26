import bpy
import numpy as np

from linen.blender.path import add_linen_trajectory_visualization
from linen.blender.points import add_points
from linen.blender.render_setups import setup_cycles, setup_white_background
from linen.blender.robotics.robotiq import add_animated_robotiq
from linen.grasping.slide_grasp import slide_grasp_orientation
from linen.repositioning.rotate import rotate_trajectories

approach_angle = np.pi / 4

position0 = np.array([0.5, 0, 0])
position1 = np.array([0, 0.25, 0])

approach_direction0 = np.array([0, 1.0, 0])
approach_direction1 = np.array([0, -1.0, 0])

orientation0 = slide_grasp_orientation(approach_direction0, approach_angle)
orientation1 = slide_grasp_orientation(approach_direction1, approach_angle)

pose0 = np.identity(4)
pose0[:3, 3] = position0
pose0[:3, :3] = orientation0

pose1 = np.identity(4)
pose1[:3, 3] = position1
pose1[:3, :3] = orientation1

trajectory0, trajectory1 = rotate_trajectories(pose0, pose1, -np.pi / 2)

bpy.ops.object.delete()

camera = bpy.context.scene.camera
camera.rotation_euler = np.deg2rad([65.2, 0.0, 51.1])
camera.location = np.array([1.928, -1.22, 1.04])

orange = [1.0, 0.27, 0.0, 1.0]
center = (pose0[:3, 3] + pose1[:3, 3]) / 2
add_points([center], radius=0.01, color=orange)

add_linen_trajectory_visualization(trajectory0, pose_size=0.05)
add_linen_trajectory_visualization(trajectory1, pose_size=0.05)

add_animated_robotiq(trajectory0)
add_animated_robotiq(trajectory1)

setup_cycles()
setup_white_background()
