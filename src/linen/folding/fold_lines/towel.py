from typing import List

import numpy as np


def towel_fold_line(ordered_keypoints: List[np.ndarray], grasped_edge: int = 0):
    """
    The fold line that fold the towel in half.

    Example when grasped_edge == 0:

        1<------0
        |       ^
        |       |
    ----+---c---+----> d
        |       |
        v       |
        2------>3

    Args:
        ordered_keypoints: The keypoints of the towel ordered counterclockwise.
        grasped_edge: The edge that is grasped (must be between 0 and 3).

    Returns:
        The fold line as a tuple of a point on the line and a direction vector.
    """

    edges = [(0, 1), (1, 2), (2, 3), (3, 0)]  # edge 0, 1, 2, 3

    towel_center = np.mean(ordered_keypoints, axis=0)

    edge_directions = []
    for edge in edges:
        start, end = edge
        edge_direction = ordered_keypoints[end] - ordered_keypoints[start]
        edge_direction /= np.linalg.norm(edge_direction)
        edge_directions.append(edge_direction)

    # Here we average the direction of the two edges parallel to the grasped edge.
    # Not that we need to flip some sign to make the sure the directions don't cancel out,
    # and such that the direction of rotation is correct.
    if grasped_edge == 0:
        fold_line_direction = (-edge_directions[0] + edge_directions[2]) / 2
    elif grasped_edge == 1:
        fold_line_direction = (-edge_directions[1] + edge_directions[3]) / 2
    elif grasped_edge == 2:
        fold_line_direction = (edge_directions[0] - edge_directions[2]) / 2
    elif grasped_edge == 3:
        fold_line_direction = (edge_directions[1] - edge_directions[3]) / 2

    fold_line_direction /= np.linalg.norm(fold_line_direction)

    return towel_center, fold_line_direction
