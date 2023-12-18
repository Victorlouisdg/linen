from typing import Tuple

import numpy as np
from airo_typing import Vector3DType


def project_point_on_line(point: Vector3DType, line: Tuple[Vector3DType, Vector3DType]) -> Vector3DType:
    """
    Projects a point on a line.

    Args:
        point: The point to project.
        line: The line w.r.t. which the point is projected. The line is defined by a point and a direction

    Returns:
        The projected point.
    """
    point = np.array(point)
    line = np.array(line)
    point_on_line, line_direction = line  # TODO maybe add line as airo-typing type?
    line_direction = line_direction / np.linalg.norm(line_direction)
    dot = np.dot(point - point_on_line, line_direction)
    return point_on_line + dot * line_direction
