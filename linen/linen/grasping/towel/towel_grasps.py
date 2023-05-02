from typing import List

import numpy as np

from linen.grasping.edge_grasps import orthogonal_insetted_edge_grasps


def towel_aligned_grasps(ordered_keypoints, grasp_depth=0.05, inset=0.05, grasped_edge: int = 0):
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
        grasped_edge: The edge to grasp.

    Returns:
        The two grasp locations on the selected edge.

    """

    # TODO: Do we need to grasp other edges of the towel?
    edges = [(0, 1), (1, 2), (2, 3), (3, 0)]  # edge 0, 1, 2, 3
    start, end = edges[grasped_edge]
    edge_start = ordered_keypoints[start]
    edge_end = ordered_keypoints[end]
    return orthogonal_insetted_edge_grasps(edge_start, edge_end, grasp_depth, inset)


def towel_twisted_grasps(
    ordered_keypoints: List[np.ndarray], grasp_depth: float = 0.05, inset: float = 0.05, top_grasp_near0: bool = True
):
    """Two opposing grasps that are also not aliged with each other.


    Option 1:           Option 2:

    1-----------|-->0    1---|---------->0
    |           v   |    |   v           |
    |           x   |    |   x           |
    |   x           |    |           x   |
    |   ^           |    |           ^   |
    2---|---------->3    2-----------|-->3


    Args:
        ordered_keypoints: The keypoints of the towel ordered counterclockwise.
        grasp_depth: The depth of the grasp.
        inset: The distance along the edge to inset the grasp locations.
        top_grasp_near0: Whether the grasp at the top edge of the towel should be near the first keypoint.

    Returns:
        The two grasp locations, the first will be the grasp at the top edge of the towel.

    """

    left_bottom_to_top = ordered_keypoints[1] - ordered_keypoints[2]
    right_bottom_to_top = ordered_keypoints[0] - ordered_keypoints[3]

    bottom_to_top = (left_bottom_to_top + right_bottom_to_top) / 2
    bottom_to_top /= np.linalg.norm(bottom_to_top)

    approach_direction_top = -bottom_to_top
    approach_direction_bottom = bottom_to_top

    # Project and normalize
    approach_direction_top[2] = 0
    approach_direction_bottom[2] = 0
    approach_direction_top /= np.linalg.norm(approach_direction_top)
    approach_direction_bottom /= np.linalg.norm(approach_direction_bottom)

    top_left_to_right = ordered_keypoints[0] - ordered_keypoints[1]
    bottom_left_to_right = ordered_keypoints[3] - ordered_keypoints[2]
    left_to_right = (top_left_to_right + bottom_left_to_right) / 2
    left_to_right /= np.linalg.norm(left_to_right)

    if top_grasp_near0:
        location_top = ordered_keypoints[0] - inset * left_to_right
        location_bottom = ordered_keypoints[2] + inset * left_to_right
    else:
        location_top = ordered_keypoints[1] + inset * left_to_right
        location_bottom = ordered_keypoints[3] - inset * left_to_right

    location_top += grasp_depth * approach_direction_top
    location_bottom += grasp_depth * approach_direction_bottom

    grasp_top = (location_top, approach_direction_top)
    grasp_bottom = (location_bottom, approach_direction_bottom)

    return grasp_top, grasp_bottom


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
