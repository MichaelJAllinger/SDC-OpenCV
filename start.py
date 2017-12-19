#Global Import
import RPi.GPIO as GPIO
import time
import numpy as np
import cv2

#Set State
STATE = "START"

#set global GPIO mode
GPIO.setmode(GPIO.BCM)

#def motor + def calc_drive
PIN_ENA = 18
PIN_IN1 = 23
PIN_IN2 = 24

PIN_ENB = 16
PIN_IN3 = 25
PIN_IN4 = 12

GPIO.setup(PIN_ENA, GPIO.OUT)
GPIO.setup(PIN_IN1, GPIO.OUT)
GPIO.setup(PIN_IN2, GPIO.OUT)

GPIO.setup(PIN_ENB, GPIO.OUT)
GPIO.setup(PIN_IN3, GPIO.OUT)
GPIO.setup(PIN_IN4, GPIO.OUT)
"""
#Sensoren definieren
FRONT_GPIO_TRIGGER = 
FRONT_GPIO_ECHO = 
RIGHT_GPIO_TRIGGER = 
RIGHT_GPIO_ECHO = 
LEFT_GPIO_TRIGGER = 
LEFT_GPIO_ECHO = 

GPIO.setup(LEFT_GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(LEFT_GPIO_ECHO, GPIO.IN)
GPIO.setup(RIGHT_GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(RIGHT_GPIO_ECHO, GPIO.IN)
GPIO.setup(FRONT_GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(FRONT_GPIO_ECHO, GPIO.IN)

video_capture = cv2.VideoCapture(0)         # -1: zufällige Kamera auswählen 

"""

STATE = "WAITGREEN"