from machine import Pin
import utime
import time
import machine 


## renvoi la distance en cm (mesure par ultrasons)
def distance():
    #initialisation des pins
    trig = Pin('P23', mode = Pin.OUT)
    echo = Pin('P22', mode = Pin.IN)
    
    # envoie d'une impulsion de 10us
    trig.value(0)
    time.sleep(2/1000000)
    trig.value(1)
    time.sleep(10/1000000)
    trig.value(0)
    
    # mesure du temps de propagation
    while echo() == 0:
        pass
    start = utime.ticks_us()

    while echo() == 1:
        pass
    finish = utime.ticks_us()
    
    duree = start-finish
    
    # calcul de la distance
    distance = duree * 340 / 2 / 10000 # 340 : vitesse du son en m/s / 2 : aller-retour / 10000 : pour passer de µs en s
    
    return distance
    
    
def niveau_liquide():
    adc = machine.ADC()
    apin = adc.channel(pin='P16')
    niveau = apin.voltage()
    return niveau