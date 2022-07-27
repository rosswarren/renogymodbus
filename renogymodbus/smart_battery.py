import minimalmodbus
import serial
from retrying import retry


class RenogySmartBattery(minimalmodbus.Instrument):
    """Instrument class for Renogy Smart Batteries.

    Args:
        * portname (str): port name
        * slaveaddress (int): slave address in the range 1 to 247

    """

    def __init__(self, portname, slaveaddress):
        minimalmodbus.Instrument.__init__(self, portname, slaveaddress)
        self.serial.baudrate = 9600
        self.serial.bytesize = 8
        self.serial.parity = serial.PARITY_NONE
        self.serial.stopbits = 1
        self.serial.timeout = 1
        self.mode = minimalmodbus.MODE_RTU

        self.clear_buffers_before_each_transaction = True

    @retry(wait_fixed=200, stop_max_attempt_number=5)
    def retriable_read_register(
        self, registeraddress, number_of_decimals, functioncode=3, signed=False
    ):
        return self.read_register(
            registeraddress, number_of_decimals, functioncode, signed
        )

    @retry(wait_fixed=200, stop_max_attempt_number=5)
    def retriable_read_long(
        self, registeraddress
    ):
        return self.read_long(
            registeraddress
        )

    def get_current(self):
        """
        The current in Amps.
        """
        return self.retriable_read_register(0x13b2, 2, 3, True)
    
    def get_voltage(self):
        """
        The voltage in Volts.
        """
        return self.retriable_read_register(0x13b3, 1)

    def get_remaining_charge(self):
        """
        The remaining charge in mAh.
        """
        return self.retriable_read_long(0x13b4)

    def get_capacity(self):
        """
        The capacity in mAh.
        """
        return self.retriable_read_long(0x13b6)

    def get_state_of_charge(self):
        """
        The state of charge as a percentage.
        """
        return (self.get_remaining_charge() / self.get_capacity()) * 100
