from datetime import datetime
import json
import logging
import os

import cv2
from flask import Flask, send_from_directory, request, make_response
from flask_restx import Api, Resource, reqparse, fields
from api.camera import DigitalCamera

logging.basicConfig()


app = Flask(__name__)
api = Api(app,
        version='1.0',
        title='Camera Capture',
        description='Camera capture')

camera_parser = reqparse.RequestParser()
camera_parser.add_argument('camera',  type=dict, location='json')
camera = DigitalCamera()
@api.route('/<path:path>')
class LandingPage(Resource):
    def get(self, path):
        return send_from_directory('templates/home', path)
        #return {'hello':'world'}

@api.route('/camera')
@api.expect(camera_parser)
class CameraApi(Resource):

    logger = logging.getLogger("CameraApi")
    logger.setLevel(logging.DEBUG)

    def post(self):
        args = camera_parser.parse_args(req=request, strict=True)
        self.logger.debug(f"args :{args}")
        action = args['camera']['action']
        self.logger.debug(f"action : {action}")
        if action == "take_picture":
            #image = camera.dummy_image()
            image = camera.capture()
            self.save_image(image)
            thumb_image = cv2.resize(image, (0,0), fx=0.25, fy=0.25)
            cv2_encoded = cv2.imencode('.png', thumb_image)[1]
            response = make_response(cv2_encoded.tobytes())
            response.headers.set('Content-Type', 'image/png')
            return response

    def get_filename(self):
        current_time = datetime.now().strftime("%Y-%m-%d-%H_%M_%S_%f")
        return current_time

    def save_image(self, image, path="Images"):
        image_path = os.path.join("Images", "images")
        thumb_path = os.path.join("Images", "thumb")
        if not os.path.exists(path):
            os.makedirs(image_path)
            os.makedirs(thumb_path)
        current_time = self.get_filename()
        filename = current_time + ".jpg"
        save_path = os.path.join(image_path, filename)
        cv2.imwrite(save_path, image)
        thumb_image = cv2.resize(image, (0,0), fx=0.25, fy=0.25)
        save_path = os.path.join(thumb_path, filename)
        cv2.imwrite(save_path, thumb_image)

if __name__ == "__main__":

    app.run(debug=True, host='0.0.0.0')
