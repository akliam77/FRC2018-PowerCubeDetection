"""
File Name: DetectCubeCenter.py

Author: Akli Amrous

Description: This program calculates the center of a cube object
and sends it back to the Roborio via NetworkTables. This was created
for the 2018 FIRST Robotics Competition. 
Copyright (c) Akli Amrous 2018

"""
import cv2
import numpy as np
from picamera.array import PiRGBArray
from picamera import PiCamera
from networktables import NetworkTables as nt
import logging
import time
from camera import Camera 
from datatransfer import DataTransfer


cap = cv2.VideoCapture(0)
cam = Camera()
scale = DataTransfer()
sc = scale.sc
s = scale.s
centerX = 320
centerY = 225
nt.initialize(server=sc.ip)


def main():

    for frame in cam.capture_continuous(cam.rawcap, format="bgr", use_video_port=True):       
        imge = frame.array
        canvas = imge
        hsv = cv2.cvtColor(imge, cv2.COLOR_BGR2HSV)
        lower_red = np.array([20,120,120])
        upper_red = np.array([30,255,255])
    
        # Here we are defining range of blue, red, and yellow color in HSV
        # This creates a mask of blue, red, and yellow coloured 
        # objects found in the frame.
        mask = cv2.inRange(hsv, lower_red, upper_red)

        res = cv2.bitwise_and(imge,imge, mask= mask)
        im2, contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        blob = max(contours, key=lambda el: cv2.contourArea(el), default=0)
        
        M = cv2.moments(blob)
        if (len(contours) == 0):
            print("Empty contours")
        else:
            pass
        

        center = cam.computeCenter(M)
        
        cv2.circle(canvas, center, 2 ,(255,0,0), -1)
        x, y = center
        scale.sendScaleData(centerX, centerY)
        scale.sendSwitchData(centerX, centerY)
        s.putNumber('View', 1)
        
        
        # The bitwise and of the frame and mask is done so 
        # that only the blue, red, or yellow coloured objects are highlighted 
        # and stored in res
    
        blurred = cv2.GaussianBlur(canvas, (5,5), 0)
        hsv  = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
        lowerBlue = np.array([218,64.3, 81.2])
        upperBlue = np.array([219, 96.9, 100])
        lowerRed = np.array([359.2, 83.9, 100])
        upperRed = np.array([359, 96.9, 100])
        screenBlue = cv2.inRange(hsv, lowerBlue, upperBlue)
        screenRed = cv2.inRange(hsv, lowerRed, upperRed)
        
        # im_with_keypoints = detectScaleLights(blurred)
        # cv2.imshow('Keypoints', im_with_keypoints)
        cv2.imshow('Gray', hsv)
        cv2.imshow('frame',imge)
        cv2.imshow('mask',mask)
        cv2.imshow('can',canvas)
        cv2.setMouseCallback('Gray', cam.post)
            
        cam.rawcap.truncate(0)
        
        # This displays the frame, mask 
        # and res which we created in 3 separate windows.
        k = cv2.waitKey(33)
        if k == ord('a'):
            break
    
    print("Exited program loop")
    # Destroys all of the HighGUI windows.
    cv2.destroyAllWindows()
    
    # release the captured frame
    cap.release()



    scale.sendScaleData(centerX, centerY)
    scale.sendSwitchData(centerX, centerY)


if __name__ == '__main__':
    main()
