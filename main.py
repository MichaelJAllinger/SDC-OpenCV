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
    
    #zeile_hinten = mask[80, :]
    
    #x_hinten = np.arange(zeile_hinten.shape[0]) #x=0,1,2 ... N-1 (N=Bildbreite)
    #point_of_gravity_hinten = (zeile_hinten*x_hinten).sum() / (zeile_hinten.sum()+1)
    
    #zeile_mitte = mask[300, :]
    
    #x_mitte = np.arange(zeile_mitte.shape[0]) #x=0,1,2 ... N-1 (N=Bildbreite)
    #point_of_gravity_mitte = (zeile_mitte*x_hinten).sum() / (zeile_mitte.sum()+1)

    zeile_korrektur1 = mask[55, :]
    zeile_korrektur2 = mask[45, :]
    zeile_vorne = mask[50, :]
    
    x_vorne = np.arange(zeile_vorne.shape[0]) #x=0,1,2 ... N-1 (N=Bildbreite)
    delta_point_of_gravity_0 = (zeile_vorne*x_vorne).sum() / (zeile_vorne.sum()+1)
    
    x_korrektur1 = np.arange(zeile_korrektur1.shape[0]) #x=0,1,2 ... N-1 (N=Bildbreite)
    delta_point_of_gravity_1 = (zeile_korrektur1*x_korrektur1).sum() / (zeile_korrektur1.sum()+1)
    
    x_korrektur2 = np.arange(zeile_korrektur2.shape[0]) #x=0,1,2 ... N-1 (N=Bildbreite)
    delta_point_of_gravity_2 = (zeile_korrektur2*x_korrektur2).sum() / (zeile_korrektur2.sum()+1)
    
    delta_point_of_gravity = (delta_point_of_gravity_0 + delta_point_of_gravity_1 + delta_point_of_gravity_2) / 3
    """
    diff = delta_point_of_gravity - earlier_delta

    if diff > 100:
        delta_point_of_gravity = earlier_delta + 100
    
    elif diff < -100:
        delta_point_of_gravity = earlier_delta - 100
    
    else:
        delta_point_of_gravity = delta_point_of_gravity
    """
    #point_of_gravity_vornemitte = (point_of_gravity_vorne + point_of_gravity_mitte) / 2
    
    #delta_point_of_gravity = point_of_gravity_vornemitte
    
    #delta_point_of_gravity = point_of_gravity_hinten - point_of_gravity_vornemitte + 320       # um eine positive Zahl zu erhalten

    #print( x.dtype )
    """
    if delta_point_of_gravity > 3 and delta_point_of_gravity <= 100:                                       # Auto positionieren (Linkskurve, Rechtskurve, Geradeausfahrt)
        a = "Starke Linkskurve gebraucht!"
        
    elif delta_point_of_gravity > 100 and delta_point_of_gravity < 230:
        a = "Linkskurve gebraucht!"
    
    elif delta_point_of_gravity >= 230 and delta_point_of_gravity < 265:
        a = "Schwache Linkskurve gebraucht!"
        
    elif delta_point_of_gravity >= 265 and delta_point_of_gravity <= 375:
        a = "Geradeausfahren!"
        
    elif delta_point_of_gravity > 375 and delta_point_of_gravity <= 430:
        a = "Schwache Rechtskurve gebraucht!"

    elif delta_point_of_gravity > 430 and delta_point_of_gravity < 540:
        a = "Rechtskurve gebraucht!"
     
    elif delta_point_of_gravity >= 540:
        a = "Starke Rechtskurve gebraucht!"
    
    else:
        a = "Keine Linie gefunden!"
    """   
        #distance_left = distanz_left(LEFT_GPIO_TRIGGER, LEFT_GPIO_ECHO)
        
        #if distance_left <= 30:                                       # Auto positionieren
            #a = "Sensor: Linkskurve gebraucht!"
        
        #elif distance_left < 30 and distance_left > 10:
            #a = "Sensor: Geradeausfahren!"
        
        #elif distance_left >= 10:
            #a = "Sensor: Rechtskurve gebraucht!"
        
        #else:
            #a = "Weder Linie noch linke Wand gefunden!"
    
    lower_green = np.array([40,50,50])                      
    upper_green = np.array([65,255,255])
    
    mask_green = cv2.inRange(hsv_img, lower_green, upper_green)
    
    zeile100_green = mask_green[100, :]
    row_sum_green = zeile100_green.sum()
    
    if row_sum_green == 0:
        b = "Kein Grün vorhanden."
        
    else:
        b = "Los geht's!"   
      
    #lower_blue = np.array([40,50,50])                      
    #upper_blue = np.array([65,255,255])
    
    #mask_blue = cv2.inRange(hsv_img, lower_blue, upper_blue)
    
    #zeile100_blue = mask_blue[100, :]
    #row_sum_blue = zeile100_blue.sum()
    
    #if row_sum_blue == 0:
        #c = "Weiter!"
        
    #else:
        #c = "Ziel erreicht!"
    
    return [delta_point_of_gravity]

