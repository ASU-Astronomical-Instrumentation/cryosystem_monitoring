'''
author: Cody Roberson
date: 1/13/2020
description: This is the main interface between the host pc and the cryocon ______ temperature sensors. The
values obtained from here will be made available upon request from the plotting algorithm.
'''

import serial

class Cryocon():
    def __init__(self):
        try:
            ser = serial.Serial("/dev/ttyUSB0", 9600, timeout=5)
        except (OSError, serial.SerialException):
            print("Serial Error, please ensure that the device is conected and the correct port is.")
        
        print("Init successfull")


def main():
    print("Main Function for testing functionality in cryocon.pyd")
    device = Cryocon()

if __name__=="__main__":
    main()