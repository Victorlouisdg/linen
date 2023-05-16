from enum import Enum
from typing import List, Tuple

import cv2
import numpy as np
from airo_camera_toolkit.interfaces import Camera
from airo_camera_toolkit.utils import ImageConverter


class Annotation(Enum):
    """Enum for the different types of annotations"""

    Keypoint = 0
    LineSegment = 1
    Line = 2
    BoundingBox = 3


num_clicks_required = {
    Annotation.Keypoint: 1,
    Annotation.LineSegment: 2,
    Annotation.Line: 2,
    Annotation.BoundingBox: 2,
}


def draw_infinite_line(
    image: np.ndarray,
    point0: Tuple[int, int],
    direction: Tuple[int, int],
    color: Tuple[int, int, int] = (255, 255, 0),
) -> np.ndarray:
    point = np.array(point0)
    line_start = point - np.array(direction) * 1000
    line_end = point + np.array(direction) * 1000
    line_start = tuple(line_start.astype(int))
    line_end = tuple(line_end.astype(int))
    image = cv2.line(image, line_start, line_end, color, 1)  # Arrow is currently off screen
    return image


def draw_keypoint_annotation(
    image: np.ndarray,
    point: Tuple[int, int],
    name: str,
    color: Tuple[int, int, int] = (0, 255, 0),
) -> np.ndarray:
    text_location = (point[0] + 8, point[1])
    image = cv2.circle(image, point, 3, color, -1)
    image = cv2.putText(
        image,
        name,
        text_location,
        cv2.FONT_HERSHEY_SIMPLEX,
        0.5,
        (255, 255, 0),
        1,
    )
    return image


def draw_line_segment_annotation(
    image: np.ndarray,
    point0: Tuple[int, int],
    point1: Tuple[int, int],
    name: str,
    color: Tuple[int, int, int] = (0, 255, 0),
) -> np.ndarray:
    text_location_start = (point0[0] + 8, point0[1])
    image = cv2.circle(image, point0, 3, color, -1)
    image = cv2.circle(image, point1, 3, color, -1)
    image = cv2.line(image, point0, point1, color, 1)
    image = cv2.putText(
        image,
        f"{name}_start",
        text_location_start,
        cv2.FONT_HERSHEY_SIMPLEX,
        0.5,
        color,
        1,
    )
    text_location_end = (point1[0] + 8, point1[1])
    image = cv2.putText(
        image,
        f"{name}_end",
        text_location_end,
        cv2.FONT_HERSHEY_SIMPLEX,
        0.5,
        color,
        1,
    )
    return image


def draw_line_annotation(
    image: np.ndarray,
    point0: Tuple[int, int],
    direction: Tuple[int, int],
    name: str,
    color: Tuple[int, int, int] = (0, 255, 0),
) -> np.ndarray:
    text_location = (point0[0] + 8, point0[1])
    image = cv2.circle(image, point0, 3, color, -1)
    image = draw_infinite_line(image, point0, direction, color)
    image = cv2.putText(
        image,
        name,
        text_location,
        cv2.FONT_HERSHEY_SIMPLEX,
        0.5,
        color,
        1,
    )
    return image


def draw_bounding_box_annotation(
    image: np.ndarray,
    point0: Tuple[int, int],
    point1: Tuple[int, int],
    name: str,
    color: Tuple[int, int, int] = (0, 255, 0),
) -> np.ndarray:
    text_location = (point0[0] + 8, point0[1])
    image = cv2.circle(image, point0, 3, color, -1)
    image = cv2.circle(image, point1, 3, color, -1)
    image = cv2.rectangle(image, point0, point1, color, 1)
    image = cv2.putText(
        image,
        name,
        text_location,
        cv2.FONT_HERSHEY_SIMPLEX,
        0.5,
        color,
        1,
    )
    return image


def process_clicked_points(annotation_type: Annotation, clicked_points: list) -> tuple:
    """Process the clicked points into the annotations dictionary."""

    # Early exit if we don't have enough points
    if len(clicked_points) < num_clicks_required[annotation_type]:
        return clicked_points, None

    if annotation_type == Annotation.Keypoint:
        annotation = clicked_points[0]

    if annotation_type == Annotation.LineSegment:
        annotation = clicked_points[0], clicked_points[1]

    if annotation_type == Annotation.Line:
        direction = tuple(np.array(clicked_points[1]) - np.array(clicked_points[0]))
        annotation = clicked_points[0], direction

    if annotation_type == Annotation.BoundingBox:
        annotation = clicked_points[0], clicked_points[1]

    return [], annotation  # Reset the clicked points


