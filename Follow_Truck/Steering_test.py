import time
import RPi.GPIO as GPIO
import cv2
import numpy as np 

GPIO.setmode(GPIO.BOARD)
GPIO.cleanup()


steerenable = 11
steerinput1 = 13
steerinput2 = 15
GPIO.setup(steerenable, GPIO.OUT)
GPIO.setup(steerinput1, GPIO.OUT)
GPIO.setup(steerinput2, GPIO.OUT)

cap = cv2.VideoCapture(0)

while True:
    _, frame = cap.read()
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    lower_red = np.array([140, 100,50])
    upper_red = np.array([190, 255, 255])

    mask = cv2.inRange(hsv, lower_red, upper_red)
    res = cv2.bitwise_and(frame , frame, mask = mask)


    kernal = np.ones((5,5), np.uint8)
    dilation = cv2.dilate(mask, kernal , iterations = 1)
    median = cv2.medianBlur(dilation, 15)
    #cv2.imshow('median', median)

    
    ret, contours, hierachy = cv2.findContours(median, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    cx = 0;
    if contours: #if contours where found
        centrex= [] # initialise list of contour x-coordinates
        for contour in contours: # loop contours found
            area = cv2.contourArea(contour) # calculate area
            if 100000 > area > 500:
                rect = cv2.minAreaRect(contour)
                box = cv2.boxPoints(rect)
                (x1,_), (_,_) ,_ = rect
                centrex.append(x1)

        if centrex:
            cx = np.mean(centrex)
            if 400 > cx > 340:
                GPIO.output(steerenable,0)
                time.sleep(0.5)
                print("straight ahead")
            elif cx > 400:
                GPIO.output(steerenable,1)
                GPIO.output(steerinput1,1)
                GPIO.output(steerinput2,0)
                time.sleep(0.3)
                print( "turn left")
            elif cx < 340:
                GPIO.output(steerenable,1)
                GPIO.output(steerinput1,1)
                GPIO.output(steerinput2,0)
                time.sleep(0.3)
                print ("turn right ")

    

    k = cv2.waitKey(5) & 0xFF
    if k ==27:
        break

cv2.destroyAllWindows()
cap.release()