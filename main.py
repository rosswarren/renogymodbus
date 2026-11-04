import argparse
import sys

import minimalmodbus
import serial

from renogymodbus import RenogyChargeController


def scan(controller: RenogyChargeController, port: serial.Serial) -> int:
    port.timeout = 0.3
    found = []
    for address in [*range(1, 248), 255]:
        controller.address = address
        try:
            voltage = controller.read_register(0x0101, 1, 3, False)
        except minimalmodbus.ModbusException:
            continue
        found.append(address)
        print(f"Response from slave {address}: battery voltage {voltage:.1f} V")

    if not found:
        print("No device answered at any slave address.", file=sys.stderr)
        return 1
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Test a Renogy controller through a Waveshare TCP serial bridge."
    )
    parser.add_argument(
        "--host",
        default="172.17.204.243",
        help="Waveshare TCP server IP address",
    )
    parser.add_argument(
        "--tcp-port",
        default=4196,
        type=int,
        help="Waveshare TCP server port",
    )
    parser.add_argument(
        "--slave-address",
        default=1,
        type=int,
        help="Renogy Modbus slave address",
    )
    parser.add_argument(
        "--scan",
        action="store_true",
        help="Try every slave address (1-247 and 255) and report responders",
    )
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Print the raw bytes sent and received",
    )
    args = parser.parse_args(argv)

    port = None
    try:
        port = serial.serial_for_url(
            f"socket://{args.host}:{args.tcp_port}",
            baudrate=9600,
            bytesize=8,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            timeout=1,
        )
        controller = RenogyChargeController(port, args.slave_address)
        controller.debug = args.debug

        if args.scan:
            return scan(controller, port)

        voltage = controller.get_battery_voltage()
    except serial.SerialException as exc:
        print(f"Could not connect to Waveshare TCP server: {exc}", file=sys.stderr)
        return 1
    except minimalmodbus.ModbusException as exc:
        print(
            "TCP connected, but the controller did not return a valid Modbus "
            f"response: {exc}",
            file=sys.stderr,
        )
        print(
            "Check the slave address, RS-485 wiring, and converter serial settings.",
            file=sys.stderr,
        )
        return 1
    finally:
        if port is not None:
            port.close()

    print(
        f"Modbus RTU test passed: {args.host}:{args.tcp_port}, "
        f"slave {args.slave_address}"
    )
    print(f"Battery voltage: {voltage:.1f} V")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
