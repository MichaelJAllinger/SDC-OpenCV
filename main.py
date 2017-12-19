CAR_MODE = "GO"
import start

while (CAR_MODE="GO") # keep ready
	cam #hier soll noch die Kamera-Auswertung hin
	
	distance # Hier sollen die Entfernungen gemessen und gespeichert werden
	
	if (STATE="WAITGREEN") # cam, ports and sensors ready
		print ("Bereit zum Start!")
				
	elif (STATE="WAITBLUE") # waiting for finish line
		print ("Go!")
	
	elif (STATE="WASBLUE") # finish line spotted, drive over finish line
		print ("Ziellinie in Sicht!")
		import calc_drive from drive
		time.sleep (10)
		CAR_MODE="STOP"
		
	else # for debug/error reasons
		GPIO.cleanup()
		print ("Irgendetwas ist mit den 'States' schiefgegangen")

if (CAR_MODE="STOP") # Stop car after finish line

	GPIO.cleanup()
	print ("Das Auto ist über die Ziellinie gefahren und hat erfolgreich abgeschalten")