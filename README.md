# Vocoder w/ Raspberry Pi Project

Platform: Raspberry Pi 3 Model B
OS: Raspbian

Raspberry Pi MCP3008 driver code [inspired by Lady Ada's gist][adafruit-gist].

## Setup

0. Download Repository to Raspberry Pi

1. Install dependencies

```
./utils/setup.sh
```

2. Inspect USB DAC and Mic

   - The

```
csound utils/get_device_list.csd
```

## Usage

0. SSH into Raspberry Pi, in two separate terminals

1. Start vocoder in one terminal

```
csound voscil.csd
```

2. Start MIDI controller in other terminal

```
python3 adafruit_mcp3008.py
```

3. End session by using Ctrl-C in each terminal

## Csound

### Modifying Vocoder Parameters

### Save to File

[adafruit-gist]: https://gist.github.com/ladyada/3151375
