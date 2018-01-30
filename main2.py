#Global Import
import RPi.GPIO as GPIO
import time
import numpy as np
import cv2

def distanz_left(LEFT_GPIO_TRIGGER, LEFT_GPIO_ECHO):
    StartZeit = 0
    StopZeit = 0
    
    GPIO.output(LEFT_GPIO_TRIGGER, True)    #10us-Impuls erzeugen
    time.sleep(0.000001)
    GPIO.output(LEFT_GPIO_TRIGGER, False)
    
    while GPIO.input(LEFT_GPIO_ECHO) == 0:  #Warten auf LOW
        StartZeit = time.time()
    
    while GPIO.input(LEFT_GPIO_ECHO) == 1:  #Warten auf HIGH
        StopZeit = time.time()
    
    Techo = StopZeit-StartZeit
    distanz_left = (Techo * 33e3) / 2       #Ergebnis in cm
    return distanz_left

def middle(video_capture):
    
    a = 0
    b = 0
    c = 0
    #diff = 0
        
    ret, frame = video_capture.read()       # Video capturen

    img_rgb = frame[:, :, ::-1]             # richtige Farbdarstellung

    #crop_img = frame[240:480,0:640]

    hsv_img = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    lower_pink = np.array([10,0,0])                      
    upper_pink = np.array([170,180,254])
    
    mask_wrong = cv2.inRange(hsv_img, lower_pink, upper_pink)

    mask = cv2.bitwise_not(mask_wrong)
    
    zeile_korrektur1 = mask[80, :]
    zeile_korrektur2 = mask[200, :]
    zeile_korrektur3 = mask[420, :]
    zeile_vorne = mask[30, :]
    #zeile_90grad = mask[80, 530:]
    
    x_vorne = np.arange(zeile_vorne.shape[0]) #x=0,1,2 ... N-1 (N=Bildbreite)
    delta_point_of_gravity_0 = (zeile_vorne*x_vorne).sum() / (zeile_vorne.sum()+1)
    
    x_korrektur1 = np.arange(zeile_korrektur1.shape[0]) #x=0,1,2 ... N-1 (N=Bildbreite)
    delta_point_of_gravity_1 = (zeile_korrektur1*x_korrektur1).sum() / (zeile_korrektur1.sum()+1)
    
    x_korrektur2 = np.arange(zeile_korrektur2.shape[0]) #x=0,1,2 ... N-1 (N=Bildbreite)
    delta_point_of_gravity_2 = (zeile_korrektur2*x_korrektur2).sum() / (zeile_korrektur2.sum()+1)
    
    x_korrektur3 = np.arange(zeile_korrektur3.shape[0]) #x=0,1,2 ... N-1 (N=Bildbreite)
    delta_point_of_gravity_3 = (zeile_korrektur3*x_korrektur3).sum() / (zeile_korrektur3.sum()+1)
    
    #x_90grad = np.arange(zeile_90grad.shape[0]) #x=0,1,2 ... N-1 (N=Bildbreite)
    #delta_point_of_gravity_90 = (zeile_90grad*x_90grad).sum() / (zeile_90grad.sum()+1)
    
    #delta_point_of_gravity = (delta_point_of_gravity_0 + delta_point_of_gravity_1 + delta_point_of_gravity_2) / 3
    
    return delta_point_of_gravity_0, delta_point_of_gravity_1, delta_point_of_gravity_2, delta_point_of_gravity_3

def green(video_capture):
    
    ret, frame = video_capture.read()       # Video capturen

    img_rgb = frame[:, :, ::-1]             # richtige Farbdarstellung

    #crop_img = frame[240:480,0:640]

    hsv_img = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    lower_green = np.array([45,200,200])                      
    upper_green = np.array([80,255,255])
    
    mask_green = cv2.inRange(hsv_img, lower_green, upper_green)
    
    no_green = cv2.countNonZero(mask_green)

    return no_green

