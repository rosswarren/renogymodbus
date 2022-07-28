import argparse
from renogymodbus import RenogyChargeController, RenogySmartBattery
from renogymodbus.find_slaveaddress import find_slaveaddress

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--portname", help="Port name for example /dev/ttyUSB0", default="/dev/ttyUSB0"
    )
    parser.add_argument(
        "--slaveaddress", help="Slave address 1-247", default=1, type=int
    )
    parser.add_argument(
        "--device", help="Device to read data from. Either charge_controller or smart_battery", choices=["charge_controller", "smart_battery"], default="charge_controller", type=str
    )
    parser.add_argument(
        "--find-slave-address", help="Find slave address of modbus device", action="store_true", default=False
    )
    args = parser.parse_args()

    if args.find_slave_address:
        print("Finding slave addresses...")
        addresses = find_slaveaddress(args.portname)

        if len(addresses) == 0:
            print("No modbus devices found")
        else:
            print("Found modbus devices at addresses:")
            for address in addresses:
                print(f"{address}")
    elif args.device == "charge_controller":
        print_charge_controller_output(args)
    elif args.device == "smart_battery":
        print_smart_battery_output(args)


def print_charge_controller_output(args):
    controller = RenogyChargeController(args.portname, args.slaveaddress)

    print("Real Time Charge Controller Data")
    print(f"Solar voltage: {controller.get_solar_voltage()}V")
    print(f"Solar current: {controller.get_solar_current()}A")
    print(f"Solar power: {controller.get_solar_power()}W")
    print(f"Load voltage: {controller.get_load_voltage()}V")
    print(f"Load current: {controller.get_load_current()}A")
    print(f"Load power: {controller.get_load_power()}W")
    print(f"Battery voltage: {controller.get_battery_voltage()}V")
    print(f"Battery state of charge: {controller.get_battery_state_of_charge()}%")
    print(f"Battery temperature: {controller.get_battery_temperature()}°C")
    print(f"Controller temperature: {controller.get_controller_temperature()}°C")
    print(f"Maximum solar power today: { controller.get_maximum_solar_power_today()}W")
    print(f"Minimum solar power today: { controller.get_minimum_solar_power_today()}W")
    print(f"Maximum battery voltage today: { controller.get_maximum_battery_voltage_today()}V")
    print(f"Minimum battery voltage today: { controller.get_minimum_battery_voltage_today()}V")

def print_smart_battery_output(args):
    battery = RenogySmartBattery(args.portname, args.slaveaddress)

    print("Real Time Smart Battery Data")
    print(f"Cell voltages: {battery.get_cell_voltages()}V")
    print(f"Cell temperatures: {battery.get_cell_temperatures()}°C")
    print(f"BMS temperature: {battery.get_bms_temperature()}°C")
    print(f"Environment temperatures: {battery.get_environment_temperatures()}°C")
    print(f"Heater temperatures: {battery.get_heater_temperatures()}°C")
    print(f"Current: {battery.get_current()}A")
    print(f"Voltage: {battery.get_voltage()}V")
    print(f"Remaining capacity: {battery.get_remaining_capacity()}Ah")
    print(f"Total capacity: {battery.get_total_capacity()}Ah")
    print(f"State of charge: {battery.get_state_of_charge()}%")
    print(f"Cycle number: {battery.get_cycle_number()}")
    print(f"Charge voltage limit: {battery.get_charge_voltage_limit()}V")
    print(f"Discharge voltage limit: {battery.get_discharge_voltage_limit()}V")
    print(f"Charge current limit: {battery.get_charge_current_limit()}A")
    print(f"Discharge current limit: {battery.get_discharge_current_limit()}A")

if __name__ == "__main__":
    main()
