import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

PIN_ENA = 18
PIN_IN1 = 23
PIN_IN2 = 24

PIN_ENB = 16
PIN_IN3 = 25
PIN_IN4 = 12

GPIO_TRIGGER = 22
GPIO_ECHO = 5

GPIO.setup(PIN_ENA, GPIO.OUT)
GPIO.setup(PIN_IN1, GPIO.OUT)
GPIO.setup(PIN_IN2, GPIO.OUT)

GPIO.setup(PIN_ENB, GPIO.OUT)
GPIO.setup(PIN_IN3, GPIO.OUT)
GPIO.setup(PIN_IN4, GPIO.OUT)

GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)

MotorL = GPIO.PWM(PIN_ENA, 50.0)
MotorR = GPIO.PWM(PIN_ENB, 50.0)

GPIO.output(PIN_IN1, 1)
GPIO.output(PIN_IN2, 0)
GPIO.output(PIN_IN3, 0)
GPIO.output(PIN_IN4, 1)

# ------------------------

def distanzl():
    GPIO.output(GPIO_TRIGGER, True)    #10us-Impuls erzeugen
    time.sleep(0.000001)
    GPIO.output(GPIO_TRIGGER, False)
    
    while GPIO.input(GPIO_ECHO) == 0:  #Warten auf LOW
        StartZeit = time.time()
    
    while GPIO.input(GPIO_ECHO) == 1:  #Warten auf HIGH
        StopZeit = time.time()
    
    Techo = StopZeit-StartZeit
    distanz = (Techo * 33e3) / 2       #Ergebnis in cm
    return distanz



try:
    while True:
        MotorL.start(90)
        MotorR.start(100)
        Entfernung = distanzl()
        print("Gemessene Entfernung = %.1f cm" %Entfernung)
        time.sleep(0.1)
except KeyboardInterrupt:
    print("Messung angehalten.")
    MotorR.stop()
    MotorL.stop()
    GPIO.cleanup()

GPIO.cleanup()