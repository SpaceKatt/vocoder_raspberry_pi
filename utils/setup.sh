#!/usr/bin/env bash
sudo apt update
sudo apt upgrade

# Install Cython
sudo apt install csound

# Install Csound

# Install dependencies for python-rtmidi
sudo apt install libasound2-dev libjack-dev

# Install RTMIDI package
python3 -m pip install python-rtmidi

