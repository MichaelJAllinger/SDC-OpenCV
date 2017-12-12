import numpy as np
import cv2

#import mylib		#sucht mylib.py und führt es aus
#die Suche wird durchgeführt in:
#import sys
#sys.path



video_capture = cv2.VideoCapture(-1)         # -1: zufällige Kamera auswählen 
video_capture.set(3, 640)                    # Breite des Bildes festlegen
video_capture.set(4, 480)                    # Höhe des Bildes festlegen


while(True):                                 # unendliche Schleife
    ret, frame = video_capture.read()        # Video capturen
    crop_img = frame[240:480,0:640]      # Bild abschneiden ((noch) irrelevante Streckenabschnitte eliminieren)
    
    hsv_img = cv2.cvtColor(crop_img, cv2.COLOR_BGR2HSV)     # Farben in HSV darstellen
    
    lower_pink = np.array([145,50,50])                      # lower_pink, upper_pink definieren
    upper_pink = np.array([164,255,255])
    
    mask = cv2.inRange(hsv_img, lower_pink, upper_pink)         # Threshold the image / Maske erstellen (nur pinke Pixel werden weiß, alle anderen schwarz)
                                                            # inRange creates a binary image!!
    contours,hierarchy = cv2.findContours(mask.copy(), 1, cv2.CHAIN_APPROX_NONE)        # Konturen erkennen:
                                                                                        # CHAIN_APPROX_NONE: Konturen werden nur erkannt, wenn die Pixel horizontale, vertikale oder diagonale Nachbarn sind
    if len(contours) > 0:
        c = max(contours, key=cv2.contourArea)              # die größte Kontur finden (if-Befehl)
        M = cv2.moments(c)
        
        cx = int(M['m10']/M['m00'])                         # Mittelpunktskoordinaten der größten Fläche finden
        cy = int(M['m01']/M['m00'])
        
        if cx >= 360:                                       # Auto positionieren (Linkskurve, Rechtskurve, Geradeausfahrt)
            print "Linkskurve gebraucht!"
        
        if cx < 360 and cx > 120:
            print "Geradeausfahren!"
        
        if cx <= 120:
            print "Rechtskurve gebraucht!"
    
    else:
        print "Keine Linie gefunden."