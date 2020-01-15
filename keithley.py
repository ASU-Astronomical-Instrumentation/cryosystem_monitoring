"""
    file: keithley.py
    date: 2020-01-15
    author: cody roberson (carobers@asu.edu), Hamdi Mani (Hamdi.Mani@asu.edu)
    The is the main device interface for the Keithley2400LV. This will be modified such that it can be used and called from the plot class
    which will plot the collected data.

    Note: It seems that in pythong 3, defining someVariable = b"somestr"
            sets the datatype to bytes and is equivalent to using "somestringhere".encode("ASCII"). This is more cleaner looking than pasting
            encoding functions everywhere.
"""


import time, serial, os, sys, datetime
import numpy as np
import threading as thr

'''
    Converts numbers into scientific notation for setting values in the keithley.
    NOTE: converts float to the 'bytes' datatype
'''
def numberFormat(number):
    if sys.version_info.major == 3:
        formattedString = bytes(str('%1.6e' % number), "UTF-8")
    else:
        formattedString = str("%1.6e" % number)
    return formattedString


"""
This is the class to control the Keithley 2400 LV
"""
class Keithley2400LV():
    def __init__(self, portName, verbose=False):
        self.verbose = verbose

        self.serialDevice = serial.Serial()
        self.serialDevice.port = portName
        self.serialDevice.baudrate = 9600
        self.serialDevice.bytesize = 8
        self.serialDevice.stopbits = 1
        self.serialDevice.parity = "N"
        self.serialDevice.timeout = 2

    def openPort(self):
        try:
            self.serialDevice.open()
        except (OSError, serial.SerialException):
            print("[KEITHLEY] Serial Error, please ensure that the device is conected and the correct port is selected.")
            exit()

    def closePort(self):
        self.serialDevice.close()


    def turnOutput_ON(self):
        self.serialDevice.write(b":OUTP ON\n")
        if self.verbose:
            print("The output for the Keithley 2400-LV has been set to ON")


    def turnOutput_OFF(self):
        self.serialDevice.write(b":OUTP OFF\n")
        if self.verbose:
            print("The output for the Keithley 2400-LV has been set to OFF")

    def getMeasermentVoltage(self):
        self.serialDevice.write(b"MEAS:VOLT?\n")
        voltageStr = self.serialDevice.readline()
        if self.verbose:
            print(voltageStr, "is the read voltage from the Keithley 2400-LV")
        return voltageStr

    def setKeithley2400LV_voltage(self, setVoltage):
        self.serialDevice.write(b":FUNC VOLT\n:SOUR:VOLT ")
        self.serialDevice.write(numberFormat(setVoltage))
        self.serialDevice.write(b"\n")
        if self.verbose:
            print("Keithley 2400-LV was set to a voltage of", setVoltage)


    def getSourceCurrent(self):
        self.serialDevice.write(b'SOUR:CURR?\n')
        current = float(self.serialDevice.readline())
        if self.verbose:
            print(current, "is the read current from the Keithley 2400-LV")
        return current


    def setSourceCurrent(self, setCurrent):
        self.serialDevice.write(b"SOUR:FUNC CURR\n:SOUR:CURR ")
        self.serialDevice.write(numberFormat(setCurrent))
        self.serialDevice.write(b"\n")
        if self.verbose:
            print("Keithley 2400-LV was set to a current of", setCurrent, "Amps")



    # select 4-WIRE resistance function
    '''
        TODO: Some of the range settings should not be hard coded and instead, should be a set of constants in their own
                python file

        Config for cryo meas. 
        1. set the function to measure resistance
        2. source is to be set to manual
        3. sense is 4w
        4. guard cable //never changes
        5. set ranges
        6. config ohms offset compensation is enable
        7. speed set to high accuracty (use 10)
    '''
    def initResistanceMeasurement(self):
        self.serialDevice.write(b":SENSE:FUNC \"RES\" \n") # Set the Keithley to measure resistance
        self.serialDevice.write(b':SENS:RES:MODE MAN \n') # Set the ohm mode to manual
        self.serialDevice.write(b':SOUR:CURR:RANG 0.1 \n') # Set the current range to 0.1
        self.serialDevice.write(b':SENSE:RES:RANG 0.01 \n')# set the resistance range to 0.01 Ohms
        self.serialDevice.write(b':SENSE:RES:OCOM ON \n') # enable ohms offset compensation
        self.serialDevice.write(b':SENS:VOLT:PROT 2 \n') # set voltage protection to 2 Volts
        self.serialDevice.write(b':SENS:CURR:PROT 0.01 \n') # set currnet protection to 0.01
        self.serialDevice.write(b':SOUR:FUNC CURR \n') # Set source mode to current
        self.serialDevice.write(b':SYST:RSEN ON \n') # ON for 4-wire measurments

    def getMeasermentResistance(self):
            self.serialDevice.write(b':READ?\n')
            resistanceStr = self.serialDevice.readline()
            if self.verbose:
                print(resistanceStr, "is the read resistance from the Keithley 2400-LV")
            return resistanceStr

    def getRange_Keithley2400LV(self):
        writeString = b":CURR:RANG?\n"
        self.serialDevice.write(writeString)
        theRange = self.serialDevice.readline()
        if self.verbose:
            print(theRange, "is the current RANGE from the Keithley 2400-LV")
        return theRange


###############################################################################
############################################################################### 


'''
    Used to test control and functionality of the keithley software by connecting, setting it to measure resistance,
    and printing the result.
'''
def main():
    print("[KEITHLEY] Begin Test")
    keithley2400LV = Keithley2400LV("/dev/ttyUSB0", True)
    keithley2400LV.openPort()
    keithley2400LV.initResistanceMeasurement()
    keithley2400LV.setSourceCurrent(10.0e-3)
    print("[KEITHLEY] Commanded settings")

    # Confirm before turning the thing on
    usrin = input(prompt="Enable output? [y/n]")

    if usrin == "y":
        keithley2400LV.turnOutput_ON()
        current = float(keithley2400LV.getSourceCurrent())
        bytestring = keithley2400LV.getMeasermentResistance()
        resistance = float(bytestring[29:41])
        print("Current read {}\tResistance read: {}\n".format(current, resistance))
        print("[KEITHLEY] End Test")
        keithley2400LV.turnOutput_OFF()
        print("[KEITHLEY] OUTPUT SET TO OFF")
        keithley2400LV.closePort()
        print("[KEITHLEY] POrt Closed")
        
    else:
        print("[KEITHLEY] Aborting and closing connection")
        keithley2400LV.closePort()
        exit()

if __name__ == "__main__":
    main()
