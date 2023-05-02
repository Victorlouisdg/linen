from typing import Dict, Tuple

import numpy as np
from airo_typing import Vector3DType


def shirt_sleeve_and_side_fold_line(keypoints: Dict[str, Vector3DType]) -> Tuple[Vector3DType, Vector3DType]:
    """
    The vertical fold line that fold the side of a shirt inwards, including the sleeve.

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

    return bottom_center, bottom_to_top

    # TODO determine where to lie the fold line?
    # armpit_left + 0.25 * (armpit_right - armpit_left)?
