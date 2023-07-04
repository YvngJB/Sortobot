""" 
First install on PI
sudo apt update
sudo apt install python3-opencv
sudo apt install python3-numpy
"""


import cv2
import numpy as np
from PIL import Image
import keyboard
import time

class Camera:
    def __init__(self, camera_index=0) -> None:
        self._camera = cv2.VideoCapture(camera_index)
        self._last_capture_time = 0

    def _capture(self, absolute_path: str) -> None:
        current_time = time.time()
        if current_time - self._last_capture_time >= 3:
            ret, frame = self._camera.read()
            if ret:
                height, width, _ = frame.shape
                center_x, center_y = width // 2, height // 2
                crop_size = 250
                crop = frame[center_y - crop_size // 2: center_y + crop_size // 2,
                             center_x - crop_size // 2: center_x + crop_size // 2]
                cv2.imwrite(absolute_path, crop)
                self._last_capture_time = current_time

    def _get_rgb(self) -> tuple:
        try:
            self._capture("temp.jpg")
            img = cv2.imread("temp.jpg")
            img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

            lower_red = np.array([0, 50, 50])
            upper_red = np.array([10, 255, 255])
            lower_green = np.array([50, 50, 50])
            upper_green = np.array([70, 255, 255])
            lower_blue = np.array([100, 50, 50])
            upper_blue = np.array([130, 255, 255])
            lower_yellow = np.array([20, 50, 50])
            upper_yellow = np.array([40, 255, 255])

            mask_red = cv2.inRange(img_hsv, lower_red, upper_red)
            mask_green = cv2.inRange(img_hsv, lower_green, upper_green)
            mask_blue = cv2.inRange(img_hsv, lower_blue, upper_blue)
            mask_yellow = cv2.inRange(img_hsv, lower_yellow, upper_yellow)

            contours_red, _ = cv2.findContours(mask_red, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            contours_green, _ = cv2.findContours(mask_green, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            contours_blue, _ = cv2.findContours(mask_blue, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            contours_yellow, _ = cv2.findContours(mask_yellow, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            contours = [contours_red, contours_green, contours_blue, contours_yellow]
            max_contour_area = 0
            max_contour_color = None
            for i, color_contours in enumerate(contours):
                if len(color_contours) > 0:
                    contour_area = max(cv2.contourArea(contour) for contour in color_contours)
                    if contour_area > max_contour_area:
                        max_contour_area = contour_area
                        max_contour_color = i

            colors = ["Red", "Green", "Blue", "Yellow"]
            if max_contour_color is not None:
                print(colors[max_contour_color])
                return colors[max_contour_color]
            else:
                return None

        except (FileNotFoundError, cv2.error) as e:
            print(f"Error: {e}")
            return None

    def scan(self):
        rgb = self._get_rgb()
        if rgb is not None:
            return rgb
        else:
            return "error"

if __name__ == "__main__":
    def test_scan():
        cam = Camera(camera_index=0)
        start_time = time.time()
        while True:
            current_time = time.time()
            if current_time - start_time >= 3:
                color = cam.scan()
                if color is not None:
                    print(f"Detected color: {color}")
                start_time = current_time

            if keyboard.is_pressed('space'):
                break

    test_scan()
  