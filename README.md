# renogymodbus

This package is intended to help you communicate with a Renogy charge controller. It has been tested with a Renogy Rover Elite but should work with other Renogy devices.

## Features
* Read real time data
* Automatic retries

## Connecting to the charge controller



## Installing the package


To install the package run

```sh
pip install renogymodbus
```

This package requires Python 3, depending on your setup you might have to instead run:

```sh
pip3 install renogymodbus
```


## Command line utility

To run the command line utility and see the debug output run the following on the command line:

```sh
renogymodbus --portname /dev/ttyUSB0 --slaveaddress 1
```

```sh
usage: renogymodbus [-h] [--portname PORTNAME] [--slaveaddress SLAVEADDRESS]

optional arguments:
  -h, --help            show this help message and exit
  --portname PORTNAME   Port name for example /dev/ttyUSB0
  --slaveaddress SLAVEADDRESS
                        Slave address 1-247
```

Example output

```sh
```

## Python usage

To use the library within your Python code

```python
from renogymodbus.driver import RenogyChargeController

controller = RenogyChargeController("/dev/ttyUSB0", 1)
controller.get_solar_voltage()
```

See https://github.com/rosswarren/renogymodbus/blob/main/renogymodbus/driver.py for all available methods
