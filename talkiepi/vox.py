#!/usr/bin/env python
#coding: utf8

## This is a VOX-Script.


import time
import RPi.GPIO as GPIO
import sys
marker = 1
while True:
    try:
        if marker == 0:
            file = open ("/sys/class/gpio/gpio25/device/gpio/gpio25/active_low","w")
            file.write("1")
            file.close()
            marker = 1
            time.sleep(60)
        if marker == 1:
            file = open ("/sys/class/gpio/gpio25/device/gpio/gpio25/active_low","w")
            file.write("0")
            file.close()
            marker = 0
        time.sleep(1)
    except (KeyboardInterrupt, SystemExit):
        file = open ("/sys/class/gpio/gpio25/device/gpio/gpio25/active_low","w")
        file.write("0")
        file.close()
        time.sleep(1)

sys.exit()
