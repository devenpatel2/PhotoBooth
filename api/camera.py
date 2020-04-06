from abc import ABC, abstractmethod
import os
import logging

import cv2
import gphoto2 as gp
import numpy as np

logging.basicConfig()
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

class Camera:

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

class DummyCamera(Camera):

    def __init__(self):
        super().__init__(camera_type="Dummy")

    def capture(self):
        rnd_image = np.random.randint(0, 255, [1920, 1024, 3]).astype(dtype=np.uint8)
        return rnd_image

    def close(self):
        pass

class WebCam(Camera):

    def __init__(self, external=False):
        super().__init__(camera_type="WebCam")
        device_idx = 0 if external else 1
        self._camera = cv2.VideoCapture(device_idx)

    def close(self):
        self._camera.release()

    def capture(self):
        ret, frame = self._camera.read()
        if not ret:
            raise Exception("Failed to capture image")
        return frame

class DigitalCamera(Camera):

    def __init__(self):
        super().__init__(camera_type="DigitalCam")
        self._camera = gp.Camera()
        #self._camera.init()

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
        rnd_image = np.random.randint(0, 255, [100, 100, 3]).astype(dtype=np.uint8)
        return rnd_image

def test_driver():
    cam = Camera()
    image = cam.capture()
    print(image.shape)
    cam.close()

if __name__ == "__main__":

    test_driver()
