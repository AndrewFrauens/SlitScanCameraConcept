import cv2


def get_VideoCapture_settings(camera_selection: str, mode: int = 1):
    if camera_selection == "web":
        return mode  # one works on my computer, I think there's a chance a different number could be needed on other computers
    elif camera_selection != "piv2":
        raise ValueError(f'Expected camera to be of "web" or "piv2," but received "{camera_selection}" instead')

    # information on the sensor modes can be found here
    # https://picamera.readthedocs.io/en/release-1.13/fov.html#sensor-modes

    # these settings are used for internal to the camera

    capture_width = 0
    capture_height = 0
    framerate = 0
    if mode == 1:
        capture_width = 1920
        capture_height = 1080
        framerate = 30
    elif mode == 2 or mode == 3:
        capture_width = 3280
        capture_height = 2464
        framerate = 15
    elif mode == 4:
        capture_width = 1640
        capture_height = 1232
        framerate = 40
    elif mode == 5:
        capture_width = 1640
        capture_height = 922
        framerate = 40
    elif mode == 6:
        capture_width = 1280
        capture_height = 720
        framerate = 90
    elif mode == 7:
        capture_width = 640
        capture_height = 480
        framerate = 120
    else:
        raise ValueError(f'Unexpected mode of {mode} for piv2')

    capture_string = f' video/x-raw(memory:NVMM), width={capture_width}, height={capture_height}, format=NV12, framerate={framerate}/1 '

    # todo: provide a way to change the flip mode
    flip_mode = 0

    flip_string = f' nvvidconv flip-method={flip_mode} '

    # todo: provide a way to request output that doesn't match the capture settings
    display_width = capture_width
    display_height = capture_height

    display_string = f' video/x-raw, width={display_width}, height={display_height}, format=BGRx '

    camera_settings = f'nvarguscamerasrc !{capture_string}!{flip_string}!{display_string}! videoconvert ! video/x-raw, format=BGR ! appsink'
    return camera_settings


def get_camera(camera_selection: str, mode: int):
    camSettings = get_VideoCapture_settings(camera_selection, mode)
    return cv2.VideoCapture(camSettings, cv2.CAP_DSHOW)


def frame_generator(*args):
    # create video_capture either based on camera_selection and mode or on an already created string
    video_capture = get_camera(*args) if len(args) == 2 else cv2.VideoCapture(*args, cv2.CAP_DSHOW) if len(args) == 1 else None
    if video_capture == None:
        raise ValueError(f'Something in the arguments "{args}" is incorrect')

    ret = True

    while ret and video_capture.isOpened():
        # get return status and the current frame
        ret, frame = video_capture.read()
        yield frame

    video_capture.release()
    yield None
