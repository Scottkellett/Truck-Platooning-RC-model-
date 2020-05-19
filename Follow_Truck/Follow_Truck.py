import threading
import time
#import RPi.GPIO as GPIO
#import numpy as np
import cv2
#from FollowClient import Recieve

# set up GPIO pins
GPIO.setmode(GPIO.BOARD)
GPIO.cleanup()

# set up ultrasonic sensor
TRIG = 35  # ultrasonic sensor trigger
ECHO = 37  # ultrasonic sensor echo

GPIO.setup(TRIG, GPIO.OUT)
GPIO.output(TRIG, 0)
GPIO.setup(ECHO, GPIO.IN)

# set up motor driver
# L293 pin connections
driverenable1 = 12
driverinput1 = 10
driverinput2 = 8
steerenable1 = 11
steerinput1 = 13
steerinput2 = 15

GPIO.setup(driverenable1, GPIO.OUT)
GPIO.output(driverenable1, 1)
GPIO.setup(driverinput1, GPIO.OUT); acc = GPIO.PWM(driverinput1, 50); acc.start(0)
GPIO.setup(driverinput2, GPIO.OUT)
GPIO.setup(steerenable1, GPIO.OUT)
GPIO.setup(steerinput1, GPIO.OUT)
GPIO.setup(steerinput2, GPIO.OUT)

# ----- set up PWM function ------
cycleTimes_eng = {  # speed, timeLow
    0: 0.020,
    1: 0.018,
    2: 0.016,
    3: 0.014,
    4: 0.012,
    5: 0.01,
    6: 0.008,
    7: 0.006,
    8: 0.004,
    9: 0.002,
    10: 0.00}


def PWM(speed):
    global isStraight
    isStraight = True
    data = 1
    leadTruckVelocity = 1
    StartTime = time.time()
    StartTime2 = time.time()
    distance = checkdistance()
    message = "blank"

    while True:
        interval = time.time() - StartTime
        if interval > 2:
            StartTime = time.time()
            try:
                value = Recieve()
                data = int(value)
                leadTruckVelocity = data - 2
                print("successful transmission" + str(leadTruckVelocity))
            except:
                print("unsuccessful transmission")
        if data != 0:
            if isStraight:
                interval2 = time.time() - StartTime2
                if interval2 > 1:
                    StartTime2 = time.time()
                    distance = checkdistance()
                    print(message)

                if 15 < distance < 30:
                    message = "at goal distance"
                elif distance < 8:
                    GPIO.output(8, 1)
                    time.sleep(0.2)
                    GPIO.output(8, 0)
                    message = "breaking"
                elif distance > 200:
                    message = "ultrasonic sensor out of range"
                elif distance > 30:
                    speed = int(leadTruckVelocity) + 1
                    message = "accelerating"
                    # there is no 11 speed value or -1
                    if speed > 10:
                        speed = 10
                elif 8 < distance < 15:
                    speed = int(leadTruckVelocity) - 1
                    message = "decelerating"
                    if speed < 0:
                        speed = 0
            print("speed value is:" + str(speed))

            # set cycle times
            timeLow = cycleTimes_eng[speed]
            timeHigh = timeLow - 0.020
            if timeHigh < 0:
                timeHigh = -timeHigh

            # implement cycle
            GPIO.output(10, 1)
            time.sleep(timeHigh)
            GPIO.output(10, 0)
            time.sleep(timeLow)

            # reset times for next cycle
            timeLow = 0
            timeHigh = 0


def checksteering(cap):
    while True:  # continueous loop

        _, frame = cap.read()  # read frame

        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)  # convert to HSV colour scale

        lower_red = np.array([140, 100, 50])  # define range of desirable pixel values
        upper_red = np.array([190, 255, 255])
        mask = cv2.inRange(hsv, lower_red, upper_red)  # only detect pixels in the range

        kernal = np.ones((5, 5), np.uint8)  # 5x5 kernal
        dilation = cv2.dilate(mask, kernal, iterations=1)  # dilate the extracted image
        median = cv2.medianBlur(dilation, 15)  # apply a median filter with kernal = 15
        _, contours, _ = cv2.findContours(median, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)  # draw region of interest

        cx = 0
        if contours:  # if contours where found
            centrex = []  # initialise list of contour x-coordinates
            for contour in contours:  # loop contours found
                area = cv2.contourArea(contour)  # calculate area
                if 100000 > area > 500:
                    rect = cv2.minAreaRect(contour)  # find bounding box
                    box = cv2.boxPoints(rect)  # get rectangular points of bounding box
                    (x1, _), (_, _), _ = rect  # get contours's midpoint's x co-ordinate
                    centrex.append(x1)  # append it to the list

            if centrex:  # in centres where found
                cx = np.mean(centrex)  # find mean of the array of x co-ordinates
                if 400 > cx > 340:
                    GPIO.output(steerenable1, 0)  # drive straight
                    isStraight = True
                    time.sleep(0.1)
                    print("stright ahead")
                elif cx > 400:
                    GPIO.output(steerenable1, 1)
                    GPIO.output(steerinput1, 0)  # drive left
                    GPIO.output(steerinput2, 1)
                    isStraight = False
                    time.sleep(0.1)
                    print("left")
                elif cx < 340:
                    GPIO.output(steerenable1, 1)
                    GPIO.output(steerinput1, 1)  # drive right
                    GPIO.output(steerinput2, 0)
                    isStraight = False
                    time.sleep(0.1)
                    print("right")
            else:
                print("truck outside of pixel range ")
        else:
            print("no contours found")


def checkdistance():
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
    # print(" current distance is : " + str(current_distance))
    return current_distance


# ----------- main code --------------
print("starting code")
speed = 0
cap = cv2.VideoCapture(0)

print("starting steering thread")

SteeringPWM = threading.Thread(target=checksteering(cap))
SteeringPWM.start()

print("starting Engine PWN thread")
# EnginePWM = threading.Thread(target=PWM( speed))
# EnginePWM.start()


print("ending main thread")
cv2.destroyAllWindows()
cap.release()
