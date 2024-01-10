from MotorModule import Motor
# import ControllerModule as ctrl
# from LaneDetectionModule import getLaneCurve
import WebcamModule as cam
import cv2
import utils
import numpy as np
from tensorflow.keras.models import load_model

#########################
# robot initialization
bot = Motor(35, 29, 31, 37, 32, 33)
steeringRatio = 0.7
maxSpeed = 0.25
model = load_model('model.h5')
# method = 'Joystick'
#########################

def preProcess(image):
	image = image[54:120, :, :]
	image = cv2.cvtColor(image, cv2.COLOR_RGB2YUV)
	image = cv2.GaussianBlur(image, (3, 3), 0)
	image = cv2.resize(image, (200, 66))
	image = image / 255
	return image

def main():
	
	# run using image processing
	#utils.initializeTrackbars([0, 416, 100, 172])
	#image = WebcamModule.getImage()
	#curveVal = getLaneCurve(image, 1)
	
	#sensitivity = 1.3
	#maxSpeed = 0.3
	
	#if curveVal > maxSpeed: curveVal = maxSpeed
	#if curveVal < -maxSpeed: curveVal = -maxSpeed
	
	#if curveVal > 0:
	#	sensitivity = 1.5
	#	if curveVal < 0.05: curveVal = 0
	#else:
	#	if curveVal > -0.08: curveVal = 0
		
	#bot.move(0.2, curveVal * sensitivity, 0.05)
	#cv2.waitKey(1)
	
	# run using controller
	#if method == 'Joystick':
	#	ctrlVal = ctrl.getCtrl()
	#	bot.move(-(ctrlVal['axis3']), -(ctrlVal['axis2']), 0.1)
	
	# run using neural network
	image = cam.getImage(True, size = [240, 120])
	image = np.asarray(image)
	image = preProcess(image)
	image = np.array([image])
	steering = float(model.predict(image))
	print(steering * steeringRatio)
	#bot.move(maxSpeed, -steering * steeringRatio)
	cv2.waitKey(1)
	
		
if __name__ == '__main__':
	while True:
		main()

# ffmpeg -f v4l2 -r 25 -s 640x480 -i /dev/video0 out.avi
# https://storage.googleapis.com/tensorflow/linux/cpu/tensorflow_cpu-2.15.0-cp39-cp39-manylinux_2_17_x86_64.manylinux2014_x86_64.whl
# sudo apt-get install --yes libssl-dev zlib1g-dev libbz2-dev libreadline-dev libsqlite3-dev llvm libncurses5-dev libncursesw5-dev xz-utils tk-dev libgdbm-dev lzma lzma-dev tcl-dev libxml2-dev libxmlsec1-dev libffi-dev liblzma-dev wget make openssl
# sudo apt-get install -y libhdf5-dev libc-ares-dev libeigen3-dev gcc gfortran libgfortran5 libatlas3-base libatlas-base-dev libopenblas-dev libopenblas-base libblas-dev liblapack-dev cython3 libatlas-base-dev openmpi-bin libopenmpi-dev python3-dev build-essential cmake pkg-config libjpeg-dev libtiff5-dev libpng-dev libavcodec-dev libavformat-dev libswscale-dev libv4l-dev libxvidcore-dev libx264-dev libfontconfig1-dev libcairo2-dev libgdk-pixbuf2.0-dev libpango1.0-dev libgtk2.0-dev libgtk-3-dev libhdf5-serial-dev libhdf5-103 libqt5gui5 libqt5webkit5 libqt5test5 python3-pyqt5
# low-1.14.0-cp37-cp37m-linux_armv7l.sh
# https://raw.githubusercontent.com/PINTO0309/Tensorflow-bin/main/previous_versions/download_tensorflow-1.14.0-cp37-cp37m-linux_armv7l.sh
