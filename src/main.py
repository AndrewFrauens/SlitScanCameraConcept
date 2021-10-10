import sys

import cv2 as cv2

import argparse
import os

import CameraSetup
import SlitScanParameterSlider as SSPS

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Experiment with some slit scan camera concepts")

    parser.add_argument('--camera', type=str, choices=('piv2', 'web'),
                        default='piv2',
                        help='select what camera you are using')

    parser.add_argument('--mode', type=int, default=1, choices=range(0, 8),
                        help='select a mode.  For webcam you may need to try different numbers including zero.  For Pi v 2 camera, a higher mode should be lower res but higher fps, don\'t try zero for pi though')

    parser.add_argument('--outputVid', type=str, default="./slit_scan_video.avi",
                        help='path to save video of attempt to. will delete whatever it is pointed at. Tested with .avi')

    args = parser.parse_args()

    camera_selection = args.camera
    mode = args.mode
    vid_path = args.outputVid

    gui = None

    outVid = None

    for frame in CameraSetup.frame_generator(camera_selection, mode):

        if gui is None:
            # arbitrary multiplier on width, could turn into CLI input
            goal_shape = (frame.shape[0], int(frame.shape[1] * 2.31), frame.shape[2])

            source_shape = frame.shape

            window_name = "Experiment -- press (q) or (ESC) to quit"

            gui = SSPS.SlitScanParameterSlider(goal_shape, source_shape, window_name)
            gui.start_viz()

            if vid_path is not None:

                try:
                    os.remove(vid_path)
                except:
                    pass

                processed_img = gui.update_image(frame)

                # todo: find a way to match the fps to the frame generator
                codec = 'XVID'
                outVid = cv2.VideoWriter(vid_path, cv2.VideoWriter_fourcc(*codec), 30, (processed_img.shape[1], processed_img.shape[0]))

        processed_img = gui.update_image(frame)
        if outVid is not None:
            outVid.write(processed_img)

        key_pressed = cv2.waitKey(1)
        # if Q or ESC are pressed, then quit
        if key_pressed == ord('q') or key_pressed == 27:
            break

    if outVid is not None:
        # This probably happens after end of scope anyway, but need to check documentation
        outVid.release()
    cv2.destroyAllWindows()
