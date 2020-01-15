"""
    The is the main device interface for the Keithley2400LV. This will be modified such that it can be used and called from the plot class
    which will plot the collected data.
"""


import time, serial, os, sys, datetime
import numpy as np
import threading as thr



"""
These are definitions that are used by many methods in the Keithley2400LV class below.
"""
def readKeithley(keithley2400LV):
    if sys.version_info.major == 3:
        oneByte = b""
        byteString = b""
        while oneByte is not  b'\n':
            oneByte = keithley2400LV.read()
            byteString += oneByte
    else:
        print("[Keithley] Error: Python 2 Is not Supported, Please ensure you are using Python3")
    return byteString


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
        self.serialDevice.write(":OUTP ON\n".encode("ASCII"))
        if self.verbose:
            print("The output for the Keithley 2400-LV has been set to ON")


    def turnOutput_OFF(self):
        self.serialDevice.write(":OUTP OFF\n".encode("ASCII"))
        if self.verbose:
            print("The output for the Keithley 2400-LV has been set to OFF")

    def getMeasermentVoltage(self):
        self.serialDevice.write('MEAS:VOLT?\n'.encode("ASCII"))
        voltageStr = self.serialDevice.readline()
        if self.verbose:
            print(voltageStr, "is the read voltage from the Keithley 2400-LV")
        return voltageStr

    def setKeithley2400LV_voltage(self, setVoltage):
        self.serialDevice.write(":FUNC VOLT\n:SOUR:VOLT ".encode("ASCII"))
        self.serialDevice.write(numberFormat(setVoltage))
        self.serialDevice.write("\n".encode("ASCII"))
        if self.verbose:
            print("Keithley 2400-LV was set to a voltage of", setVoltage)


    def getSourceCurrent(self):
        self.serialDevice.write(b'SOUR:CURR?\n')
        current = float(self.serialDevice.readline())
        if self.verbose:
            print(current, "is the read current from the Keithley 2400-LV")
        return current


    def setSourceCurrent(self, setCurrent):
        self.serialDevice.write("SOUR:FUNC CURR\n:SOUR:CURR ".encode("ASCII"))
        self.serialDevice.write(numberFormat(setCurrent))
        self.serialDevice.write("\n".encode("ASCII"))
        if self.verbose:
            print("Keithley 2400-LV was set to a current of", setCurrent, "Amps")



    # select 4-WIRE resistance function
    '''
        Config for cryo meas
        1. set the function to measure resistance
        2. source is to be set to manual
        3. sense is 4w
        4. guard cable //never changes
        5. set ranges
        6. config ohms offset compensation is enable
        7. speed set to high accuracty (use 10)
    '''
    def initResistanceMeasurement(self):
        self.serialDevice.write(b":SENSE:FUNC \"RES\" \n") #works
        #self.serialDevice.write(b':SENSE:VOLT:RANG 0 \n')
        self.serialDevice.write(b':SENS:RES:MODE MAN \n')
        self.serialDevice.write(b':SOUR:CURR:RANG 0.1 \n') # doesn't work
        self.serialDevice.write(b':SENSE:RES:RANG 0.01 \n')
        self.serialDevice.write(b':SENSE:RES:OCOM ON \n')
        #self.serialDevice.write(b':FORM:ELEM:SENSE: RES \n')
        self.serialDevice.write(b':SENS:VOLT:PROT 2 \n')
        self.serialDevice.write(b':SENS:CURR:PROT 0.01 \n')
        self.serialDevice.write(b':SOUR:FUNC CURR \n')
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

""" portName = "/dev/ttyUSB0"

keithley2400LV = Keithley2400LV(portName=portName, verbose=verbose)
keithley2400LV.openPort()
keithley2400LV.initResistanceMeasurement()
keithley2400LV.setSourceCurrent(10.0e-3)
keithley2400LV.turnOutput_ON() """

""" 
def resistance_Temp():
    try:
        TempA,TempB = readCryoCon()
        current = float(keithley2400LV.getSourceCurrent())
        bytestring = keithley2400LV.getMeasermentResistance()
        voltage = float(bytestring[0:13])
    #    print(bytestring[14:27])
    #    current = float(bytestring[14:27])
        resistance = float(bytestring[29:41])
        print(str('T = ') + str(TempA) + str(' K') + ', '+ str(TempB) + ' K' + ', ' + str('R = ') + str(resistance) + str(' Ohms') + ' , ' + str('V = ')+ str(voltage) + str(' V') + ', '+ str('I = ') + str(current) + str(' A') +'\n')
        f.write(str(TempA) +  ',' + str(resistance) + '\n')
        f.flush()
    except KeyboardInterrupt:
         f.flush()
         exit()
        

while True:
    resistance_Temp()
    time.sleep(0.1)
 """
""" keithley2400LV.turnOutput_OFF()
keithley2400LV.closePort() """

def main():
    print("[KEITHLEY] Begin Test")
    keithley2400LV = Keithley2400LV("/dev/ttyUSB0", True)
    keithley2400LV.openPort()
    keithley2400LV.initResistanceMeasurement()
    keithley2400LV.setSourceCurrent(10.0e-3)
    keithley2400LV.turnOutput_ON()
   
    # print("[KEITHLEY] Performed init")
    current = float(keithley2400LV.getSourceCurrent())
    # print("[KEITHLEY] Finised get getSourceCurrent()")
    bytestring = keithley2400LV.getMeasermentResistance()
    # print("[KEITHLEY] GOt Mesasurement of resistance")
    resistance = float(bytestring[29:41])
    print("Current read {}\tResistance read: {}\n".format(current, resistance))
    print("[KEITHLEY] End Test")
    keithley2400LV.turnOutput_OFF()
    print("[KEITHLEY] OUTPUT SET TO OFF")
    keithley2400LV.closePort()
    print("[KEITHLEY] POrt Closed")
if __name__ == "__main__":
    main()
