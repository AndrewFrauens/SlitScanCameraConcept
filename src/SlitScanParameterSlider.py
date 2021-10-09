import numpy as np
import cv2
from typing import Tuple


class SlitScanParameterSlider:
    def __init__(self, shape: Tuple[int, int, int], source_shape: Tuple[int, int, int], window_name: str):
        self.accumulation_image = np.zeros(shape).astype(np.uint8)
        self.split_image = np.zeros((shape[0], 4, 3)).astype(np.uint8)
        self.window_name = window_name

        self.step_size = 2
        self.step_size_name = "step size"
        self.step_size_max_value = 200
        self.step_through_source = 1  # 1 is truthy
        self.step_through_source_name = "step through source"
        self.step_through_source_max_value = 1

        self.source_location = 0
        self.source_location_max_value = source_shape[1]
        self.source_location_name = "source location"
        self.accumulation_image_location = 0
        self.accumulation_image_location_max_value = shape[1]
        self.accumulation_location_name = "accumulation location"

    def set_step_size(self, step_size: int):
        self.step_size = step_size
        cv2.setTrackbarPos(self.step_size_name, self.window_name, self.step_size)

    def set_step_through_source(self, step_through_source):
        self.step_through_source = step_through_source
        cv2.setTrackbarPos(self.step_through_source_name, self.window_name, self.step_through_source)

    def set_source_location(self, source_location):
        self.source_location = source_location
        cv2.setTrackbarPos(self.source_location_name, self.window_name, self.source_location)

    def set_accumulation_location(self, accumulation_location):
        self.accumulation_image_location = accumulation_location
        cv2.setTrackbarPos(self.accumulation_location_name, self.window_name, self.accumulation_image_location)

    def start_viz(self):
        cv2.namedWindow(self.window_name)
        cv2.createTrackbar(self.step_size_name, self.window_name, self.step_size, self.step_size_max_value,
                           self.set_step_size)
        cv2.createTrackbar(self.step_through_source_name, self.window_name, self.step_through_source,
                           self.step_through_source_max_value, self.set_step_through_source)
        cv2.createTrackbar(self.source_location_name, self.window_name, self.source_location,
                           self.source_location_max_value, self.set_source_location)
        cv2.createTrackbar(self.accumulation_location_name, self.window_name, self.accumulation_image_location,
                           self.accumulation_image_location_max_value, self.set_accumulation_location)
        cv2.imshow(self.window_name, self.accumulation_image)

    def update_image(self, input_frame):
        # probably better to find openCV way to handle this
        # didn't want to deal with edge cases of the 4 ways that the indexes could be in or outside of bounds

        beam_image = np.copy(input_frame)
        for col_count in range(self.step_size):
            source_x = (self.source_location + col_count) % input_frame.shape[1]
            dest_x = (self.accumulation_image_location + col_count) % self.accumulation_image.shape[1]

            self.accumulation_image[:, dest_x] = input_frame[:, source_x]

            cv2.line(beam_image, (source_x, 0), (source_x, input_frame.shape[1]), (0, 0, 255))

        if (self.step_through_source == 1):
            self.set_source_location((self.source_location + self.step_size) % input_frame.shape[1])

        self.set_accumulation_location((self.accumulation_image_location + self.step_size) %
                                       self.accumulation_image.shape[1])

        cv2.imshow("input image", input_frame)
        cv2.imshow("accumulation image", self.accumulation_image)

        beam_bias = 0.5
        beam_image = cv2.addWeighted(beam_image, beam_bias, input_frame, 1 - beam_bias, 0)
        total_image = np.hstack((beam_image, self.split_image, self.accumulation_image))
        cv2.imshow(self.window_name, total_image)

        return total_image


