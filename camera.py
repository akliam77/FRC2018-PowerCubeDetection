import cv2
import numpy as np
from picamera.array import PiRGBArray
from picamera import PiCamera
from networktables import NetworkTables as nt

class Camera(object):

    def __init__(self):
        self.cam = PiCamera()
        self.cam.resolution = (400, 400)
        self.cam.framerate = 15
        self.rawcap = PiRGBArray(self.cam, size=(400,400))
    
    def post(self, event, x, y, flags, param):
        if self.event == cv2.EVENT_MOUSEMOVE:
        
            print(x)
            print(y)
            X = x
            Y = y

    def computeCenter(self, M):
        m00 = int(M["m00"])
        m10 = int(M["m10"])
        m01 = int(M["m01"])
        
        if m00 == 0:
            print("Detected bad data from opencv")
            return (-1, -1)
        else:
            x = int(m10/m00)
            y = int(m01/m00)
        
            return(x,y)
