import airo_blender as ab
import bpy
import numpy as np
import urdf_workshop

from linen.blender.path import animate_object_along_path
from linen.path.path import Path


def add_robotiq(closed=True) -> bpy.types.Object:
    """
    Adds a Robotiq 2F-85 gripper to the scene.

    Args:
        closed: Whether the gripper should be closed or open.

    Returns:
        The base of the gripper that allows posing the gripper.
    """
    gripper_joints, _, gripper_links = ab.import_urdf(urdf_workshop.robotiq_2f85)
    gripper_bases = [link for link in gripper_links.values() if link.parent is None]
    gripper_base = gripper_bases[0]

    gripper_joint = gripper_joints["finger_joint"]

    if closed:
        gripper_joint.rotation_euler = (0, 0, np.deg2rad(42))

    return gripper_base


def add_animated_robotiq(tcp_trajectory: Path, tcp_z=0.172, closed=True):
    gripper_base = add_robotiq(closed=closed)

    def gripper_base_trajectory_function(t):
        tcp_offset = np.array([0.0, 0.0, tcp_z])
        tcp_transform = np.identity(4)
        tcp_transform[:3, 3] = tcp_offset
        tcp_inverse_transform = np.linalg.inv(tcp_transform)
        return tcp_trajectory(t) @ tcp_inverse_transform

    gripper_base_trajectory = Path(
        gripper_base_trajectory_function,
        start_time=tcp_trajectory.start_time,
        end_time=tcp_trajectory.end_time,
    )

    animate_object_along_path(gripper_base, gripper_base_trajectory)
