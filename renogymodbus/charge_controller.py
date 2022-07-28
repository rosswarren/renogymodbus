import minimalmodbus
import serial

from renogymodbus.retriable_instrument import RetriableInstrument


class RenogyChargeController(RetriableInstrument):
    """Instrument class for Renogy Charge Controllers.

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

    def get_solar_voltage(self):
        """PV array input in volts"""
        return self.retriable_read_register(0x0107, 1, 3, False)

    def get_solar_current(self):
        """PV array input in amps"""
        return self.retriable_read_register(0x0108, 2, 3, False)

    def get_solar_power(self):
        """PV array input in watts"""
        return self.retriable_read_register(0x0109, 0, 3, False)

    def get_load_voltage(self):
        """Load output in volts"""
        return self.retriable_read_register(0x0104, 1, 3, False)

    def get_load_current(self):
        """Load output in amps"""
        return self.retriable_read_register(0x0105, 2, 3, False)

    def get_load_power(self):
        """Load output in watts"""
        return self.retriable_read_register(0x0106, 0, 3, False)

    def get_battery_voltage(self):
        """Battery voltage"""
        return self.retriable_read_register(0x0101, 1, 3, False)

    def get_battery_state_of_charge(self):
        """Battery state of charge"""
        return self.retriable_read_register(0x0100, 0, 3, False)

    def get_battery_temperature(self):
        """battery temperature"""
        register_value = self.retriable_read_register(0x0103, 0, 3, False)
        battery_temperature = register_value & 0b0000000001111111
        battery_temperature_sign = (register_value & 0b0000000010000000) >> 7
        battery_temperature = -battery_temperature if battery_temperature_sign == 1 else battery_temperature
        return battery_temperature

    def get_controller_temperature(self):
        """Temperature inside equipment"""
        register_value = self.retriable_read_register(0x0103, 0, 3, False)
        controller_temperature = (register_value & 0b0111111100000000) >> 8
        controller_temperature_sign = (register_value & 0b1000000000000000) >> 15
        controller_temperature = -controller_temperature if controller_temperature_sign == 1 else controller_temperature
        return controller_temperature

    def get_maximum_solar_power_today(self):
        """Max solar power today"""
        return self.retriable_read_register(0x010F, 0, 3, False)

    def get_minimum_solar_power_today(self):
        """Min solar power today"""
        return self.retriable_read_register(0x0110, 0, 3, False)

    def get_maximum_battery_voltage_today(self):
        """Maximum solar power today"""
        return self.retriable_read_register(0x010C, 1, 3, False)

    def get_minimum_battery_voltage_today(self):
        """Minimum solar power today"""
        return self.retriable_read_register(0x010B, 1, 3, False)
