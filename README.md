# mysmartusb_manager
Manager for the MySmartUSB light programmer in Linux. Written in Python3.
Allows to control the voltage provided by the device and lists information.

## Dependencies
python-pyserial

## Usage
Download [mysmartusb_manager.py](mysmartusb_manager.py)
> ./mysmartusb_manager

Output should look something like this: 
> Using port /dev/ttyUSB0
> Found device: myAVR - mySmartUSB light V1.11.1897
> Mode STK500
> Port /dev/ttyUSB0
> Current Voltage: 5V
> 
> 
> [0] Set power on
> [1] Set power off
> [2] Toggle voltage				5V
> [3] Toggle power on burn		OFF
> 
> 
> [q] Quit


Enter 0, 1, 2, 3 to set power/voltages accordingly. Enter q to quit.
