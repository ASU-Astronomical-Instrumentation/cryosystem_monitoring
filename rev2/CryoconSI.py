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
        self.status = "dcd"
        # Configure and attempt to open the serial port
        try:
            self.ser.baudrate = 9600
            self.ser.port = port
            self.ser.open()
            self.ser.timeout = 0.6
            self.status = "connected"
        except (OSError, serial.SerialException):
            print("[Cryocon] Serial Error, please ensure that the device is conected and the correct port is selected.")
            self.status = "dcd"

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
# 

    def gethtrCurr(self):
        htrCurr = []
        self.ser.write(b'LOOP 1:HTRREAD? \n')
        time.sleep(0.010)
        temp = self.ser.readline()
        htrCurr.append(temp.decode('utf-8'))

        self.ser.write(b'LOOP 2:HTRREAD? \n')
        time.sleep(0.010)
        temp = self.ser.readline()
        htrCurr.append(temp.decode('utf-8'))

        return htrCurr


    def getRampStatus(self):
        rampstatus = []
        self.ser.write(b'LOOP 1:RAMP? \n')
        time.sleep(0.010)
        temp = self.ser.readline()
        rampstatus.append(temp.decode('utf-8'))

        self.ser.write(b'LOOP 2:RAMP? \n')
        time.sleep(0.010)
        temp = self.ser.readline()
        rampstatus.append(temp.decode('utf-8'))

        return rampstatus

    def setLoopSettings(self, loop : bytes, settings : list):
        """
        Prints all relevant settings for either loop 1 or loop 2
        of the cryocon.

        Parameters
        ----------
        interf : serial.Serial
            serial connection to cryocon.
        settings : list[string]
            List of settings in order as get/set
        loop : bytes
            This is really an internal param. This should either be b'1'
            or b'2' for loop 1 and loop 2

        Returns
        -------
        list[] size 14 components

        """
        param = []
        for s in settings:
            g = str.encode(s, "ASCII")
            param.append(g)
        try:
            self.ser.write(b'LOOP ' + loop + b':SOURCE ' + param[0] + b' \n')
            time.sleep(0.010)

            self.ser.write(b'LOOP '+loop+ b':SETPT ' + param[1] + b' \n')
            time.sleep(0.010)

            self.ser.write(b'LOOP '+loop+ b':TYPE ' + param[2] + b' \n')
            time.sleep(0.010)

            self.ser.write(b'LOOP '+loop+ b':MAXSET ' + param[3] + b' \n')
            time.sleep(0.010)

            self.ser.write(b'LOOP '+loop+ b':LOAD' + param[4] + b' \n')
            time.sleep(0.010)

            self.ser.write(b'LOOP '+loop+ b':RATE' + param[5] + b' \n')
            time.sleep(0.010)
            
            self.ser.write(b'LOOP '+loop+ b':RANGE ' + param[6] + b' \n')
            time.sleep(0.010)
            
            self.ser.write(b'LOOP '+loop+ b':PGAIN ' + param[7] + b' \n')
            time.sleep(0.010)
            
            self.ser.write(b'LOOP '+loop+ b':IGAIN ' + param[8] + b' \n')
            time.sleep(0.010)

            self.ser.write(b'LOOP '+loop+ b':DGAIN ' + param[9] + b' \n')
            time.sleep(0.010)
            
            self.ser.write(b'LOOP '+loop+ b':PMAN ' + param[10] + b' \n')
            time.sleep(0.010)

            self.ser.write(b'LOOP '+loop+ b':MAXPWR ' + param[11] + b' \n')
            time.sleep(0.010)
            
            # self.ser.write(b'LOOP '+loop+ b':OUTPWR ' + param[12] + b' \n')
            # time.sleep(0.010)  NOT SETTABLE
            
            self.ser.write(b'LOOP '+loop+ b':TABLEIX ' + param[13] + b' \n')
            time.sleep(0.010)


        except (OSError, serial.SerialException):
            print("getLoopSettings() -> Port error, couldn't connect to the cryocon")
        
        return None

    def __getReply(self):
        temp = self.ser.readline()
        temp = temp.decode('utf-8')
        temp = temp.strip()
        return temp
    
    def startLoops(self):
        try:
            self.ser.write(b'CONTROL \n')
        except (OSError, serial.SerialException):
            print("getLoopSettings() -> Port error, couldn't connect to the cryocon")

    def stopLoops(self):
        try:
            self.ser.write(b'STOP \n')
        except (OSError, serial.SerialException):
            print("getLoopSettings() -> Port error, couldn't connect to the cryocon")


    def __parsePIDTable(self, filename : str):
        if filename == None:
            filename = 'pidtable.cfg'
        file = open(filename, "r")
        inputdata = file.readlines()
        file.close()

        if len(inputdata) > 17:
            print("ERROR, too many rows in configuration file. Format should be 'table name' followed by up to 16 pid table rows")
        elif len(inputdata) <= 1:
            print("ERROR: Not enough data. Format should be 'table name' followed by up to 16 pid table rows")
        else:
            cmd = b'PIDTABLE 0:TABLE\n '
            for line in inputdata:
                cmd = cmd + (line.encode('ascii'))
            cmd = cmd + (b'\n;')
            return cmd


    def writePIDTABLE(self):
        self.ser.write(self.__parsePIDTable(None))


    def getPIDTableSettings(self) -> str:
        self.ser.write(b'PIDTABLE 0:NENTRY?\n')
        temp = self.ser.readline()
        # print("PID TABLE NUMBER OF ENTRIES: {}".format(temp.decode('utf-8')))

        self.ser.write(b'PIDTABLE 0:TABLE?\n')
        timeout = self.ser.timeout
        self.ser.timeout = 1
        temp = self.ser.readlines()
        dat = ""
        for line in temp:
            # print(line.decode('utf-8'))
            dat = dat + line.decode('utf-8')

        self.ser.timeout = timeout
        return dat

    def getLoopSettings(self, loop : bytes):
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
        list[] size 14 components

        """
        settings = []
        try:
            self.ser.write(b'LOOP ' + loop + b':SOURCE? \n')
            settings.append(self.__getReply())
            
            self.ser.write(b'LOOP '+loop+ b':SETPT? \n')
            settings.append(self.__getReply())
            
            self.ser.write(b'LOOP '+loop+ b':TYPE? \n')
            settings.append(self.__getReply())
            
            self.ser.write(b'LOOP '+loop+ b':MAXSET? \n')
            settings.append(self.__getReply())
            
            self.ser.write(b'LOOP '+loop+ b':LOAD? \n')
            settings.append(self.__getReply())
            
            self.ser.write(b'LOOP '+loop+ b':RATE? \n')
            settings.append(self.__getReply())
            
            self.ser.write(b'LOOP '+loop+ b':RANGE? \n')
            settings.append(self.__getReply())
            
            self.ser.write(b'LOOP '+loop+ b':PGAIN? \n')
            settings.append(self.__getReply())
            
            self.ser.write(b'LOOP '+loop+ b':IGAIN? \n')
            settings.append(self.__getReply())
            
            self.ser.write(b'LOOP '+loop+ b':DGAIN? \n')
            settings.append(self.__getReply())
            
            self.ser.write(b'LOOP '+loop+ b':PMAN? \n')
            settings.append(self.__getReply())
            
            self.ser.write(b'LOOP '+loop+ b':MAXPWR? \n')
            settings.append(self.__getReply())
            
            self.ser.write(b'LOOP '+loop+ b':OUTPWR? \n')
            settings.append(self.__getReply())
            
            self.ser.write(b'LOOP '+loop+ b':TABLE? \n')
            settings.append(self.__getReply())

        except (OSError, serial.SerialException):
            print("getLoopSettings() -> Port error, couldn't connect to the cryocon")
        
        return settings

def main():
    if sys.version_info < (3,0):
        print("Error, please use python 3")
        exit()
    
    dev = Cryocon("COM8")
    print("Temperatures are {}".format(dev.getTemperatures()))
    dev.closeConnection()


if __name__=="__main__":
    main()