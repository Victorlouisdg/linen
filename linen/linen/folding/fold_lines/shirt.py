from typing import Dict, Tuple

import numpy as np
from airo_typing import Vector3DType


def shirt_sleeve_and_side_fold_line(
    keypoints: Dict[str, Vector3DType], left=True, offset_from_armpit_fraction=1.0 / 6.0
) -> Tuple[Vector3DType, Vector3DType]:
    """
    The vertical fold line that folds the side of a shirt inwards, including the sleeve.

          ^
          |
    +--+--|-+---+---+--+
    |     |            |
    +--+  |         +--+
        | |         |
        | |         |
        | |         |
        | |         |
        +-|---------+
          |



    Args:
        keypoints: The keypoints of the shirt.
        left: Whether to fold the left or right side.
        offset_from_armpit_fraction: The fraction of the distance between the two armpits to offset the fold line

    Returns:
        The fold line as a tuple of a point and a direction vector.

    """

    neck_left = keypoints["neck_left"]
    shoulder_left = keypoints["shoulder_left"]
    armpit_left = keypoints["armpit_left"]
    waist_left = keypoints["waist_left"]

    neck_right = keypoints["neck_right"]
    shoulder_right = keypoints["shoulder_right"]
    armpit_right = keypoints["armpit_right"]
    waist_right = keypoints["waist_right"]

    top_left = (armpit_left + shoulder_left + neck_left) / 3
    top_right = (armpit_right + shoulder_right + neck_right) / 3
    top_center = (top_left + top_right) / 2
    bottom_center = (waist_left + waist_right) / 2

    bottom_to_top = top_center - bottom_center
    bottom_to_top /= np.linalg.norm(bottom_to_top)

    if left:
        fold_line_point = armpit_left + offset_from_armpit_fraction * (armpit_right - armpit_left)
        fold_line_direction = bottom_to_top
    else:
        fold_line_point = armpit_right + offset_from_armpit_fraction * (armpit_left - armpit_right)
        fold_line_direction = -bottom_to_top

    return fold_line_point, fold_line_direction


# TODO consider this further
# def shirt_middle_fold_line(
#     keypoints: Dict[str, Vector3DType]
# ) -> Tuple[Vector3DType, Vector3DType]:
#     """
#     The horizontal fold line that folds the shirt in half.


#     +--+---+---+---+
#     |          |   |
#     +--+       +---+
#         |          |
#      <--|----------+--
#         |          |
#         |          |
#         +----------+


#     Args:
#         keypoints: The keypoints of the perfectly flattend shirt.

#     Returns:
#         The fold line as a tuple of a point and a direction vector.

#     """

#     neck_left = keypoints["neck_left"]
#     shoulder_left = keypoints["shoulder_left"]
#     armpit_left = keypoints["armpit_left"]
#     waist_left = keypoints["waist_left"]

#     neck_right = keypoints["neck_right"]
#     shoulder_right = keypoints["shoulder_right"]
#     armpit_right = keypoints["armpit_right"]
#     waist_right = keypoints["waist_right"]

#     top_left = (armpit_left + shoulder_left + neck_left) / 3
#     top_right = (armpit_right + shoulder_right + neck_right) / 3
#     top_center = (top_left + top_right) / 2
#     bottom_center = (waist_left + waist_right) / 2

#     bottom_to_top = top_center - bottom_center
#     bottom_to_top /= np.linalg.norm(bottom_to_top)

#     neck_center = (neck_left + neck_right) / 2


#     return fold_line_point, fold_line_direction
