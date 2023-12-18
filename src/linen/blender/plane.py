import bpy


def add_plane(width: float, length: float):
    bpy.ops.mesh.primitive_plane_add()
    plane = bpy.context.object
    plane.scale = (width / 2.0, length / 2.0, 1)
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    return plane
