from typing import List

import numpy as np
from airo_typing import Vector3DType


def angle_2D(v0, v1):
    # TODO: document.
    x1, y1, *_ = v0
    x2, y2, *_ = v1
    dot = x1 * x2 + y1 * y2  # dot product between [x1, y1] and [x2, y2]
    det = x1 * y2 - y1 * x2  # determinant
    angle = np.arctan2(det, dot)  # atan2(y, x) or atan2(sin, cos)
    return angle


def get_counterclockwise_ordered_keypoints(keypoints: List[Vector3DType]) -> List[Vector3DType]:
    """
    Orders keypoints according to their angle w.r.t. a frame that is created by translating the world frame to the center of the cloth.
    the first keypoints is the one with the smallest, positive angle and they are sorted counter-clockwise.

    1---0
    |  /|
    | . |
    |   |
    2---3

    y
    |
    +--x

    Args:
        keypoints: The keypoints to order.

    Returns:
        The keypoints ordered counterclockwise.

    """
    keypoints = np.array(keypoints)
    center = np.mean(keypoints, axis=0)
    x_axis = np.array([1, 0])
    angles = [angle_2D(x_axis, keypoint - center) for keypoint in keypoints]
    angles = [angle % (2 * np.pi) for angle in angles]  # make angles positive from 0 to 2*pi
    keypoints_sorted = keypoints[np.argsort(angles)]
    return list(keypoints_sorted)