def visualize_finished_annotations(image: np.ndarray, annotations: dict, annotation_spec) -> np.ndarray:
    """Visualize the finished annotations on the image."""
    cyan = (255, 255, 0)

    for name, annotation in annotations.items():
        annotation_type = annotation_spec[name]
        if annotation_type == Annotation.Keypoint:
            draw_keypoint_annotation(image, annotation, name, cyan)
        if annotation_type == Annotation.LineSegment:
            draw_line_segment_annotation(image, annotation[0], annotation[1], name, cyan)
        if annotation_type == Annotation.Line:
            draw_line_annotation(image, annotation[0], annotation[1], name, cyan)
        if annotation_type == Annotation.BoundingBox:
            draw_bounding_box_annotation(image, annotation[0], annotation[1], name, cyan)

    return image


def visualize_current_annotation(
    image: np.ndarray,
    annotation_name: str,
    annotation_type: Annotation,
    current_mouse_point: Tuple[int, int],
    clicked_points: List[Tuple[int, int]],
) -> np.ndarray:
    """Visualize the current annotation on the image."""

    if annotation_type == Annotation.Keypoint:
        banner_text = f"Click to annotate keypoint: {annotation_name}"

    if annotation_type == Annotation.LineSegment:
        banner_text = f"Click to annotate line segment: {annotation_name}"

        if len(clicked_points) == 1:
            draw_line_segment_annotation(image, clicked_points[0], current_mouse_point, annotation_name)

    if annotation_type == Annotation.Line:
        banner_text = f"Click to annotate line: {annotation_name}"

        if len(clicked_points) == 1:
            direction = tuple(np.array(current_mouse_point) - np.array(clicked_points[0]))
            draw_line_annotation(image, clicked_points[0], direction, annotation_name)

    if annotation_type == Annotation.BoundingBox:
        banner_text = f"Click to annotate bounding box: {annotation_name}"

        if len(clicked_points) == 1:
            draw_bounding_box_annotation(image, clicked_points[0], current_mouse_point, annotation_name)

    cv2.putText(image, banner_text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    return image


def get_manual_annotations(camera: Camera, annotation_spec: dict[str, Annotation]) -> dict:
    current_mouse_point = [(0, 0)]  # has to be a list so that the callback can edit it
    clicked_points = []

    def mouse_callback(event, x, y, flags, parm):
        if event == cv2.EVENT_LBUTTONDOWN:
            clicked_points.append((x, y))
        elif event == cv2.EVENT_MOUSEMOVE:
            current_mouse_point[0] = x, y

    window_name = "Annotation window"
    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
    cv2.setMouseCallback(window_name, mouse_callback)

    annotation_names = list(annotation_spec.keys())
    annotation_types = list(annotation_spec.values())
    num_annotations = len(annotation_names)
    annotations = {}
    current_id = 0

    while True:
        image = camera.get_rgb_image()
        # image = ImageConverter(image).image_in_opencv_format # TODO: investigate why this doesn't work
        image = ImageConverter.from_numpy_format(image).image_in_opencv_format

        if current_id >= num_annotations:
            banner_text = "All annotations collected. Press 'Enter' to confirm."
            cv2.putText(
                image,
                banner_text,
                (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 255, 0),
                2,
            )
        else:
            # Process and draw
            current_name = annotation_names[current_id]
            current_type = annotation_types[current_id]

            clicked_points, annotation = process_clicked_points(current_type, clicked_points)

            if annotation is not None:
                annotations[current_name] = annotation
                current_id += 1

            image = visualize_current_annotation(
                image,
                current_name,
                current_type,
                current_mouse_point[0],
                clicked_points,
            )

        image = visualize_finished_annotations(image, annotations, annotation_spec)

        cv2.imshow(window_name, image)
        key = cv2.waitKey(10)

        if key == ord("q"):
            cv2.destroyAllWindows()
            return None

        # Enter key
        if key == 13 and current_id >= num_annotations:
            cv2.destroyAllWindows()
            return annotations


if __name__ == "__main__":
    import pprint

    from airo_camera_toolkit.cameras.zed2i import Zed2i

    camera = Zed2i(resolution=Zed2i.RESOLUTION_720, fps=30)
    annotation_spec = {
        "keypoint": Annotation.Keypoint,
        "line_segment": Annotation.LineSegment,
        "line": Annotation.Line,
        "bounding_box": Annotation.BoundingBox,
    }
    annotations = get_manual_annotations(camera, annotation_spec)

    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(annotations)
