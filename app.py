from argparse import ArgumentParser
from datetime import datetime
from glob import glob
import logging
import os

import cv2
from flask import Flask, send_from_directory, request, send_file, url_for, jsonify
from flask_restx import Api, Resource, reqparse
from api.camera import DigitalCam, DummyCam, WebCam

logging.basicConfig()


app = Flask(__name__)
api = Api(app,
          version='1.0',
          title='Camera Capture',
          description='Camera capture')

camera_parser = reqparse.RequestParser()
camera_parser.add_argument('camera', type=dict, location='json')
@api.route('/<path:path>')
class LandingPage(Resource):
    def get(self, path):
        return send_from_directory('templates/home', path)
        # return {'hello':'world'}


@api.route('/camera/<path:image_uri>')
@api.route('/camera')
@api.expect(camera_parser)
class CameraApi(Resource):

    logger = logging.getLogger("CameraApi")
    logger.setLevel(logging.DEBUG)

    def post(self):
        # req parse not working for flask version 1.1.2
        # args = camera_parser.parse_args(req=request, strict=True)
        self._camera = app.config['camera']
        args = request.get_json(force=True)
        self.logger.debug(f"args :{args}")
        action = args['camera']['action']
        self.logger.debug(f"action : {action}")
        if action == "take_picture":
            image = self._camera.capture()
            self.logger.debug(f"capture image {image.shape}")
            rescaled = self.save_image(image)
            return url_for('static', filename=rescaled)

    def get(self, image_uri):
        image_uri = image_uri.split('static/')[-1]
        self.logger.debug(f"sending image {image_uri}")
        return send_file(image_uri, 'image/jpeg')

    def get_filename(self):
        current_time = datetime.now().strftime("%Y-%m-%d-%H_%M_%S_%f")
        return current_time

    def save_image(self, image, path="Images"):
        image_path = os.path.join(path, "images")
        rescaled_path = os.path.join(path, "rescaled")
        if not os.path.exists(path):
            os.makedirs(image_path)
            os.makedirs(rescaled_path)

        current_time = self.get_filename()
        filename = current_time + ".jpg"
        save_path = os.path.join(image_path, filename)
        cv2.imwrite(save_path, image)
        aspect_ratio = image.shape[1] / image.shape[0]
        desired_height = 480
        width = int(480 * aspect_ratio)
        rescaled_image = cv2.resize(image, (width, desired_height))
        save_path = os.path.join(rescaled_path, filename)

        cv2.imwrite(save_path, rescaled_image)
        return save_path

@api.route('/gallery')
class GalleryApi(Resource):

    def get(self):
        image_list = self.get_image_list('Images/rescaled')
        image_uris = [url_for('static', filename=image_name) for image_name in image_list]
        return jsonify(image_uris)

    def get_image_list(self, image_path):
       image_list = glob(image_path + "/*.jpg")
       return sorted(image_list)

def get_camera(args):
    camera_lookup = {'digi': DigitalCam,
                     'webcam': WebCam,
                     'usbcam': WebCam,
                     'dummy': DummyCam
                     }
    camera_type = [arg for arg in vars(
        args) if getattr(args, arg) is True][0]

    print(f"Setting camera to {camera_type}")
    camera = camera_lookup[camera_type]()
    return camera


def init_static_dirs():
    pass


if __name__ == "__main__":
    parser = ArgumentParser()
    cam_types = parser.add_mutually_exclusive_group()
    cam_types.add_argument(
        "--dummy", help="Select dummy cam", action='store_true')
    cam_types.add_argument(
        "--webcam", help="Select in-build webcam as camera", action="store_true")
    cam_types.add_argument(
        "--usbcam", help="Select external usb cam", action='store_true')
    cam_types.add_argument(
        "--digi", help="Select DSLR or digital cam", action="store_true")
    args = parser.parse_args()
    app.config['camera'] = get_camera(args)
    app.run(debug=True, host='0.0.0.0')
