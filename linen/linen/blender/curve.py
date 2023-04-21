import bpy
import numpy as np


def add_discrete_curve_mesh(points: np.ndarray, closed=False) -> bpy.types.Object:
    """Add a discrete curve as a mesh of edges between consecutive points.

    Args:
        points: The consecutive points of the curve.
        closed: Whether the curve is closed, i.e. whether the last point should be connect to the first.

    Returns:
        The object representing the curve.
    """
    edges = [(i, i + 1) for i in range(len(points) - 1)]
    if closed:
        edges.append((len(points) - 1, 0))
    mesh = bpy.data.meshes.new("Curve")
    mesh.from_pydata(points, edges, [])
    mesh.update()
    curve = bpy.data.objects.new("Curve", mesh)
    bpy.context.collection.objects.link(curve)
    return curve


def skin(object: bpy.types.Object, radius: float = 0.005):
    """Add a skin and subdivision modifier to ab object. Also sets the radius of the skin vertices."""
    object.modifiers.new(name="Skin", type="SKIN")
    object.modifiers.new(name="Subdivision", type="SUBSURF")

    for vertex in object.data.vertices:
        skin_vertex = object.data.skin_vertices[""].data[vertex.index]
        skin_vertex.radius = (radius, radius)


def add_discrete_curve(points: np.ndarray, closed=False, thickness_radius: float = 0.005):
    """Add a discrete curve as a mesh of edges between consecutive points.

    Args:
        points: The consecutive points of the curve.
        closed: Whether the curve is closed, i.e. whether the last point should be connect to the first.
        thickness_radius: The radius of the skin vertices.

    Returns:
        The object representing the curve.
    """
    curve = add_discrete_curve_mesh(points, closed)
    skin(curve, thickness_radius)
    return curve


def add_line_segment(start, end):
    return add_discrete_curve([start, end])
