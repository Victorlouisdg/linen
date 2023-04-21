from typing import List

import numpy as np


def towel_fold_line(ordered_keypoints: List[np.ndarray]):
    """
        1------>0
        |       |
        |       |
    ----+---c---+----> d
        |       |
        |       |
        2------>3

    Args:
        ordered_keypoints: The keypoints of the towel ordered counterclockwise.

    Returns:
        The center of the towel and the direction of the fold line.

    """
    top_edge = ordered_keypoints[0] - ordered_keypoints[1]
    top_edge_direction = top_edge / np.linalg.norm(top_edge)

    bottom_edge = ordered_keypoints[3] - ordered_keypoints[2]
    bottom_edge_direction = bottom_edge / np.linalg.norm(bottom_edge)

    towel_center = np.mean(ordered_keypoints, axis=0)
    fold_line_direction = (top_edge_direction + bottom_edge_direction) / 2

    return towel_center, fold_line_direction


# TODO: create fold lines for towel independently of keypoint order e.g.
# def towel_fold_line_middle_short(towel_keypoints):
#
#         +-------+
#         |       |
#         |       |
#     ----+-------+---->
#         |       |
#         |       |
#         +-------+
