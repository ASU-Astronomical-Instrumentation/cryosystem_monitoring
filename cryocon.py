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

'''
    This class is everything pertaining to the Cryocon device. 
'''
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
                self.ser.write(b'INPUT? A\n')
                time.sleep(0.010)
                TempA = float(self.ser.readline())

                # Get temperature for Input B
                self.ser.write(b'INPUT? B\n')
                time.sleep(0.010)
                TempB = float(self.ser.readline())

                return TempA,TempB
            except ValueError:
                print("[Cryocon] Error: Data was not returned in a format that could be converted to a float.\
                        perhaps the cryocon was not connected to the right port?")
        else:
            print("[Cryocon] Error: Not connected to Cryocon")
        return (0,0)


    def closeConnection(self):
        if self.ser.is_open:
            self.ser.close()
            print("[Cryocon] Closed serial connection")
        else:
            print("[Cryocon] Serial Connection was already closed")

    def getLoopSettings(self, interf : serial.Serial, loop : bytes):
        """
        Prints all relevant settings for either loop 1 or loop 2
        of the cryocon.

        Parameters
        ----------
        interf : serial.Serial
            serial connection to cryocon.
        loop : bytes
            This is really an internal param. This should either be b'1'
            or b'2' for loop 1 and loop 2

        Returns
        -------
        list[] size 14 of settings in order

        """
        try:
            loopstr = loop.decode("utf-8")
            interf.write(b'LOOP ' + loop + b':SOURCE? \n')
            time.sleep(0.010)
            temp = interf.readline()
            print("Loop {} source: {}".format(loopstr, temp.decode('utf-8')))
            
            interf.write(b'LOOP '+loop+ b':SETPT? \n')
            time.sleep(0.010)
            temp = interf.readline()
            print("Loop {} setpoint: {}".format(loopstr, temp.decode('utf-8')))
            
            interf.write(b'LOOP '+loop+ b':TYPE? \n')
            time.sleep(0.010)
            temp = interf.readline()
            print("Loop {} type: {}".format(loopstr, temp.decode('utf-8')))
            
            interf.write(b'LOOP '+loop+ b':MAXSET? \n')
            time.sleep(0.010)
            temp = interf.readline()
            print("Loop {} max setpoint: {}".format(loopstr, temp.decode('utf-8')))
            d
            print("Loop {} resistance (ohms):  {}".format(loopstr, temp.decode('utf-8')))
            
            interf.write(b'LOOP '+loop+ b':RATE? \n')
            time.sleep(0.010)
            temp = interf.readline()
            print("Loop {} ramp rate (per minute): {}".format(loopstr, temp.decode('utf-8')))
            
            interf.write(b'LOOP '+loop+ b':RANGE? \n')
            time.sleep(0.010)
            temp = interf.readline()
            print("Loop {} range: {}".format(loopstr, temp.decode('utf-8')))
            
            interf.write(b'LOOP '+loop+ b':PGAIN? \n')
            time.sleep(0.010)
            temp = interf.readline()
            print("Loop {} pgain: {}".format(loopstr, temp.decode('utf-8')))
            
            interf.write(b'LOOP '+loop+ b':IGAIN? \n')
            time.sleep(0.010)
            temp = interf.readline()
            print("Loop {} igain: {}".format(loopstr, temp.decode('utf-8')))
            
            interf.write(b'LOOP '+loop+ b':DGAIN? \n')
            time.sleep(0.010)
            temp = interf.readline()
            print("Loop {} dgain: {}".format(loopstr, temp.decode('utf-8')))
            
            interf.write(b'LOOP '+loop+ b':PMAN? \n')
            time.sleep(0.010)
            temp = interf.readline()
            print("Loop {} pman: {}".format(loopstr, temp.decode('utf-8')))
            
            interf.write(b'LOOP '+loop+ b':MAXPWR? \n')
            time.sleep(0.010)
            temp = interf.readline()
            print("Loop {} maxpower: {}".format(loopstr, temp.decode('utf-8')))
            
            interf.write(b'LOOP '+loop+ b':OUTPWR? \n')
            time.sleep(0.010)
            temp = interf.readline()
            print("Loop {} output power: {}".format(loopstr, temp.decode('utf-8')))
            
            interf.write(b'LOOP '+loop+ b':TABLE? \n')
            time.sleep(0.010)
            temp = interf.readline()
            print("Loop {} table number: {}".format(loopstr, temp.decode('utf-8')))
        
        except (OSError, serial.SerialException):
            print("getLoopSettings() -> Port error, couldn't connect to the cryocon")

def main():
    if sys.version_info < (3,0):
        print("Error, please use python 3")
        exit()
    
    dev = Cryocon("COM8")
    print("Temperatures are {}".format(dev.getTemperatures()))
    dev.closeConnection()


if __name__=="__main__":
    main()