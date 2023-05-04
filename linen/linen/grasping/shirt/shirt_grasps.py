from typing import Tuple, Dict

import numpy as np
from airo_typing import Vector3DType

def shirt_sleeve_and_waist_grasps(
    keypoints: Dict[str, Vector3DType],
    sleeve_inset = 0.05,
    waist_inset = 0.05,
    grasp_depth = 0.05,
    left=True
) -> Tuple[Tuple[Vector3DType, Vector3DType], Tuple[Vector3DType, Vector3DType]]:
    """
    The vertical fold line that fold the side of a shirt inwards, including the sleeve.

              ^
      |       |
    +-|---+---|-+---+---+-----+
    | v       |               |
    +-----+   |         +-----+
          |   |         |
          |   |         |
          |   |         |
          | ^ |         |
          +-|-|---------+
            | |



    Args:
        keypoints: The keypoints of the shirt.
    

    Returns:

    """

    neck_left = keypoints["neck_left"]
    shoulder_left = keypoints["shoulder_left"]
    armpit_left = keypoints["armpit_left"]
    waist_left = keypoints["waist_left"]
    sleeve_top_left = keypoints["sleeve_left_top"]


    neck_right = keypoints["neck_right"]
    shoulder_right = keypoints["shoulder_right"]
    armpit_right = keypoints["armpit_right"]
    waist_right = keypoints["waist_right"]
    sleeve_top_right = keypoints["sleeve_right_top"]

    top_left = (armpit_left + shoulder_left + neck_left) / 3
    top_right = (armpit_right + shoulder_right + neck_right) / 3
    top_center = (top_left + top_right) / 2
    bottom_center = (waist_left + waist_right) / 2

    bottom_to_top = top_center - bottom_center
    bottom_to_top /= np.linalg.norm(bottom_to_top)


    sleeve_grasp_approach_direction = -bottom_to_top
    waist_grasp_approach_direction = bottom_to_top

    if left:
        sleeve_to_shoulder = shoulder_left - sleeve_top_left
        sleeve_to_shoulder /= np.linalg.norm(sleeve_to_shoulder)
        sleeve_grasp_location = sleeve_top_left + sleeve_inset * sleeve_to_shoulder 
        waist_left_to_right = waist_right - waist_left
        waist_grasp_location = waist_left + waist_inset * waist_left_to_right
    else:
        sleeve_to_shoulder = shoulder_right - sleeve_top_right
        sleeve_to_shoulder /= np.linalg.norm(sleeve_to_shoulder)
        sleeve_grasp_location = sleeve_top_right + sleeve_inset * sleeve_to_shoulder
        waist_right_to_left = waist_left - waist_right
        waist_grasp_location = waist_right + waist_inset * waist_right_to_left

    # Add grasp depth
    sleeve_grasp_location += grasp_depth * sleeve_grasp_approach_direction 
    waist_grasp_location += grasp_depth * waist_grasp_approach_direction

    sleeve_grasp = (sleeve_grasp_location, sleeve_grasp_approach_direction)
    waist_grasp = (waist_grasp_location, waist_grasp_approach_direction)

    return sleeve_grasp, waist_grasp