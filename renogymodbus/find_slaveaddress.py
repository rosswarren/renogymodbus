import minimalmodbus

def find_slaveaddress(portname):
    """
    Find the slave address of a modbus device.

    Args:
        portname: The name of the serial port.
    """
    instrument = minimalmodbus.Instrument(portname, slaveaddress=247)
    instrument.serial.baudrate = 9600
    instrument.serial.timeout = 0.1

    for address in range(0x01, 0xf8):
        instrument.address = address
        try:
            try:
                value = instrument.read_string(0x1402, 8)
                print(address, value)
            except:
                value = instrument.read_string(0x000C, 16)
                print(address, value)
        except:
            pass
