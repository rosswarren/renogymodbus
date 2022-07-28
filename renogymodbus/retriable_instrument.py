import minimalmodbus
from retrying import retry

class RetriableInstrument(minimalmodbus.Instrument):
    def __init__(self, port, slaveaddress):
        super().__init__(port, slaveaddress)

    @retry(wait_fixed=200, stop_max_attempt_number=5)
    def retriable_read_register(
        self, registeraddress, number_of_decimals, functioncode, signed
    ):
        return self.read_register(
            registeraddress, number_of_decimals, functioncode, signed
        )

    @retry(wait_fixed=200, stop_max_attempt_number=5)
    def retriable_read_registers(
        self, registeraddress, number_of_registers, functioncode
    ):
        return self.read_registers(
            registeraddress, number_of_registers, functioncode
        )

    @retry(wait_fixed=200, stop_max_attempt_number=5)
    def retriable_read_long(
        self, registeraddress
    ):
        return self.read_long(
            registeraddress
        )
    
    @retry(wait_fixed=200, stop_max_attempt_number=5)
    def retriable_read_bit(self, registeraddress, functioncode):
        return self.read_bit(registeraddress, functioncode)