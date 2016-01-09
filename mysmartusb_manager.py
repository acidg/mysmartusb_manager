#!/bin/python3

import sys
import os
import serial
from binascii import unhexlify

port = ""
command_prefix = b'\xe6\xb5\xba\xb9\xb2\xb3\xa9'

# Get the port
if len(sys.argv) != 2:
    ports = ["/dev/" + dev for dev in os.listdir("/dev/") if dev.startswith("ttyUSB")]

    if len(ports) == 1:
        port = ports[0]
    else:
        print("Please select port:")
        for i, port in enumerate(ports):
            print("[" + str(i) + "] " + port)

        try:
            selection = int(input())

            if selection not in range(len(ports)):
                raise ValueError

            port = ports[selection]
        except ValueError:
            print("Device not listed", file=sys.stderr)
            exit(1)
else:
    port = sys.argv[1]

print("Using port " + port)

connection = serial.Serial(port=port, baudrate=115200, timeout=3)


# -------------------------- IO commands --------------------------

def send_command(command, return_all=False):
    data = command_prefix + unhexlify(command)
    connection.write(data)

    response = connection.readline()

    if not response:
        return

    if return_all:
        return response.decode('ISO-8859-1')[:-2]
    else:
        return response.decode('ISO-8859-1')[:-2].split('±')[1]


# ----------------------------- Getter -----------------------------

def get_device_info():
    response = send_command("76", True)
    if not response:
        print("Device not responding", file=sys.stderr)
        exit(1)
    return response.split('÷')[1]


def get_voltage():
    return str(send_command("5E")) + "V"


def get_emulation_mode():
    mode = send_command("74")
    if mode == "s":
        return "STK500"
    elif mode == "a":
        return "AVR911"
    else:
        return "UNKNOWN"


def get_power_on_burn():
    state = send_command("25")
    if state == "w":
        return "ON"
    elif state == "W":
        return "OFF"
    else:
        return "UNKNOWN"


def get_voltage_reading():
    return send_command("5E")


# ----------------------------- Setter -----------------------------

def set_power(on=True):
    if on:
        send_command("2B")
    else:
        send_command("2D")


def toggle_voltage():
    voltage = get_voltage()
    if voltage == "5V":
        send_command("33")
    else:
        send_command("35")


def toggle_power_on_burn():
    status = get_power_on_burn()
    if status == "OFF":
        send_command("77")
        return

    send_command("57")


# ------------------------------ Main ------------------------------

def print_menu():
    # os.system('clear')
    print("Found device: " + get_device_info())
    print("Mode " + get_emulation_mode())
    print("Port " + port)
    print("Current Voltage: " + get_voltage_reading() + "V\n\n")
    print("[0] Set power on")
    print("[1] Set power off")
    print("[2] Toggle voltage\t\t\t\t" + get_voltage())
    print("[3] Toggle power on burn\t\t" + get_power_on_burn())

    print("\n\n[q] Quit")


while True:
    print_menu()
    selection = input()

    if selection == 'q':
        exit(0)

    elif selection == '0':
        set_power(True)
        continue

    elif selection == '1':
        set_power(False)
        continue

    elif selection == '2':
        toggle_voltage()
        continue

    elif selection == '3':
        toggle_power_on_burn()
        continue

    elif selection == '4':
        continue

    elif selection == '5':
        continue
    else:
        print("Invalid input")
