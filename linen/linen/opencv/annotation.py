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
    point1: Tuple[int, int],
    color=(255, 255, 0),
) -> np.ndarray:
    line_start = np.array(point0)
    line_end = np.array(point1)
    line_direction = line_end - line_start
    line_length = np.linalg.norm(line_direction)
    if line_length == 0:
        return image
    line_direction = line_direction / line_length
    line_start = line_start - line_direction * 10000
    line_end = line_end + line_direction * 10000
    line_start = tuple(line_start.astype(int))
    line_end = tuple(line_end.astype(int))
    image = cv2.line(image, line_start, line_end, color, 1)
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
        annotation = clicked_points[0], clicked_points[1]

    if annotation_type == Annotation.BoundingBox:
        annotation = clicked_points[0], clicked_points[1]

    return [], annotation  # Reset the clicked points


def visualize_finished_annotations(image: np.ndarray, annotations: dict, annotation_spec) -> np.ndarray:
    """Visualize the finished annotations on the image."""

    for name, annotation in annotations.items():
        annotation_type = annotation_spec[name]

        if annotation_type == Annotation.Keypoint:
            point = annotation
            text_location = (annotation[0] + 8, annotation[1])
            image = cv2.circle(image, point, 3, (255, 255, 0), -1)
            image = cv2.putText(
                image,
                name,
                text_location,
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                (255, 255, 0),
                1,
            )
        if annotation_type == Annotation.LineSegment:
            point1, point2 = annotation
            text_location = (annotation[0][0] + 8, annotation[0][1])
            image = cv2.circle(image, point1, 3, (255, 255, 0), -1)
            image = cv2.circle(image, point2, 3, (255, 255, 0), -1)
            image = cv2.line(image, point1, point2, (255, 255, 0), 1)
            image = cv2.putText(
                image,
                name,
                text_location,
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                (255, 255, 0),
                1,
            )

        if annotation_type == Annotation.Line:
            # only draw first point and then the line that extend over the full image
            point0, point1 = annotation
            image = draw_infinite_line(image, point0, point1)
            image = cv2.circle(image, point0, 3, (255, 255, 0), -1)
            image = cv2.putText(
                image,
                name,
                text_location,
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                (255, 255, 0),
                1,
            )

        if annotation_type == Annotation.BoundingBox:
            point1, point2 = annotation
            text_location = (annotation[0][0] + 8, annotation[0][1])
            image = cv2.rectangle(image, point1, point2, (255, 255, 0), 1)
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


def visualize_current_annotation(
    image: np.ndarray,
    annotation_name: str,
    annotation_type: Annotation,
    current_mouse_point: Tuple[int, int],
    clicked_points: List[Tuple[int, int]],
) -> np.ndarray:
    """Visualize the current annotation on the image."""

    if annotation_type == Annotation.Keypoint:
        text = f"Click to annotate keypoint: {annotation_name}"

    if annotation_type == Annotation.LineSegment:
        text = f"Click to annotate line segment: {annotation_name}"

        if len(clicked_points) == 1:
            point = clicked_points[0]
            image = cv2.circle(image, point, 3, (0, 255, 0), -1)
            # draw a line between the point and the current mouse position
            image = cv2.line(image, point, current_mouse_point, (0, 255, 0), 1)

    if annotation_type == Annotation.Line:
        text = f"Click to annotate line: {annotation_name}"

        if len(clicked_points) == 1:
            point0 = clicked_points[0]
            point1 = current_mouse_point
            print(point0)
            print(point1)
            image = cv2.circle(image, point0, 3, (0, 255, 0), -1)
            image = draw_infinite_line(image, point0, point1, color=(0, 255, 0))

    if annotation_type == Annotation.BoundingBox:
        text = f"Click to annotate bounding box: {annotation_name}"

        if len(clicked_points) == 1:
            point1 = clicked_points[0]
            point2 = current_mouse_point
            image = cv2.rectangle(image, point1, point2, (0, 255, 0), 1)

    cv2.putText(image, text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    return image


def get_manual_annotations(camera: Camera, annotation_spec: dict) -> dict:
    current_mouse_point = [(0, 0)]  # has to be a list so that the callback can edit it
    clicked_points = []

    def mouse_callback(event, x, y, flags, parm):
        if event == cv2.EVENT_LBUTTONDOWN:
            clicked_points.append((x, y))
        elif event == cv2.EVENT_MOUSEMOVE:
            current_mouse_point[0] = x, y

    window_name = "Annotation window"
    cv2.namedWindow(window_name)
    cv2.setMouseCallback(window_name, mouse_callback)

    annotation_names = list(annotation_spec.keys())
    annotation_types = list(annotation_spec.values())
    num_annotations = len(annotation_names)
    annotations = {}
    current_id = 0

    while True:
        _, h, w = camera.get_rgb_image().shape
        image = camera.get_rgb_image()

        image = ImageConverter(image).image_in_opencv_format

        print(len(clicked_points))

        # Process and draw
        current_name = annotation_names[current_id]
        current_type = annotation_types[current_id]

        clicked_points, annotation = process_clicked_points(current_type, clicked_points)

        if annotation is not None:
            annotations[current_name] = annotation
            current_id += 1
            if current_id >= num_annotations:
                return annotations

        image = visualize_finished_annotations(image, annotations, annotation_spec)
        image = visualize_current_annotation(image, current_name, current_type, current_mouse_point[0], clicked_points)

        cv2.imshow(window_name, image)
        key = cv2.waitKey(10)

        if key == ord("q"):
            cv2.destroyAllWindows()
            return None
