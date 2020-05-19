# this program is used to test if Ultrasonic sensor is
#is working correctly 
import threading
import time
import RPi.GPIO as GPIO
#from tkinter import*
import numpy as np
from picamera.array import PiRGBArray
from picamera import PiCamera
import cv2

GPIO.setmode(GPIO.BOARD)
GPIO.cleanup()

TRIG = 35
ECHO = 37
GPIO.setup(TRIG, GPIO.OUT)
GPIO.output(TRIG, 0)
GPIO.setup(ECHO, GPIO.IN)
time.sleep(0.1)

GPIO.output(TRIG, 1)
time.sleep(0.00001)
GPIO.output(TRIG, 0)

while GPIO.input(ECHO) == 0:
    pass

Start = time.time()

while GPIO.input(ECHO) == 1:
    pass

stop = time.time()
current_distance = (stop - Start) * 17000
print(current_distance)
