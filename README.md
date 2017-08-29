# RPi_arch-linux_Digi-Dot_mit_WS2812

Dies soll einen Einstieg in das Ansteuern von WS2812 LEDs unter Arch Linux, 
Python und einem Raspberry Zero zeigen


HOWTO

	$ sudo pacman Syu


Verkabel für 8 LEDs   

    Hinweis:
        bei einer größeren Anzahl von LEDs sollte man eine externe 
	Spannungsversorgung nutzen da der Raspberry nicht den benötigtn Strom liefern kann

    zero            Digi-Dot Booster    WS 2812

    PIN  5V       ---   PIN 5V  ----    PIN 5V        
                        PIN 2   ----    Din
    PIN GND       ---   PIN GND ----    PIN GND

    SPI Schnittstelle

    PIN 19 MOSI   ---   PIN MOSI
    PIN 24 CS0    ---   PIN CS
    PIN 23 SCK    ---   PIN SCK

    MISO wird nicht benötig


Systemeinstellungen

    /boot/config.txt
 
    device_tree_param=spi=on
    
    lsmod
        Module                  Size  Used by
        spidev                  7148  0
        spi_bcm2835             6944  0

 
Rechte zuweisen für Anwender
    
    Datei 51-i2c.rules erstellen damit alle Benutzer aus der Gruppe 
	users darauf zugreifen können
    
        /etc/udev/rules.d/51-i2c.rules
            
            SUBSYSTEM=="spidev", GROUP="users", MODE="0660"

        ls -la /dev  liefert nach einem Neustart :
                
            crw-rw----  1 root users 153,   0 29. Aug 14:15 spidev0.0
            crw-rw----  1 root users 153,   1 29. Aug 14:15 spidev0.1

Software:

    python-spidev  
    
    $ yaourt spidev
    1 aur/python-spidev 3.2-1 (1) (0,00)
        Python bindings for Linux SPI access through spidev
    2 aur/python2-spidev 3.1-1 (0) (0,00)
        Python2 bindings for Linux SPI access through spidev
    ==> Geben Sie die Nummern der zu installierenden Pakete an (z.B. 1 2 3 
	oder 1-3)
    ==> 
	--------------------------------------------------------------------
    ==> 1
  
    dann ENTER
    
    python-spidev 3.2-1  (2016-04-21 12:20)
    (Nicht unterstütztes Paket: Potenziell gefährlich!)
    ==> PKGBUILD bearbeiten? [J/n] („A“ zum Abbrechen)
    ==> ----------------------------------------------
    ==> J

    Bitte $VISUAL zu Ihren Umgebungsvariablen hinzufügen
    Zum Beispiel:
    export VISUAL="vim" (in ~/.bashrc)
    (Ersetzen Sie vim mit ihrem bevorzugten Editor)

    ==> PKGBUILD bearbeiten mit: nano
    
    dann ENTER und die Zeile mit pkgname wie unten anpassen
    
    
    # Maintainer: Radek Podgorny <radek@podgorny.cz>

    pkgname=spidev-3.2
    pkgver=3.2
    pkgrel=1
    pkgdesc="Python bindings for Linux SPI access through spidev"
    
    dann strg-o -->  ENTER --> strg-x
    
    und normal den weiteren Anweisungen folgen
    
    
Testskript starten mit 

    $ python led.py
    oder
    $ chmod 744 led.py
    $ ./led.py
    
    
Die LEDs sollten für 2 s leuchten
