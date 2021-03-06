#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
	Funktiontest der SPI Schnittstelle
	Raspberry Zero --- Digi-Dot Booster --- WS2812 LED
	Die LEDs leuten für 2 s Grün-Gelb und gehen dann aus  
'''

import spidev
import time
 
DELAY = 0.04
LED_COUNT = 30
spi = spidev.SpiDev()

# Starteinstellungen für die Schnittstelle  CS0
spi.open(0, 0)  
spi.mode = 0b00
spi.max_speed_hz= 500000

# Statusanzeige der  Einstellungen der Parameter für die Schnittstelle
bpw=spi.bits_per_word
cshigh= spi.cshigh
lsbfirst = spi.lsbfirst
speed= spi.max_speed_hz
mode = spi.mode
tw = spi.threewire
print("bpw:\t\t", bpw, "\ncshigh:\t\t", cshigh , "\nlsbfirst:\t", lsbfirst)
print("Speed:\t\t", speed,"\nMode:\t\t", mode ,"\nThreewire:\t",tw)

# Grundeinstellung für die LEDs
spi.writebytes([0xB1, LED_COUNT, 24])
time.sleep(DELAY)

# Einschalten aller LEDs und Festlegung der Farben 
spi.writebytes([0xA1, 255, 255, 0, 0xA5, 0xB2])
time.sleep(2)

# Ausschalten aller LEDs
spi.writebytes([0xA1, 0,0, 0, 0xA5, 0xB2])
time.sleep(DELAY)

print("Ich habe fertig!")
