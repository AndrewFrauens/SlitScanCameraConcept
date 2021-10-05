# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import cv2 as cv2
import numpy as np

if __name__ == '__main__':

    vid = cv2.VideoCapture(1)
    ret, frame = vid.read()

    # change this to change apparent speed
    # current method leaves jarring edges, could potentially find a way to smooth, but it'd be more complicated
    cols_to_capture = 2

    im_width = frame.shape[1]
    # start capturing from here
    capture_col = im_width // 2
    move_capture_window = True

    # start inputting to here
    destination_col = 0

    # store the constructed collection of pixels
    collection = np.zeros(frame.shape).astype(np.uint8)

    while ret:
        ret, frame = vid.read()

        # had a hard time using the start:end notation across the edge of the frame so doing col by col instead
        for i in range(cols_to_capture):
            collection[:, (destination_col + i) % im_width] = frame[:, (capture_col + i) % im_width]

        if move_capture_window:
            destination_col += cols_to_capture
            destination_col %= im_width

        capture_col += cols_to_capture
        capture_col %= im_width

        # the +_1/-1 here are to ensure that we are surrounding the captured region rather than writing on the edges of the captured region
        frame = cv2.line(frame, (capture_col - 1, 0), (capture_col - 1, frame.shape[0]), (0, 0, 255))
        frame = cv2.line(frame, ((capture_col + cols_to_capture + 1) % im_width, 0),
                         ((capture_col + cols_to_capture + 1) % im_width, frame.shape[0]), (0, 0, 255))

        cv2.imshow('frame', frame)
        # might be able to do something here if we want to maintain the oldest
        # pixels on the left and the newest on the right for every single time it's shown in every time step
        cv2.imshow('colelction', collection)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            ret = False

    vid.release()
    cv2.destroyAllWindows()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
