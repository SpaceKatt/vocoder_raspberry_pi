#!/usr/bin/env bash

# Install Cython

# Install dependencies for python-rtmidi
sudo apt update
sudo apt install libasound2-dev libjack-dev
python3 -m pip install python-rtmidi

