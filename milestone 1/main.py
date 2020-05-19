
from tkinter import *
from Engine import *
from Steering import *
import threading
import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)
GPIO.cleanup()

host = ''
port = 5560
# ----- set up PWM function ------
cycleTimes_eng = {  # slidervalue, timeLow
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

cycleTimes_ster = {  # slidervalue, input1
            -50: 0.015,
            -40: 0.012,
            -30: 0.009,
            -20: 0.006,
            -10: 0.003,
            0: 0.00,
            10: -0.003,
            20: -0.006,
            30: -0.009,
            40: -0.012,
            50: -0.015}

timeLow = 0
timeHigh = 0



def PWM():
    while True:
        global EngineGUI
        timeLow = cycleTimes_eng[EngineGUI.getPWMvalue()]

        # set cycle times

        timeHigh = timeLow - 0.020

        if timeHigh < 0:
            timeHigh =  -timeHigh

        GPIO.output(15, 1)
        time.sleep(timeHigh)
        GPIO.output(15, 0)
        time.sleep(timeLow)

        # reset times for next cycle
        timeLow = 0
        timeHigh = 0

def PWMsteering():
    while True:
        global SteeringGUI
        timeHigh = cycleTimes_ster[SteeringGUI.getPWMvalue()]

        if timeHigh < 0:
            timeHigh = -timeHigh

        timeLow = timeHigh - 0.020

        if timeLow < 0:
            timeLow = -timeLow

        if SteeringGUI.getPWMvalue() > 1:
            GPIO.output(17, 1)  # enable
            GPIO.output(27, 1)  # turn left
            time.sleep(timeHigh)
            GPIO.output(22, 0)
            time.sleep(timeLow)
        elif SteeringGUI.getPWMvalue() < 1:
            GPIO.output(17, 1)  # enable
            GPIO.output(22, 1)  # turn right
            time.sleep(timeHigh)
            GPIO.output(27, 0)
            time.sleep(timeLow)
        else:
            GPIO.output(17, 0)  # enable
            GPIO.output(22, 0)  # straight ahead
            GPIO.output(27, 0)
            time.sleep(0.002)


        # reset times for next cycle
        timeLow = 0
        timeHigh = 0


# -------- set up GUI -------

root = Tk()
root.geometry("400x200")
root.title("GUI Slider")

FrameLeft = Frame(root)
FrameLeft.pack(side=LEFT)
FrameRight = Frame(root)
FrameRight.pack(side=RIGHT)


SteeringGUI = Steering(FrameRight)
EngineGUI = Engine(FrameLeft)

EnginePWM = threading.Thread(target=PWM)
EnginePWM.start()

SteeringPWM = threading.Thread(target=PWMsteering)
SteeringPWM.start()

root.mainloop()



