import unittest

import src.CameraSetup


class Test_Webcam_Setting_Creation(unittest.TestCase):
    def test_webcam_settings(self):
        self.assertEqual(src.CameraSetup.get_VideoCapture_settings("web", 0), 0)
        self.assertEqual(src.CameraSetup.get_VideoCapture_settings("web", 1), 1)
        self.assertEqual(src.CameraSetup.get_VideoCapture_settings("web", 3), 3)
        self.assertEqual(src.CameraSetup.get_VideoCapture_settings("web"), 1)

    def test_raspberry_pi_settings(self):
        # verify that the output is even correct at all and works from Jetson Nano before writing tests
        self.assertIsNone(None)


# no test for get_camera or frame_generator since they would use the actual camera
# (I don't feel like mocking the opencv functions)


if __name__ == '__main__':
    unittest.main()
