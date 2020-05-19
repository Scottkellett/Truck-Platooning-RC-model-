# this file shows the GUI for the truck platooning project
from tkinter import *
import RPi.GPIO as GPIO
import time
from CookieClient import *
# -----set up GPIO ------

driverenable1 = 18
driverinput1 = 15
driverinput2 = 14


class Engine():

    slidervalue = 0

    # ***** motor driver******
    def __init__(self, frameleft):
        self.engine_slide = Scale(frameleft, from_=0, to=10, resolution=1, orient=VERTICAL, command=self.motorpower)
        self.labeldriver = Label(frameleft, text="Engine Power")
        self.labeldriver.pack()
        self.engine_slide.pack()

        self.my_label = Label(frameleft, text=self.engine_slide.get())
        self.my_label.pack()


        GPIO.setup(driverenable1, GPIO.OUT)
        GPIO.output(driverenable1,1)


        GPIO.setup(driverinput1, GPIO.OUT)
        GPIO.setup(driverinput2, GPIO.OUT)

        updateslider = Button(frameleft, text="Update", command=self.engine_slide_update)
        updateslider.pack()


    def engine_slide_update(self):

        self.my_label.config(text=self.engine_slide.get())

    def motorpower(self, event):
        global slidervalue
        self.getPWMvalue()
        message = self.engine_slide.get()
        print("transmitting data")
        responce = transmit(message)
        print(responce)


    def getPWMvalue(self):
        return self.engine_slide.get()