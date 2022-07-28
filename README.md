# renogymodbus

This package is intended to help you communicate with a Renogy charge controller. It has been tested with a Renogy Rover Elite but should work with other Renogy devices.

## Features
* Read real time data
* Automatic retries

## Connecting to the charge controller
Please check whether your charge controller has a rs232 or rs485 port.

### rs485
Voucher code for 7% off Renogy: https://go.referralcandy.com/share/672HVC9

* rs485 to USB serial cable (UK) https://uk.renogy.com/rs485-to-usb-serial-cable/
* rs485 to USB serial cable (US) https://renogy.com/rs485-to-usb-serial-cable/

<img width="693" alt="image" src="https://user-images.githubusercontent.com/613642/179362448-12a805d1-4475-45cc-b3d7-c8a8e9c4b409.png">

### rs232
Unfortunately the rs232 to USB serial cable has been discontinued by Renogy. It is possible to make your own.

<img width="690" alt="image" src="https://user-images.githubusercontent.com/613642/179362464-35bde1f8-fcb2-43d8-8a52-0232ffa210e8.png">


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
                   [--device {charge_controller,smart_battery}]
                   [--find-slave-address]

optional arguments:
  -h, --help            show this help message and exit
  --portname PORTNAME   Port name for example /dev/ttyUSB0
  --slaveaddress SLAVEADDRESS
                        Slave address 1-247
  --device {charge_controller,smart_battery}
                        Device to read data from. Either charge_controller or
                        smart_battery
  --find-slave-address  Find slave address of modbus device
```

Example output for charge controller
```sh
Real Time Charge Controller Data
Solar voltage: 43.1V
Solar current: 0.09A
Solar power: 4W
Load voltage: 0.0V
Load current: 0.0A
Load power: 0W
Battery voltage: 13.9V
Battery state of charge: 100%
Battery temperature: -37°C
Controller temperature: 48°C
Maximum solar power today: 51W
Minimum solar power today: 0W
Maximum battery voltage today: 14.0V
Minimum battery voltage today: 13.1V
```

Example output for smart battery
```
Real Time Smart Battery Data
Cell voltages: [3.3, 3.3, 3.3, 3.3, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]V
Cell temperatures: [24.0, 24.0, 24.0, 24.0, 1835.2, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]°C
BMS temperature: 0.0°C
Environment temperatures: [25.0, 25.0]°C
Heater temperatures: [25.0, 25.0]°C
Current: -0.2A
Voltage: 13.3V
Remaining capacity: 98.966Ah
Total capacity: 100.0Ah
State of charge: 98.966%
Cycle number: 0
Charge voltage limit: 14.8V
Discharge voltage limit: 10.0V
Charge current limit: 50.0A
Discharge current limit: -100.0A
```

## Python usage

To use the library within your Python code

### Charge Controller

```python
from renogymodbus import RenogyChargeController

controller = RenogyChargeController("/dev/ttyUSB0", 1)
controller.get_solar_voltage()
```

See https://github.com/rosswarren/renogymodbus/blob/main/renogymodbus/charge_controller.py for all available methods

### Smart Battery

```python
from renogymodbus import RenogySmartBattery

battery = RenogySmartBattery("/dev/ttyUSB0", 48)
battery.get_voltage()
```
See https://github.com/rosswarren/renogymodbus/blob/main/renogymodbus/smart_battery.py for all available methods
