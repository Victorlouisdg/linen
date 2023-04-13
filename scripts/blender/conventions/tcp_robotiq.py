import bpy
import numpy as np

from linen.blender.frame import add_frames
from linen.blender.render_setups import setup_white_background_XZ_camera
from linen.blender.robotics.robotiq import add_robotiq

bpy.ops.object.delete()

gripper_base_closed = add_robotiq()
gripper_base_open = add_robotiq(closed=False)

gripper_base_closed.location.x -= 0.16 + 0.02
gripper_base_open.location.x += 0.04 + 0.02

gripper_base_closed.location.z += 0.15
gripper_base_open.location.z += 0.15

angle = np.deg2rad(-135.0)
gripper_base_closed.rotation_euler.y = angle
gripper_base_open.rotation_euler.y = angle

gripper_base_closed.rotation_euler.z = np.pi  # make x point up
gripper_base_open.rotation_euler.z = np.pi  # make x point up

bpy.context.view_layer.update()
closed_pose = np.array(gripper_base_closed.matrix_world)
open_pose = np.array(gripper_base_open.matrix_world)

tcp_offset = np.array([0.0, 0.0, 0.17])
tcp_transform = np.identity(4)
tcp_transform[:3, 3] = tcp_offset

closed_tcp = closed_pose @ tcp_transform
open_tcp = open_pose @ tcp_transform

add_frames([closed_tcp, open_tcp], size=0.04)

camera = setup_white_background_XZ_camera(ortho_scale=0.6)
camera.rotation_euler.x = np.deg2rad(83.6)
camera.rotation_euler.z = np.deg2rad(10.8)
camera.location = [0.197, -0.97, 0.193]

scene = bpy.context.scene
scene.render.resolution_x = 2100
scene.render.resolution_y = 700
