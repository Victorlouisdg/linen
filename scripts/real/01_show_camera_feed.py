import cv2
from airo_camera_toolkit.cameras.zed2i import Zed2i
from airo_camera_toolkit.utils import ImageConverter

zed = Zed2i(resolution=Zed2i.RESOLUTION_720, fps=30)

window_name = "Camera feed"
cv2.namedWindow(window_name)

while True:
    _, h, w = zed.get_rgb_image().shape
    image = zed.get_rgb_image()
    image = ImageConverter(image).image_in_opencv_format
    cv2.imshow(window_name, image)  # refresh image
    key = cv2.waitKey(10)

    if key == ord("q"):
        cv2.destroyAllWindows()
        break