def blue(video_capture):
    
    ret, frame = video_capture.read()       # Video capturen

    img_rgb = frame[:, :, ::-1]             # richtige Farbdarstellung

    #crop_img = frame[240:480,0:640]

    hsv_img = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    lower_blue = np.array([45,200,200])                      
    upper_blue = np.array([120,255,255])
    
    mask_blue = cv2.inRange(hsv_img, lower_blue, upper_blue)
    
    no_blue = cv2.countNonZero(mask_blue)

    return no_blue


PIN_ENA = 18
PIN_IN1 = 23
PIN_IN2 = 24

PIN_ENB = 16
PIN_IN3 = 25
PIN_IN4 = 12

GPIO.setmode(GPIO.BCM)

GPIO.setup(PIN_ENA, GPIO.OUT)
GPIO.setup(PIN_IN1, GPIO.OUT)
GPIO.setup(PIN_IN2, GPIO.OUT)

GPIO.setup(PIN_ENB, GPIO.OUT)
GPIO.setup(PIN_IN3, GPIO.OUT)
GPIO.setup(PIN_IN4, GPIO.OUT)

#Sensoren definieren
#FRONT_GPIO_TRIGGER = 
#FRONT_GPIO_ECHO = 
#RIGHT_GPIO_TRIGGER = 
#RIGHT_GPIO_ECHO = 
LEFT_GPIO_TRIGGER = 19
LEFT_GPIO_ECHO = 26

GPIO.setup(LEFT_GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(LEFT_GPIO_ECHO, GPIO.IN)
#GPIO.setup(RIGHT_GPIO_TRIGGER, GPIO.OUT)
#GPIO.setup(RIGHT_GPIO_ECHO, GPIO.IN)
#GPIO.setup(FRONT_GPIO_TRIGGER, GPIO.OUT)
#GPIO.setup(FRONT_GPIO_ECHO, GPIO.IN)

MotorL = GPIO.PWM(PIN_ENA, 50.0)
MotorR = GPIO.PWM(PIN_ENB, 50.0)

GPIO.output(PIN_IN1, 1)
GPIO.output(PIN_IN2, 0)
GPIO.output(PIN_IN3, 1)
GPIO.output(PIN_IN4, 0)

video_capture = cv2.VideoCapture(0)

STATE = 0


while (STATE == 0):
    start_req = green(video_capture)
    print (STATE)
    
    if start_req > 500:
        STATE = 1



ideal = 320
speicher = 1

while (STATE == 1):
    schwerpunkt, schwerpunkt2, schwerpunkt3, schwerpunkt4 = middle(video_capture)
    speed = 35
    a = 1
    b = 1 
    
    #if schwerpunkt90 > 0:
    #    schwerpunkt = 639
    
    if schwerpunkt == 0 and schwerpunkt2 > 0:
        schwerpunkt = schwerpunkt2
    
    elif schwerpunkt == 0 and schwerpunkt2 == 0:
        schwerpunkt = schwerpunkt3
    
    elif schwerpunkt == 0 and schwerpunkt2 == 0 and schwerpunkt3 == 0:
        schwerpunkt = schwerpunkt4
    
    else:
        schwerpunkt = schwerpunkt
    
       
    lenkung = schwerpunkt/ideal
    
    if lenkung == 0 or lenkung-speicher < -0.5 or lenkung-speicher > 0.5:
        lenkung = speicher
    
    if lenkung > 1.7 or lenkung < 0.3:
        a = 1.1
    
    elif lenkung > 1.95 or lenkung < 0.05:
        a = 1.8
        b = 0
    
    
    #print(lenkung) 

    
    if lenkung == 1:
        MotorL.start(speed)                             # geringen Dämpfungsfaktor einbauen, damit die Lenkung bei höheren Geschwindigkeiten nicht zu krass ist
        MotorR.start(speed)
        speicher = 1
    
    elif lenkung < 1 and lenkung > 0:                         # Linkskurve
        MotorL.start(speed*lenkung)
        MotorR.start(speed*a)
        speicher = lenkung
        
    elif lenkung > 1:                         # Rechtskurve
        MotorL.start(speed*a)
        MotorR.start((2 - lenkung)*speed*b)        
        speicher = lenkung
      

        





 
    


    
    
GPIO.cleanup()



