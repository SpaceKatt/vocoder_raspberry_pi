#!/usr/bin/env python

import time
import os

import rtmidi
from rtmidi.midiconstants import NOTE_OFF, NOTE_ON, PITCH_BEND

import mcp3008_driver as MCP


DEBUG = 0


# 10k trim pot connected to adc #0
POTENTIOMETER_ADC = 0;

NOTE = 60  # middle C is 60

NOTE_CONSTANT_ON = [NOTE_ON, NOTE, 112]
NOTE_CONSTANT_OFF = [NOTE_OFF, NOTE, 0]

PITCH_MIDDLE = 0x2000


def pitch_bend_cmd(value):
    middle = 1024 / 2
    adjust =  value - middle

    pitch = int(adjust + PITCH_MIDDLE)

    pitch &= 0x3FFF
    lsb = pitch & 0x007F
    pitch >>= 7
    msb = pitch & 0x007F

    data = [lsb, msb]
    return data


def run_midi():
  midiout = rtmidi.MidiOut()

  time.sleep(0.5)

  last_read = 0
  tolerance = 5       # to keep from being jittery we'll only change
                      # volume when the pot has moved more than 5 'counts'

  with (midiout.open_port(0) if midiout.get_ports() else
        midiout.open_virtual_port("My virtual output")):

      note_on = [PITCH_BEND, 0x00, 0x40]

      # note_off = [NOTE_OFF, 0x50, 0x00]
      midiout.send_message(NOTE_CONSTANT_ON)

      trim_pot = 512

      while True:
          try:
              # read the analog pin
              trim_pot = MCP.readadc(POTENTIOMETER_ADC)
              # how much has it changed since the last read?
              pot_adjust = abs(trim_pot - last_read)

              if DEBUG:
                      print("trim_pot:", trim_pot)
                      print("pot_adjust:", pot_adjust)
                      print("last_read", last_read)

              if ( pot_adjust < tolerance ):
                  continue

              if DEBUG:
                      print("trim_pot_changed", trim_pot_changed)

              time_delta = 0.0001

              weight = 4.1459 * time_delta
              last_read += weight * (trim_pot - last_read)

              pitch_data = pitch_bend_cmd(last_read)

              note_on = [PITCH_BEND] + pitch_data

              midiout.send_message(note_on)

              time.sleep(time_delta)
          except KeyboardInterrupt:
              print("Keyboard Interrupt! Stop the presses!")
              print("Cleanup!")

              midiout.send_message(NOTE_CONSTANT_OFF)
              del midiout

              break

if __name__ == '__main__':
    MCP.setup_SPI()

    run_midi()

    MCP.teardown_SPI()

    exit()
