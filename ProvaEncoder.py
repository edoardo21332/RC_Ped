#!/usr/bin/env python3

import RPi.GPIO as GPIO

BUTTON_GPIO = 26
incremento = 0
def enco(): 
    if __name__ == '__main__':
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(BUTTON_GPIO, GPIO.IN)

        while True:
            GPIO.wait_for_edge(BUTTON_GPIO, GPIO.RISING)
            incremento = incremento + 1
         
            print(str(incremento))                                     
        
