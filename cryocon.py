'''
author: Cody Roberson
date: 1/13/2020
description: This is the main interface between the host pc and the CryoCon 32B Temperature Controller. The
values obtained from here will be made available upon request from the plotting algorithm.
'''

import serial
import sys
import os
import time


class Cryocon():
    def __init__(self, port):
        # create a serial object
        self.ser = serial.Serial()

        # Configure and attempt to open the serial port
        try:
           self.ser.baudrate = 9600
           self.ser.port = port
           self.ser.open()

        except (OSError, serial.SerialException):
            print("[Cryocon] Serial Error, please ensure that the device is conected and the correct port is selected.")

    def getTemperatures(self):
        TempA = None
        TempB = None
        if self.ser.is_open:
            try:
                # Get Temperature for Input A
                self.ser.write('INPUT? A\n'.encode("ASCII"))
                time.sleep(0.010)
                TempA = float(self.ser.readline())

                # Get temperature for Input B
                self.ser.write('INPUT? B\n'.encode("ASCII"))
                time.sleep(0.010)
                TempB = float(self.ser.readline())

                return TempA,TempB
            except ValueError:
                print("[Cryocon] Error: Data was not returned in a format that could be converted to a float.")
        else:
            print("[Cryocon] Error: Not connected to Cryocon")
        return (0,0)


    def closeConnection(self):
        if self.ser.is_open:
            self.ser.close()
            print("[Cryocon] Closed serial connection")
        else:
            print("[Cryocon] Serial Connection was already closed")

def main():
    if sys.version_info < (3,0):
        print("Error, please use python 3")
        exit()
    
    dev = Cryocon("/dev/ttyUSB0")
    print("Temperatures are {}".format(dev.getTemperatures()))
    dev.closeConnection()


if __name__=="__main__":
    main()