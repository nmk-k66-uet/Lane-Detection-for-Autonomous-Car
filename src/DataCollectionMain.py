import WebcamModule as cam
import DataCollectionModule as collector 
import ControllerModule as ctrl
import MotorModule as MotorModule
import cv2
from time import sleep

maxSpeed = 0.25
bot = Motor(35, 29, 31, 37, 32, 33)

record = 0
while True:
    ctrlVal = ctrl.get