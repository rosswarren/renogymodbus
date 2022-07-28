import minimalmodbus
import serial

from renogymodbus.retriable_instrument import RetriableInstrument


class RenogySmartBattery(RetriableInstrument):
    """Instrument class for Renogy Smart Batteries.

    Args:
        * portname (str): port name
        * slaveaddress (int): slave address in the range 1 to 247

    """

    def __init__(self, portname, slaveaddress):
        super().__init__(portname, slaveaddress)
        self.serial.baudrate = 9600
        self.serial.bytesize = 8
        self.serial.parity = serial.PARITY_NONE
        self.serial.stopbits = 1
        self.serial.timeout = 1
        self.mode = minimalmodbus.MODE_RTU

        self.clear_buffers_before_each_transaction = True
        
    def get_cell_voltages(self):
        """
        The cell voltages in Volts.
        """
        return list(map(lambda n: n / 10, self.retriable_read_registers(5001, 16, 3)))

    def get_cell_temperatures(self):
        """
        The cell temperatures in degrees C.
        """
        return list(map(lambda n: n / 10, self.retriable_read_registers(5018, 16, 3)))

    def get_bms_temperature(self):
        """
        The BMS board temperature in degrees C.
        """
        return self.retriable_read_register(5035, 1, 3, False)

    def get_environment_temperatures(self):
        """
        The environment temperatures in degrees C.
        """
        return list(map(lambda n: n / 10, self.retriable_read_registers(5037, 2, 3)))

    def get_heater_temperatures(self):
        """
        The heater temperatures in degrees C.
        """
        return list(map(lambda n: n / 10, self.retriable_read_registers(5040, 2, 3)))

    def get_current(self):
        """
        The current in Amps.
        """
        return self.retriable_read_register(5042, 2, 3, True)
    
    def get_voltage(self):
        """
        The voltage in Volts.
        """
        return self.retriable_read_register(5043, 1, 3, False)

    def get_remaining_capacity(self):
        """
        The remaining charge in Ah.
        """
        return self.retriable_read_long(5044) / 1000

    def get_total_capacity(self):
        """
        The total capacity in Ah.
        """
        return self.retriable_read_long(5046) / 1000

    def get_state_of_charge(self):
        """
        The state of charge as a percentage.
        """
        return (self.get_remaining_capacity() / self.get_total_capacity()) * 100

    def get_cycle_number(self):
        """
        The cycle number.
        """
        return self.retriable_read_register(5048, 0, 3, False)

    def get_charge_voltage_limit(self):
        """
        The charge voltage limit in Volts.
        """
        return self.retriable_read_register(5049, 1, 3, False)

    def get_discharge_voltage_limit(self):
        """
        The discharge voltage limit in Volts.
        """
        return self.retriable_read_register(5050, 1, 3, False)

    def get_charge_current_limit(self):
        """
        The charge current limit in Amps.
        """
        return self.retriable_read_register(5051, 2, 3, False)

    def get_discharge_current_limit(self):
        """
        The discharge current limit in Amps.
        """
        return self.retriable_read_register(5052, 2, 3, True)
    