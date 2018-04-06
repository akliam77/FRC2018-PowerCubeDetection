#Python program for image processing cubes and the switch during the 2018 FRC

#Import the necessary dependencies
import cv2
import numpy as np
from picamera.array import PiRGBArray
from picamera import PiCamera
from networktables import NetworkTables as nt
import logging
from time import sleep
import threading


#define the camera, resolution and framerate

cam = PiCamera()
cam.resolution = (400, 400)
cam.framerate = 15
rawcap = PiRGBArray(cam, size=(400,400))

sleep(0.1)


 
# Define the ip address of the Robot and initialize the server.
#Get the three SmartDashboard tables
cap = cv2.VideoCapture(0)
ip = "10.46.82.2"
sd = nt.getTable("SmartDashboard")
sc = nt.getTable("Scale")
s = nt.getTable("Switch")
centerX = 320
centerY = 225



nt.initialize(server=ip)

def valueChanged(table, key, value, isNew):
     print("valueChanged: key: '%s'; value: %s; isNew: %s" % (key,value, isNew))

def connectionListener(connected, info):
     print(info, '; connected=%s' % connected)
 
def computeCenter(M):
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
    
X = 0
Y = 0
def post(event, x, y, flags, param):
    if event == cv2.EVENT_MOUSEMOVE:
        
        print(x)
        print(y)
        X = x
        Y = y
     
# This drives the program into an infinite loop.

for frame in cam.capture_continuous(rawcap, format="bgr", use_video_port=True):       
    # Captures the live stream frame-by-frame
    imge = frame.array
    
    canvas = imge
    # Converts images from BGR to HSV
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
    

    center = computeCenter(M)
    
    cv2.circle(canvas, center, 2 ,(255,0,0), -1)
    x, y = center
    s.putNumber('X', x)
    s.putNumber('Y', y)
    sc.putNumber('X', x)
    sc.putNumber('Y', y)
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
    cv2.setMouseCallback('Gray', post)
        
    rawcap.truncate(0)
    
    

 
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
sc.putNumber('X', centerX)
sc.putNumber('Y', centerY)
s.putNumber('X', centerX)
s.putNumber('Y', centerY)
#detectScaleLights()
'''------------------------------------Thread-------------------------------------------------------------'''
import time

class vision(threading.Thread):
    def __init__(self, threadID):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.stop_event = threading.Event()
    def run(self):
        while(not self.stop_event.isSet()):
            print("Waiting")
            self.stop_event.wait(1)
        return 0
    def kill(self):
        self.stop_event.set()

class retriever(threading.Thread):
    def __init__(self, threadID):
        threading.Thread.__init__(self)
        self.stop_event = threading.Event()
        self.threadID = threadID
    def run(self):
        while(not self.stop_event.isSet()):
            print("Waiting")
            self.stop_event.wait(1)
    
        print("Exiting")
    def kill(self):
        self.stop_event.set()
        


class kill(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        
        
    def run(self):
        
        print("Waiting")
        time.sleep(3)
            
       
thread1 = vision("1")
thread2 = retriever("2")
thread3 = kill()


thread1.start()
thread2.start()
thread3.start()

thread3.join()
thread1.kill()
thread2.kill()



print("Dead")



        
    

