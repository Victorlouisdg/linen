import bpy
import numpy as np


def setup_white_background_XZ_camera(ortho_scale=1.0) -> bpy.types.Camera:
    camera = bpy.data.objects["Camera"]
    camera.location = np.array([0, -1.0, 0])
    camera.rotation_euler = np.array([np.deg2rad(90.0), 0.0, 0.0])
    camera.data.type = "ORTHO"
    camera.data.ortho_scale = ortho_scale

    scene = bpy.context.scene
    scene.render.engine = "CYCLES"
    scene.cycles.samples = 64
    scene.view_settings.view_transform = "Standard"

    bpy.data.worlds["World"].node_tree.nodes["Background"].inputs["Color"].default_value = (1.0, 1.0, 1.0, 1.0)
    return camera
