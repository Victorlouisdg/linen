from typing import List

import numpy as np

from linen.grasping.edge_grasps import orthogonal_insetted_edge_grasps


def towel_aligned_grasps(ordered_keypoints, grasp_depth=0.05, inset=0.05):
    """Two parallel grasps on the same edge.

       |  |
    1--|--|--0
    |  v  v  |
    |  x  x  |
    |        |
    |        |
    2--------3

    Args:
        ordered_keypoints: The keypoints of the towel ordered counterclockwise.
        grasp_depth: The depth of the grasp.
        inset: The distance along the edge to inset the grasp locations.

    Returns:
        The two grasp locations, the first will be the grasp at the top edge of the towel.

    """

    # TODO: Do we need to grasp other edges of the towel?
    edge_start = ordered_keypoints[0]
    edge_end = ordered_keypoints[1]
    return orthogonal_insetted_edge_grasps(edge_start, edge_end, grasp_depth, inset)


def towel_twisted_grasps(ordered_keypoints: List[np.ndarray], grasp_depth: float = 0.05, inset: float = 0.05):
    """Two opposing grasps that are also not aliged with each other.

    1-----------|-->0
    |           v   |
    |           x   |
    |   x           |
    |   ^           |
    2---|---------->3


    Args:
        ordered_keypoints: The keypoints of the towel ordered counterclockwise.
        grasp_depth: The depth of the grasp.
        inset: The distance along the edge to inset the grasp locations.

    Returns:
        The two grasp locations, the first will be the grasp at the top edge of the towel.


    """
    left_top_to_bottom = ordered_keypoints[3] - ordered_keypoints[0]
    right_bottom_to_top = ordered_keypoints[1] - ordered_keypoints[2]

    approach_direction_left = left_top_to_bottom
    approach_direction_right = right_bottom_to_top

    approach_direction_left[2] = 0
    approach_direction_right[2] = 0
    approach_direction_left /= np.linalg.norm(approach_direction_left)
    approach_direction_right /= np.linalg.norm(approach_direction_right)

    top_right_to_left = ordered_keypoints[1] - ordered_keypoints[0]
    top_right_to_left /= np.linalg.norm(top_right_to_left)

    bottom_left_to_right = ordered_keypoints[3] - ordered_keypoints[2]
    bottom_left_to_right /= np.linalg.norm(bottom_left_to_right)

    location_left = ordered_keypoints[0] + 0.05 * top_right_to_left + grasp_depth * approach_direction_left
    location_right = ordered_keypoints[2] + 0.05 * bottom_left_to_right + grasp_depth * approach_direction_right

    grasp_left = (location_left, approach_direction_left)
    grasp_right = (location_right, approach_direction_right)

    return grasp_left, grasp_right


# def towel_opposing_grasps(ordered_keypoints, parallel_near_edge=(0, 1)):
#     """TODO: implement

#       1------->0
#       |        |
#     ---->x  x<----
#       |        |
#       |        |
#       |        |
#       2------->3
#     """