#Set Car-Mode
#CAR_MODE = "GO"

#Set State
#STATE = "WAITGREEN"

#global setup GPIO/PINs/CAM 
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

STATE = 1


#while(STATE == 0):
    #direction, start, ziel = drive(video_capture, LEFT_GPIO_TRIGGER, LEFT_GPIO_ECHO)
    
    #if start == "Los geht's!":
        #STATE = 1
    #else:
        #STATE = 0

speicher = 0
anfangswert = 0

while(STATE == 1):
    direction, start, ziel, schwerpunkt, test = drive(video_capture)
    
    print(direction)
    print(schwerpunkt)
    anfangswert = schwerpunkt

    if ziel == 0:
        GPIO.output(PIN_IN1, 1)
        GPIO.output(PIN_IN2, 0)
        GPIO.output(PIN_IN3, 1)
        GPIO.output(PIN_IN4, 0)
        
        
    
        if direction == "Geradeausfahren!" or direction == "Sensor: Geradeausfahren!":
            MotorL.start(25)
            MotorR.start(25)
            #time.sleep(0.001)
            #anfangswert == schwerpunkt
        
        elif direction == "Linkskurve gebraucht!" or direction == "Sensor: Linkskurve gebraucht!":
            MotorL.start(10)
            MotorR.start(25)
            speicher == "Links"
            #time.sleep(0.001)
            #anfangswert == schwerpunkt
    
        elif direction == "Rechtskurve gebraucht!" or direction == "Sensor: Rechtskurve gebraucht!":
            MotorL.start(25)
            MotorR.start(10)
            speicher == "Rechts"
            #time.sleep(0.001)
            #anfangswert == schwerpunkt
        
        elif direction == "Schwache Linkskurve gebraucht!":
            MotorL.start(17)
            MotorR.start(25)
            #time.sleep(0.001)
            #anfangswert == schwerpunkt
    
        elif direction == "Schwache Rechtskurve gebraucht!":
            MotorL.start(25)
            MotorR.start(17)
            #time.sleep(0.001)
            #anfangswert == schwerpunkt

        elif direction == "Starke Linkskurve gebraucht!":
            MotorL.start(0)
            MotorR.start(35)
            speicher == "Links"
            #time.sleep(0.001)
            #anfangswert == schwerpunkt
    
        elif direction == "Starke Rechtskurve gebraucht!":
            MotorL.start(35)
            MotorR.start(0)
            speicher == "Rechts"
            #time.sleep(0.001)
            #anfangswert == schwerpunkt
            
        else:
                   
            if speicher == "Links":
                MotorL.start(0)
                MotorR.start(40)
    
            elif speicher == "Rechts":
                MotorL.start(40)
                MotorR.start(0)
            """
            elif speicher == "Starke Linkskurve gebraucht!":
                MotorL.start(0)
                MotorR.start(30)
                
            elif speicher == "Starke Rechtskurve gebraucht!":
                MotorL.start(30)
                MotorR.start(0)
            
            GPIO.output(PIN_IN1, 0)
            GPIO.output(PIN_IN2, 1)
            GPIO.output(PIN_IN3, 0)
            GPIO.output(PIN_IN4, 1)
            MotorL.start(50)
            MotorR.start(0)
            #time.sleep(1)
            #STATE = 2
            """
            
    else:
        MotorL.start(20)
        MotorR.start(20)
        time.sleep(3)
        STATE = 2

    
GPIO.cleanup()



