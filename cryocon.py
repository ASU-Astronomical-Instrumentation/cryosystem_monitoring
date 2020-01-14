'''
author: Cody Roberson
date: 1/13/2020
description: This is the main interface between the host pc and the cryocon ______ temperature sensors. The
values obtained from here will be made available upon request from the plotting algorithm.
'''

import serial
import sys
import os

class Cryocon():
    def __init__(self):
        # create a serial object
        self.ser = serial.Serial()

        # Configure and attempt to open the serial port
        try:
           self.ser.baudrate = 9600
           self.ser.port = "/dev/ttyUSB0"
           self.ser.open()

        except (OSError, serial.SerialException):
            print("[Cryocon] Serial Error, please ensure that the device is conected and the correct port is selected.")


    def getTemperatures(self):
        return [0,0]


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
    
    dev = Cryocon()
    print(dev.getTemperatures())
    dev.closeConnection()


if __name__=="__main__":
    main()