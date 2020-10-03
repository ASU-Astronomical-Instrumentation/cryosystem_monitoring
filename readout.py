"""
@author  Cody A. Roberson
@date    2020-09-21
@file    readout.py
@desc    This code is allows the user to control the loop settings 
            'heater ramping' of the cryocon 32b over serial interface
"""

import serial, time, os

def cls():
    os.system('cls' if os.name=='nt' else 'clear')

def getInputAsString(msg : str):
    res = ""
    try:
        res = input(msg)
    except KeyboardInterrupt:
        print("\nKeyboard Interupt, Exiting\n")
        input("\nPress enter to continue...")
        raise
    return res
                         
class cryoconHeater():
    def __init__(self):
        self.initSerialIF()
    
    def initSerialIF(self):
        self.SerialIfc = serial.Serial()
        try:
            print("Attempting to open serial connection...")
            ## Settings go here ##
            self.SerialIfc.baudrate = 9600
            self.SerialIfc.port = "/dev/ttyUSB1"
            self.SerialIfc.timeout = 0.75  # r/w timeout
            self.SerialIfc.open()
            
        except (OSError, se rial.SerialException):
            print("Port error, couldn't connect to the cryocon")
            # self.SerialIfc.close()


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
        None.

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
            
            interf.write(b'LOOP '+loop+ b':LOAD? \n')
            time.sleep(0.010)
            temp = interf.readline()
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


    def getPIDTableSettings(self, interf : serial.Serial, pidIndex : str):
        """
        Gets specified PID table from cryocon (0-5) and prints to screen

        Parameters
        ----------
        interf : serial.Serial
            Serial connection to cryocon
        pidIndex : str
            Number 0-5

        Returns
        -------
        None.

        """
        tbl = pidIndex.encode("ASCII")
        try:
            print("Printing table at index "+ pidIndex + "\n")
            interf.write(b'PIDTABLE '+tbl+':TABLE?\n')
            time.sleep(0.010)
            temp = interf.readlines()
            for line in temp:
                print(line.decode('utf-8'))
        
        except (OSError, serial.SerialException):
            print("getPIDTableSettings() -> Port error, couldn't connect to the cryocon")


    def printMenu(self):
        print("\n** MENU **\n")
        print("1. Print loop 1's settings")
        print("2. Print loop 2's settings")
        print("3. Print PID Table (0-5)")
        
        print("4. Set loop 1's settings")
        print("5. Set loop 2's settings")
        
        print("6. Change Loop 1's Setpoint")
        print("7. Change Loop 2's setpoint")

        print("8. upload PID table (0-5)")
        
        print("9. Enable Loops (control button on panel)")
        print("10. Stop Loops (stop button on panel")
        
        print("\nCTRL + c to exit")


    def menuControl(self):
        cls()
        
        while True:
            self.printMenu()
            
            # Get user input
            usrinpt = getInputAsString("Please enter choice 1-7: ")
            
            # Act on user input
            if usrinpt == "1":
                self.getLoopSettings(self.SerialIfc, b'1')
            elif usrinpt == "2":
                self.getLoopSettings(self.SerialIfc, b'2')
            elif usrinpt == "3":
                pass
            
            # Give user pause and allow them to loop again
            # TODO: I realized that Sasha and Farzad may want to have the loop
            #   settings be more persistent on screen even if it is a bit..spammy
            input("\nPress enter to continue...")
            cls()
            

if __name__ == "__main__":
    # Test
    cryo = cryoconHeater()
    cryo.menuControl()