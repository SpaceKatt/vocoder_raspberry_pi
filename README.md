# Vocoder w/ Raspberry Pi Project

Raspberry Pi MCP3008 code [inspired by Lady Ada's gist][adafruit-gist].

## Setup

### Ensure USB DAC is set with `-odac` flag

```
csound utils/get_device_list.csd
```

## Usage

1. Start vocoder

```
csound voscil.csd
```



## Csound

[adafruit-gist]: https://gist.github.com/ladyada/3151375
