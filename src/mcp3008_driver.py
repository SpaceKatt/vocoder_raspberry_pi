#!/usr/bin/env python

# Written by Limor "Ladyada" Fried for Adafruit Industries, (c) 2015
# This code is released into the public domain
import RPi.GPIO as GPIO


GPIO.setmode(GPIO.BCM)


DEBUG = 0


# change these as desired - they're the pins connected from the
# SPI port on the ADC to the Cobbler
SPICLK = 18
SPIMISO = 23
SPIMOSI = 24
SPICS = 25

def setup_SPI():
    # set up the SPI interface pins
    GPIO.setup(SPIMOSI, GPIO.OUT)
    GPIO.setup(SPIMISO, GPIO.IN)
    GPIO.setup(SPICLK, GPIO.OUT)
    GPIO.setup(SPICS, GPIO.OUT)

def teardown_SPI():
    GPIO.cleanup()

# read SPI data from MCP3008 chip, 8 possible adc's (0 thru 7)
def readadc(adcnum):
    if ((adcnum > 7) or (adcnum < 0)):
            return -1

    GPIO.output(SPICS, True)

    GPIO.output(SPICLK, False)  # start clock low
    GPIO.output(SPICS, False)     # bring CS low

    commandout = adcnum
    commandout |= 0x18  # start bit + single-ended bit
    commandout <<= 3    # we only need to send 5 bits here

    for i in range(5):
            if (commandout & 0x80):
                    GPIO.output(SPIMOSI, True)
            else:
                    GPIO.output(SPIMOSI, False)

            commandout <<= 1

            GPIO.output(SPICLK, True)
            GPIO.output(SPICLK, False)

    adcout = 0
    # read in one empty bit, one null bit and 10 ADC bits
    for i in range(12):
        GPIO.output(SPICLK, True)
        GPIO.output(SPICLK, False)

        adcout <<= 1

        if (GPIO.input(SPIMISO)):
            adcout |= 0x1

    GPIO.output(SPICS, True)

    adcout >>= 1       # first bit is 'null' so drop it
    return adcout
