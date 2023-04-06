import airo_blender as ab
import bpy
import numpy as np


def add_points(points: np.ndarray, radius: float = 0.005, color: tuple = None) -> bpy.types.Object:
    """Adds points to the scene as spheres.

    Args:
        points: The locations of the points.
        radius: The radius of the spheres.
        color: The color of the spheres. If specified, a material will be added to the spheres.

    Returns:
        The object from which all spheres are instanced (which we name the "template"). This is useful for controlling
        all the instanced spheres together, e.g. adding a material yourself.
    """

    # Save the active collection as we will temporarily change it to add the instances etc.
    view_layer = bpy.context.view_layer
    collection_originally_active = view_layer.active_layer_collection

    template_collection = bpy.data.collections.new("Point template")
    bpy.context.scene.collection.children.link(template_collection)
    view_layer.active_layer_collection = view_layer.layer_collection.children[template_collection.name]
    bpy.context.view_layer.update()
    bpy.ops.mesh.primitive_ico_sphere_add(scale=(radius, radius, radius))
    template = bpy.context.object

    # Make new collection to group the instances
    instances_collection = bpy.data.collections.new("Point instances")
    bpy.context.scene.collection.children.link(instances_collection)
    view_layer.active_layer_collection = view_layer.layer_collection.children[instances_collection.name]

    # Add instances of the sphere
    for point in points:
        bpy.ops.object.collection_instance_add(collection=template_collection.name, location=point)
        instance_empty = bpy.context.object
        instance_empty.empty_display_size = radius * 1.5

    # Add a material to the template if a color was specified
    if color is not None:
        ab.add_material(template, color)

    # Hide the template itself
    view_layer.layer_collection.children.get(template_collection.name).exclude = True

    # Restore the active collection
    view_layer.active_layer_collection = collection_originally_active

    return template
