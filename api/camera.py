from abc import ABC, abstractmethod
import os
import logging

import cv2
import gphoto2 as gp
import numpy as np

logging.basicConfig()
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


class Camera(ABC):

    def __init__(self, camera_type="generic"):
        self._camera_type = camera_type

    @property
    def camera_type(self):
        return self._camera_type

    @abstractmethod
    def capture(self):
        pass

    @abstractmethod
    def close(self):
        pass

    def stream(self):
        # TO-DO
        pass


class DummyCam(Camera):

    def __init__(self):
        super().__init__(camera_type="Dummy")

    def capture(self):
        rnd_image = np.random.randint(
            0, 255, [1024, 1920, 3]).astype(dtype=np.uint8)
        return rnd_image

    def close(self):
        pass


class WebCam(Camera):

    def __init__(self, external=False):
        super().__init__(camera_type="WebCam")

    def close(self):
        self._camera.release()

    def capture(self):
        self._camera = cv2.VideoCapture(-1)
        ret, frame = self._camera.read()
        if not ret:
            raise Exception("Failed to capture image")
        self._camera.release()
        return frame


class DigitalCam(Camera):

    def __init__(self):
        super().__init__(camera_type="DigitalCam")
        self._camera = gp.Camera()
        # self._camera.init()

    def close(self):
        logger.info("closing camera")
        self._camera.exit()

    def capture(self, tmp_path="/tmp/gp2_capture"):
        if not os.path.exists(tmp_path):
            os.makedirs(tmp_path)
        file_path = self._camera.capture(gp.GP_CAPTURE_IMAGE)
        target = os.path.join(tmp_path, file_path.name)
        camera_file = self._camera.file_get(
            file_path.folder, file_path.name, gp.GP_FILE_TYPE_NORMAL)
        camera_file.save(target)
        image = cv2.imread(target)
        return image

    def dummy_image(self):
        rnd_image = np.random.randint(
            0, 255, [100, 100, 3]).astype(dtype=np.uint8)
        return rnd_image


def test_driver():
    cam = Camera()
    image = cam.capture()
    print(image.shape)
    cam.close()


if __name__ == "__main__":

    test_driver()
