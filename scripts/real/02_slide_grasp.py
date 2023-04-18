import os
import sys
from pathlib import Path

import cv2
import numpy as np
from airo_camera_toolkit.cameras.zed2i import Zed2i
from airo_camera_toolkit.reprojection import reproject_to_frame_z_plane
from airo_camera_toolkit.utils import ImageConverter
from airo_dataset_tools.pose import Pose
from airo_robots.grippers.hardware.robotiq_2f85_urcap import Robotiq2F85
from airo_robots.manipulators.hardware.ur_rtde import URrtde
from airo_spatial_algebra import SE3Container

from linen.grasping.slide_grasp import slide_grasp_trajectory
from linen.opencv.annotation import Annotation, get_manual_annotations, visualize_finished_annotations


### Functions that need to go somewhere else
def load_extrinsics(path="camera_pose.json") -> np.ndarray:
    if not os.path.exists(path):
        path_relative_to_script = Path(__file__).parent / "camera_pose.json"
        if not os.path.exists(path_relative_to_script):
            return None

    pose_saved = Pose.parse_file("camera_pose.json")
    position = pose_saved.position_in_meters
    euler_angles = pose_saved.rotation_euler_xyz_in_radians

    position_array = np.array([position.x, position.y, position.z])
    euler_angles_array = np.array([euler_angles.roll, euler_angles.pitch, euler_angles.yaw])

    camera_in_base = SE3Container.from_euler_angles_and_translation(
        euler_angles_array, position_array
    ).homogeneous_matrix
    return camera_in_base


def draw_pose(image, pose_in_base, camera_in_base, intrinsics):
    pose_in_camera = np.linalg.inv(camera_in_base) @ pose_in_base
    rvec = pose_in_camera[:3, :3]
    tvec = pose_in_camera[:3, -1]
    image = cv2.drawFrameAxes(image, intrinsics, np.zeros(4), rvec, tvec, 0.1)
    return image


def execute_open_loop_trajectory(trajectory: Path, robot, control_period=0.01):
    t = 0.0
    while t < trajectory.duration:
        robot.servo_to_tcp_pose(trajectory(t), control_period).wait()
        t += control_period
    robot.rtde_control.servoStop()


### End of functions that need to go somewhere else

camera_in_base = load_extrinsics()
if camera_in_base is None:
    print("Could not load camera pose.")
    sys.exit()


### Move robot to home
robot_ip = "10.42.0.162"
gripper = Robotiq2F85(robot_ip)
robot = URrtde(robot_ip, URrtde.UR3E_CONFIG, gripper)

home_joints_ur5e_split_left = np.deg2rad([-180, -45, -95, -130, 90, 90])
home_joints = home_joints_ur5e_split_left

robot.move_to_joint_configuration(home_joints, joint_speed=1.0).wait()
robot.gripper.open().wait()

# Annotations
annotation_spec = {
    "slide": Annotation.LineSegment,
}

zed = Zed2i(resolution=Zed2i.RESOLUTION_720, fps=30)
annotations = get_manual_annotations(zed, annotation_spec)

if annotations is None:
    sys.exit()

intrinsics_matrix = zed.intrinsics_matrix()

### The interesting part: creation of the slide_grasp
table_height_offset = -0.02

points_in_image = np.array(annotations["slide"])
points_in_world = reproject_to_frame_z_plane(points_in_image, intrinsics_matrix, camera_in_base, table_height_offset)
slide_start = points_in_world[0]
slide_end = points_in_world[1]

grasp_approach_direction = slide_end - slide_start
approach_distance = np.linalg.norm(grasp_approach_direction)
grasp_approach_direction /= approach_distance

speed = 0.1
hover_height = 0.05
approach_angle = np.pi / 4

grasp_location = slide_end + np.array([0, 0, 0.05])  # above table for initial testing

grasp_trajectory = slide_grasp_trajectory(
    grasp_location,
    grasp_approach_direction,
    approach_distance,
    approach_angle,
    hover_height,
    speed,
)
###

window_name = "Camera feed"
cv2.namedWindow(window_name)

while True:
    _, h, w = zed.get_rgb_image().shape
    image = zed.get_rgb_image()
    image = ImageConverter(image).image_in_opencv_format

    image = draw_pose(image, np.identity(4), camera_in_base, intrinsics_matrix)
    image = draw_pose(image, grasp_trajectory.start, camera_in_base, intrinsics_matrix)
    image = draw_pose(image, grasp_trajectory.end, camera_in_base, intrinsics_matrix)
    image = visualize_finished_annotations(image, annotations, annotation_spec)

    banner_text = "Press 'Enter' to execute slide grasp."
    cv2.putText(
        image,
        banner_text,
        (10, 30),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 255, 0),
        2,
    )

    cv2.imshow(window_name, image)
    key = cv2.waitKey(10)

    if key == ord("q"):
        cv2.destroyAllWindows()
        break

    if key == 13:
        start_pose = grasp_trajectory.start
        robot.move_to_tcp_pose(start_pose, joint_speed=0.4).wait()

        execute_open_loop_trajectory(grasp_trajectory, robot)
        gripper.close().wait()

        # Ad hoc adding end pose
        end_pose = grasp_trajectory(grasp_trajectory.duration)
        retreat_pose = end_pose.copy()
        retreat_pose[2, 3] += 0.1

        robot.move_linear_to_tcp_pose(retreat_pose).wait()
        gripper.open().wait()

        robot.move_to_joint_configuration(home_joints, joint_speed=1.0).wait()

        cv2.destroyAllWindows()
        break
