def distanz_right():
    GPIO.output(RIGHT_GPIO_TRIGGER, True)    #10us-Impuls erzeugen
    time.sleep(0.000001)
    GPIO.output(RIGHT_GPIO_TRIGGER, False)
    
    while GPIO.input(RIGHT_GPIO_ECHO) == 0:  #Warten auf LOW
        StartZeit = time.time()
    
    while GPIO.input(RIGHT_GPIO_ECHO) == 1:  #Warten auf HIGH
        StopZeit = time.time()
    
    Techo = StopZeit-StartZeit
    distanz_right = (Techo * 33e3) / 2       #Ergebnis in cm
    return distanz_right