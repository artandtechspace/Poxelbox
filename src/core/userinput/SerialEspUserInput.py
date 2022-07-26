import serial
import glob
import time

from config import Config
from core.errors.InputError import InputError
from core.userinput.BaseUserInput import BaseUserInput


class SerialEspUserInput(BaseUserInput):
    # Serial connection object
    __ser = None

    # Returns all usb-ports with connected devices
    def __get_ports(self):
        # TODO: Note das this only works on Linux (Raspberry Pi)
        return glob.glob("/dev/ttyUSB*")

    # Opens the port
    def __open_port(self):

        # Gets all connected ports
        ports = self.__get_ports()

        # Ensures only one device got detected
        if len(ports) != 1:
            # TODO: Change to full error that crashes the system
            raise InputError(
                "Es wurden " + str(len(ports)) + " gefunden. Bitte schließe mindestens bzw. nur ein Gerät an.")

        # Opens the serial-connection
        self.__ser = serial.Serial(ports[0], Config.ESP_BAUD)

    # Updates the controller-input
    def update(self):
        try:

            # Ensures an open connection to the esp
            if self.__ser is None:
                self.__open_port()

            # Waits until data got found
            while self.__ser.inWaiting() >= 3:
                # Gets next data
                data = self.__ser.read(3)

                # Performs checksum-check using XOR
                if data[0] ^ data[1] != data[2]:
                    print("Error detected")
                    # Kills remaining bytes to prevent out-of-sync
                    self.__ser.read(self.__ser.inWaiting())
                    return

                # Reads in the packet and executes the callback
                self._on_change(data[0] | (data[1] << 8))

        except serial.serialutil.SerialException:
            # TODO: Change to full error that crashes the system
            print("Serial-port error. Retrying on next run...")
            time.sleep(1)
