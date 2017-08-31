#!/usr/bin/env python
# -*- coding: utf-8 -*-                                                             
                                                                                    
import spidev                                                                       
import time                                                                         
                                                                                    
DELAY = 0.04                                                                        
LED_COUNT =8                                                                        
# Anzahl der LEDs für Farbeverlauf von der Zeilfarbe zu Weis                        
# Links und Rechts der LED                                                          
LED_FARBVERLAUF=3                                                                   
'''                                                                                 
Normierung  der Farben Rot ,Grün und Blau                                           
ROT_MAX=116                                                                         
GRUEN_MAX=61                                                                        
BLAU_MAX=255                                                                        
'''                                                                                 
HELLIGKEIT_MAX=40                                                                   
ROT_MAX=HELLIGKEIT_MAX                                                              
GRUEN_MAX=HELLIGKEIT_MAX                                                            
BLAU_MAX=HELLIGKEIT_MAX                                                             
                                                                                    
FARBE="0xA1,"                                                                       
LED_NR=",0xA4,"                                                                     
ANZEIGEN="0xB2]"                                                                    
                                                                                    
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
    #spi.max_speed_hz= 500000
    spi.max_speed_hz= 12000000
    led_count=LED_COUNT+2*LED_FARBVERLAUF
    spi.writebytes([0xB1, led_count, 24])
    time.sleep(DELAY)

def led_weis():
    h=HELLIGKEIT_MAX
    spi.writebytes([0xA1, h, h,h, 0xA5, 0xB2])
    time.sleep(DELAY)
    
def led_rot(p):

    led1="0xA1,60,60,60,0xA4,"+ str(p)   +","
    led2="0xA1,60,40,40,0xA4,"+ str(p+1) +","
    led3="0xA1,60,20,20,0xA4,"+ str(p+2) +","
    led4="0xA1,60, 0, 0,0xA4,"+ str(p+3) +","
    led5="0xA1,60,20,20,0xA4,"+ str(p+4) +","
    led6="0xA1,60,40,40,0xA4,"+ str(p+5) +","
    led7="0xA1,60,60,60,0xA4,"+ str(p+6) +","
    leds=eval("["+led1+led2+led3+led4+led5+led6+led7+"0xB2]")
    spi.writebytes(leds)
    time.sleep(DELAY)
  
def led_blau(p):
    #print(len(abstufung))
    befehl=""
    for a in range (-(len(abstufung)-1),len(abstufung)):
        farbe1= str(abstufung[abs(a)]) + "," + str(abstufung[abs(a)]) + "," + str(BLAU_MAX)
        pos=LED_NR + str(p+a)+ ","
        led=FARBE + farbe1 + pos 
        befehl=befehl +led

    leds=eval("["+befehl+"0xB2]")
    #print (leds)
    spi.writebytes(leds)
    time.sleep(DELAY)

def led_blau2(p):
    '''
    Blau mit Kontrastanpassung
    '''
    befehl=""
    for a in range (-(len(abstufung)-1),len(abstufung)):
        farbe1= str(abstufung[abs(a)]) + "," + str(abstufung[abs(a)]) + "," + str(BLAU_MAX-abstufung_sollfarbe[abs(a)])
        pos=LED_NR + str(p+a)+ ","
        led=FARBE + farbe1 + pos
        befehl=befehl +led

    leds=eval("["+befehl+"0xB2]")
    #print (leds)                                                                   
    spi.writebytes(leds)
    time.sleep(DELAY)

def leds_aus():
    spi.writebytes([0xA1, 0,0, 0, 0xA5, 0xB2])
    time.sleep(DELAY)
    pass

if __name__ == "__main__":
    try:
        p=0
        start_spi()
        abstufung2=[]
        abstufung=[]
        for a in range (0,4):
            # Abstufung von Weis nach Zeilfarbe
            abstufung.append(a*int(HELLIGKEIT_MAX/LED_FARBVERLAUF))
            # reduzierung der Zielfarbe um den Kontrast zu erhöhen
            abstufung2.append(a*int((HELLIGKEIT_MAX)/LED_FARBVERLAUF/2))
        abstufung_sollfarbe=abstufung2[::-1]
            
        #farbe_soll="blau"            
        farbe_soll="blau2"
        #led_weis()
    
        while True:
            # 
            p= p % (8+LED_FARBVERLAUF)
            
            if farbe_soll == "blau" :
                led_blau(p)
            if farbe_soll == "rot":
                led_rot(p)
            if farbe_soll == "blau2":
                led_blau2(p)
                
            p +=1
        pass
    except KeyboardInterrupt:
        status()
        leds_aus()
        spi.close()


