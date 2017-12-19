def distanz_front():
    GPIO.output(FRONT_GPIO_TRIGGER, True)    #10us-Impuls erzeugen
    time.sleep(0.000001)
    GPIO.output(FRONT_GPIO_TRIGGER, False)
    
    while GPIO.input(FRONT_GPIO_ECHO) == 0:  #Warten auf LOW
        StartZeit = time.time()
    
    while GPIO.input(FRONT_GPIO_ECHO) == 1:  #Warten auf HIGH
        StopZeit = time.time()
    
    Techo = StopZeit-StartZeit
    distanz_front = (Techo * 33e3) / 2       #Ergebnis in cm
    return distanz_front