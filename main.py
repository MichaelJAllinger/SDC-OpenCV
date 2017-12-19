#Global Import
import RPi.GPIO as GPIO
import time
import numpy as np
import cv2
import start
from drive import calc_drive as drive
from drive import drive_left as dl
from drive import drive_right as dr
from drive import drive_forward as df
from sensor import check_front as cf
from sensor import check_right as cr
from sensor import check_left as cl
from cam import camerafunctions as camfunc

#Set Car-Mode
CAR_MODE = "GO"

#Set State
STATE = "WAITGREEN"

#global setup GPIO/PINs/CAM 
start.CAMGPIOPINSETUP ()


"""
while (CAR_MODE="GO") # keep ready
	cam #hier soll noch die Kamera-Auswertung hin
	
	if (camfunc.GREEN == TRUE)
		STATE = "WAITBLUE"
	if (camfunc.BLUE == TRUE)
		STATE = "WASBLUE"
	
	
	distance # Hier sollen die Entfernungen gemessen und gespeichert werden
	
	if (STATE=="WAITGREEN") # cam, ports and sensors ready
		print ("Bereit zum Start!")
				
	elif (STATE=="WAITBLUE") # waiting for finish line
		print ("Go!")
		drive.DRIVE
	
	elif (STATE=="WASBLUE") # finish line spotted, drive over finish line
		print ("Ziellinie in Sicht!")
		time.sleep (10)
		CAR_MODE="STOP"
		
	else # for debug/error reasons
		GPIO.cleanup()
		print ("Irgendetwas ist mit den 'States' schiefgegangen")

if (CAR_MODE="STOP") # Stop car after finish line

	GPIO.cleanup()
	print ("Das Auto ist über die Ziellinie gefahren und hat erfolgreich abgeschaltet")
	
"""

GPIO.cleanup()