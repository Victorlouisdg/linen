from airo_camera_toolkit.cameras.zed2i import Zed2i

from linen.opencv.annotation import Annotation, get_manual_annotations

observation_spec = {
    "grasp_location": Annotation.Keypoint,
    "line_segment": Annotation.LineSegment,
    "line": Annotation.Line,
    "box": Annotation.BoundingBox,
}

zed = Zed2i(resolution=Zed2i.RESOLUTION_720, fps=30)
annotations = get_manual_annotations(zed, observation_spec)

for name, annotation in annotations.items():
    print(f"{name}: {annotation}")
