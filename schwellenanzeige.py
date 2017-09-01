#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
    Funktion:
       Schwellenwertanzeige mit 8 LEDs WS2812 und einem Digi-Dot Booster 

        Alarm       Rot   2 LEDs
        Warnug      Gelb  2 LEDs
        Bereich OK  Grün  4 LEDs
'''

import spidev
import time
 
DELAY = 0.04
LED_COUNT =8
    
'''
Normierung  der Farben Rot ,Grün und Blau
ROT_MAX=116
GRUEN_MAX=61
BLAU_MAX=255
'''
HELLIGKEIT_MAX=100
ROT_MAX=HELLIGKEIT_MAX
GRUEN_MAX=HELLIGKEIT_MAX
BLAU_MAX=HELLIGKEIT_MAX

# Variablen für die verwendeten Befehle
# einfacheres Verständnis beim programmieren
FARBE_setzen="0xA1,"
LED_NR=",0xA4,"
ANZEIGEN="0xB2]"

# Grenzen für min und max Werte
# MIN=0
# MAX=100

# 8 LED werden wie folgt verteilt für die Anzeige
leds_rt=2    # rot
leds_gb=2    # gelb
leds_gn=4    # grün


# Bereiche für die Farbedarstellung
# GRUEN_MIN=0
# GRUEM_MAX=60
# GELB_MIN=60
# GELB_MAX=80
# ROT_MIN=80
# ROT_MAX=100
B0=0      # grün
B1=60     # ab diesem Bereich gelb
B2=80     # ab diesem Bereich rot
B3=100
spi = spidev.SpiDev()

def status():
    '''
    Ausgabe der Schnittstellenparameter

    '''
    bpw=spi.bits_per_word
    cshigh= spi.cshigh
    lsbfirst = spi.lsbfirst
    speed= spi.max_speed_hz
    mode = spi.mode
    tw = spi.threewire
    print("bpw:\t\t", bpw, "\ncshigh:\t\t", cshigh , "\nlsbfirst:\t", lsbfirst)
    print("Speed:\t\t", speed,"\nMode:\t\t", mode ,"\nThreewire:\t",tw)

def start_spi() :
    '''
    Starteinstellungen für die SPI Schnittstelle
    open(0,0) für CS0
    open(0,1) für CS1
    Der LED Booster verwendet mode 0 (CPHA=0 und CPOL=0) für SPI

    '''
    spi.open(0, 0)  
    spi.mode = 0b00
    spi.max_speed_hz= 500000
    #spi.max_speed_hz= 12000000
    spi.writebytes([0xB1, LED_COUNT, 24])
    time.sleep(DELAY)

def led_weis():
    h=HELLIGKEIT_MAX
    spi.writebytes([0xA1, h, h,h, 0xA5, 0xB2])
    time.sleep(DELAY)

def leds_aus():
    spi.writebytes([0xA1, 0,0, 0, 0xA5, 0xB2])
    time.sleep(DELAY)
    pass

def berechnung_der_leds(wert):
    # Wert den Bereichen zu ordnen
    if wert >B2:
        # Bereich 80 bis 100
        gn=leds_gn
        gb=leds_gb
        wert_in_leds=(wert-B2)*leds_rt/(B3-B2)
        rt=int(wert_in_leds)
        rest= int((wert_in_leds % 1)*HELLIGKEIT_MAX)  #anzahl_leds                                                                                                      
        pass
    else:
        if wert > B1:
            # Bereich 60 bis 80
            gn=leds_gn
            rt=0
            wert_in_leds=(wert-B1)*leds_gb/(B2-B1)
            gb=int(wert_in_leds)
            rest= int((wert_in_leds % 1)*HELLIGKEIT_MAX)  #anzahl_leds
            pass
        else:
            rt=0
            gb=0
            # Bereich 0 bis 60
            # Berechnung der Werte für die LEDs anhand eines Beispielweertes                
            #print("Anzahlder LEDs:\t", wert*anzahl_leds/60)                                
            wert_in_leds=wert*leds_gn/B1
            gn=int(wert_in_leds)
            rest= int((wert_in_leds % 1)*HELLIGKEIT_MAX)  #anzahl_leds
            #print("Anzahl voller LEDs:\t",gn,"Rest:\t",rest)

        pass
            
    return [gn,gb,rt,rest]

def leds(leds):
    befehl=""
    pos=-1
    # Volle LEDs
    # grün
    for a in range (0, leds[0]):
        farbe_gn= str(0) + "," + str(HELLIGKEIT_MAX) + "," + str(0) 
        pos= str(a)
        led=FARBE_setzen + farbe_gn +LED_NR + pos + "," 
        befehl=befehl +led
    # gelb
    for a in range (0, leds[1]):
        farbe_gn= str(HELLIGKEIT_MAX) + "," + str(HELLIGKEIT_MAX) + "," + str(0)
        pos=str(a+leds_gn)
        led=FARBE_setzen + farbe_gn +LED_NR + pos + ","
        befehl=befehl +led
    # rot
    for a in range (0, leds[2]):
        farbe_gn= str(HELLIGKEIT_MAX) + ","+ str(0) + ","  + str(0)
        pos=str(a+leds_gn+leds_gb)
        led=FARBE_setzen + farbe_gn +LED_NR + pos + ","
        befehl=befehl +led
        
    gesamt_leds= leds[0]+leds[1]+leds[2]
    if gesamt_leds>=0:
        # einzelne Rest LED Grün                                                                               
        farbe_l=str(0) + "," + str(leds[3]) + "," + str(0)
        pos_l=LED_NR+ str(int(pos)+1)+ ","

    if gesamt_leds>(leds_gn-1):
        # einzelne Rest LED Gelb                                                                               
        farbe_l=str(leds[3]) + "," + str(leds[3]) + "," + str(0)
        pos_l=LED_NR+ str(int(pos)+1)+ ","

    if gesamt_leds > (leds_gn+leds_gb-1)  :
        # einzelne Rest LED Rot
        farbe_l=str(leds[3]) + "," + str(0) + "," + str(0)
        pos_l=LED_NR+ str(int(pos)+1)+ ","
        
    # volle und rest LED
    befehl=befehl+FARBE_setzen+farbe_l+pos_l
    leds=eval("["+befehl+"0xB2]")
    
    # Einschalten der LEDs
    spi.writebytes(leds)
    time.sleep(DELAY)
    return befehl
    pass

if __name__ == "__main__":
    try:
        start_spi()
        #led_weis()
        leds_aus()
        wert=20
        led_konf=berechnung_der_leds(wert)
        #print("LEDs Konfiguration:\t",led_konf)
        gn=leds(led_konf)
        #print("Rest:\t",gn)
        pass
    except KeyboardInterrupt:
        status()
        leds_aus()
        spi.close()


