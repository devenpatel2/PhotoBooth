# Introduction
This application is created for caputuring photos with a webcam or a digital camera remotely, using a web-browser. For e.g I've connected my Canon DSLR to a raspberry-pi and wanted to click images without disturbing the camera. The server is started on the raspberry pi and now photos can be clicked through a remote machine/phone using a browser. 

# Requirements
1) Opencv dependencies (for Raspberry-PI)
```bash
apt update
apt install libavcodec-dev \
    libavformat-dev \
    libswcale-dev \
    libswscale-dev \
    libqtgui4 \
    libqt4-test \
    libblas-dev \
    liblapack-dev \
    libatlas-base-dev 
```
2) [libgphoto2](http://www.gphoto.org/proj/libgphoto2/)
```bash
apt install libgphoto2-dev
```

# Install python packages
```bash
pip3 install -r requirements.txt
```
# Setup
Please change the line in [PhotoBooth/static/js/navbar_camera.js](https://github.com/devenpatel2/PhotoBooth/blob/master/static/js/navbar_camera.js#L6) to set the correct ip of your machine, if you plan to put the server on a remote machine. The app currently supports. The value indicated in brackets is the command line argument paramenter to be passed. The dummy parameter can be used for testing. It generates a random image. 
   - Digital cameras/SLR ( --digi)
   - WebCam (--webcam)
   - USBCam (--usbcam)
   - Dummy (--dummy) 
```
python app.py --digi
```
Images are stored in **Images/image** and **Images/rescaled** directories. The **image** directory contains the full-size image and the **rescaled** has the resized images. The rescaled images are sent to front end, to for speed, since with DSLR, these images can be as big as *5184x3456* in size. 
