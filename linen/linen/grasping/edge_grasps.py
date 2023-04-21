from typing import Tuple

import numpy as np
from airo_typing import Vector3DType


def orthogonal_edge_approach_direction(edge_start: Vector3DType, edge_end: Vector3DType) -> Vector3DType:
    """
    Assumes the edge is parallel to the x-y plane

                       |  approach_direction
                       v
      edge_end +<------+-------+ edge_start
               |               |

    TODO: mention the orientation convention that follows from the cross product.

    Args:
        edge_start: The first point of the edge
        edge_end: The second point of the edge

    Returns:
        The direction of the approach vector.

    """
    edge = edge_end - edge_start
    edge_direction = edge / np.linalg.norm(edge)
    up = np.array([0, 0, 1])
    approach_direction = np.cross(up, edge_direction)

    return approach_direction


def insetted_edge_grasps(
    edge_start: Vector3DType,
    edge_end: Vector3DType,
    grasp_approach_direction: Vector3DType,
    grasp_depth: float = 0.05,
    inset: float = 0.05,
) -> Tuple[Vector3DType, Vector3DType]:
    """Diagram:

                inset
    edge_start +---->+-------------------------+<----+ edge_end
               |     |  grasp_depth            |     |
               |     v                         v     |
               |-----+                         +-----|
               | grasp_location0     grasp_location1 |
               |                                     |

    Args:
        edge_start: The first point of the edge.
        edge_end: The second point of the edge.
        grasp_approach_direction: The direction of the edge will be approached. This needn't be perpendicular to the edge.
        grasp_depth: The depth of the grasp.
        inset: The distance along the edge to inset the grasp locations.

    Returns:
        The two grasp locations.
    """
    edge = edge_end - edge_start
    edge_direction = edge / np.linalg.norm(edge)

    grasp_location0 = edge_start.copy()
    grasp_location0 += inset * edge_direction
    grasp_location0 += grasp_depth * grasp_approach_direction

    grasp_location1 = edge_end.copy()
    grasp_location1 -= inset * edge_direction
    grasp_location1 += grasp_depth * grasp_approach_direction

    return grasp_location0, grasp_location1


def orthogonal_insetted_edge_grasps(
    edge_start: Vector3DType,
    edge_end: Vector3DType,
    grasp_depth: float = 0.05,
    inset: float = 0.05,
):
    """
       |  |
    1--|--|--0
    |  v  v  |
    |  x  x  |
    |        |

    Args:
        edge_start: The first point of the edge.
        edge_end: The second point of the edge.
        grasp_depth: The depth of the grasp.
        inset: The distance along the edge to inset the grasp locations.

    Returns:
        The two grasps, each of which is a tuple of the grasp location and the approach direction.


    """
    approach_direction = orthogonal_edge_approach_direction(edge_start, edge_end)
    grasp_location0, grasp_location1 = insetted_edge_grasps(
        edge_start, edge_end, approach_direction, grasp_depth, inset
    )
    return (grasp_location0, approach_direction), (grasp_location1, approach_direction)
