#!/usr/bin/env python

# Written by Limor "Ladyada" Fried for Adafruit Industries, (c) 2015
# This code is released into the public domain

import time
import os
import RPi.GPIO as GPIO

import rtmidi

from rtmidi.midiconstants import NOTE_OFF, NOTE_ON


# import ctcsound

GPIO.setmode(GPIO.BCM)
DEBUG = 0

# read SPI data from MCP3008 chip, 8 possible adc's (0 thru 7)
def readadc(adcnum, clockpin, mosipin, misopin, cspin):
        if ((adcnum > 7) or (adcnum < 0)):
                return -1
        GPIO.output(cspin, True)

        GPIO.output(clockpin, False)  # start clock low
        GPIO.output(cspin, False)     # bring CS low

        commandout = adcnum
        commandout |= 0x18  # start bit + single-ended bit
        commandout <<= 3    # we only need to send 5 bits here

        for i in range(5):
                if (commandout & 0x80):
                        GPIO.output(mosipin, True)
                else:
                        GPIO.output(mosipin, False)
                commandout <<= 1
                GPIO.output(clockpin, True)
                GPIO.output(clockpin, False)

        adcout = 0
        # read in one empty bit, one null bit and 10 ADC bits
        for i in range(12):
                GPIO.output(clockpin, True)
                GPIO.output(clockpin, False)
                adcout <<= 1
                if (GPIO.input(misopin)):
                        adcout |= 0x1

        GPIO.output(cspin, True)

        adcout >>= 1       # first bit is 'null' so drop it
        return adcout

# change these as desired - they're the pins connected from the
# SPI port on the ADC to the Cobbler
SPICLK = 18
SPIMISO = 23
SPIMOSI = 24
SPICS = 25

# set up the SPI interface pins
GPIO.setup(SPIMOSI, GPIO.OUT)
GPIO.setup(SPIMISO, GPIO.IN)
GPIO.setup(SPICLK, GPIO.OUT)
GPIO.setup(SPICS, GPIO.OUT)

# 10k trim pot connected to adc #0
potentiometer_adc = 0;

last_read = 0       # this keeps track of the last potentiometer value
tolerance = 5       # to keep from being jittery we'll only change
                    # volume when the pot has moved more than 5 'counts'

NOTE = 60  # middle C
note_on = [NOTE_ON, NOTE, 112]
note_off = [NOTE_OFF, NOTE, 0]

midiout = rtmidi.MidiOut()

with (midiout.open_port(0) if midiout.get_ports() else
      midiout.open_virtual_port("My virtual output")):
    note_on = [NOTE_ON, NOTE, 112]
    while True:
        try:
            midiout.send_message(note_off)
            # we'll assume that the pot didn't move
            trim_pot_changed = False

            # read the analog pin
            trim_pot = readadc(potentiometer_adc, SPICLK, SPIMOSI, SPIMISO, SPICS)
            # how much has it changed since the last read?
            pot_adjust = abs(trim_pot - last_read)

            if DEBUG:
                    print("trim_pot:", trim_pot)
                    print("pot_adjust:", pot_adjust)
                    print("last_read", last_read)

            if ( pot_adjust > tolerance ):
                   trim_pot_changed = True

            if DEBUG:
                    print("trim_pot_changed", trim_pot_changed)

            time_delta = 0.4

            weight = 3.1459 * time_delta
            last_read += weight * (trim_pot - last_read)

            # hang out and play a note for a half second
            NOTE = 60 + (trim_pot / 25.0)

            note_on = [NOTE_ON, NOTE, 112]
            note_off = [NOTE_OFF, NOTE, 0]

            midiout.send_message(note_on)
            time.sleep(time_delta)
        except KeyboardInterrupt:
            print("Keyboard Interrupt! Stop the presses!")
            print("Cleanup!")
            midiout.send_message(note_off)
            del midiout
            GPIO.cleanup()
            exit()
