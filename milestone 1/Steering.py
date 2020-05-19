# tkinter
# this file shows the GUI for the truck platooning project
from Tkinter import *
import RPi.GPIO as GPIO
import time

steerenable1 = 17
steerinput1 = 27
steerinput2 = 22


class Steering:

    # **** steering motor********
    def __init__(self, frameright):
        self.Steering_slide = Scale(frameright, from_=-50, to=50, resolution=10, orient=HORIZONTAL, command= self.steering)
        self.labelsteerer = Label(frameright, text="steer")
        self.labelsteerer.pack()
        self.Steering_slide.pack()

        self.my_label = Label(frameright, text=self.Steering_slide.get())
        self.my_label.pack()

        GPIO.setup(steerenable1, GPIO.OUT)
        GPIO.output(steerenable1, 1)

        GPIO.setup(steerinput1, GPIO.OUT)
        GPIO.setup(steerinput2, GPIO.OUT)

        updateslider = Button(frameright, text="Update", command=self.Steering_slide_update)
        updateslider.pack()

    def Steering_slide_update(self):
        self.my_label.config(text=self.Steering_slide.get())


    def steering(self, event):
        global slidervalue
        print(self.Steering_slide.get())
        self.getPWMvalue()

    def getPWMvalue(self):
        return self.Steering_slide.get()