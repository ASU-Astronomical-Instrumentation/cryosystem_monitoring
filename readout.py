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
              
class cryoconHeater():
    def __init__(self):
        self.SerialIfc = serial.Serial()
        try:
            print("Attempting to open serial connection...")
            ## Settings go here ##
            self.SerialIfc.baudrate = 9600
            self.SerialIfc.port = "/dev/ttyUSB1"
            self.SerialIfc.timeout = 1
            self.SerialIfc.open()
            
        except (OSError, serial.SerialException):
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
        loopstr = loop.decode("utf-8")
        interf.write(b'LOOP ' + loop + ':SOURCE? \n')
        time.sleep(0.010)
        temp = interf.readline()
        print("Loop {} source: {}".format(loopstr, temp.decode('utf-8')))
        
        interf.write(b'LOOP '+loop+':SETPT? \n')
        time.sleep(0.010)
        temp = interf.readline()
        print("Loop {} setpoint: {}".format(loopstr, temp.decode('utf-8')))
        
        interf.write(b'LOOP '+loop+':TYPE? \n')
        time.sleep(0.010)
        temp = interf.readline()
        print("Loop {} type: {}".format(loopstr, temp.decode('utf-8')))
        
        interf.write(b'LOOP '+loop+':MAXSET? \n')
        time.sleep(0.010)
        temp = interf.readline()
        print("Loop {} max setpoint: {}".format(loopstr, temp.decode('utf-8')))
        
        interf.write(b'LOOP '+loop+':LOAD? \n')
        time.sleep(0.010)
        temp = interf.readline()
        print("Loop {} resistance (ohms):  {}".format(loopstr, temp.decode('utf-8')))
        
        interf.write(b'LOOP '+loop+':RATE? \n')
        time.sleep(0.010)
        temp = interf.readline()
        print("Loop {} ramp rate (per minute): {}".format(loopstr, temp.decode('utf-8')))
        
        interf.write(b'LOOP '+loop+':RANGE? \n')
        time.sleep(0.010)
        temp = interf.readline()
        print("Loop {} range: {}".format(loopstr, temp.decode('utf-8')))
        
        interf.write(b'LOOP '+loop+':PGAIN? \n')
        time.sleep(0.010)
        temp = interf.readline()
        print("Loop {} pgain: {}".format(loopstr, temp.decode('utf-8')))
        
        interf.write(b'LOOP '+loop+':IGAIN? \n')
        time.sleep(0.010)
        temp = interf.readline()
        print("Loop {} igain: {}".format(loopstr, temp.decode('utf-8')))
        
        interf.write(b'LOOP '+loop+':DGAIN? \n')
        time.sleep(0.010)
        temp = interf.readline()
        print("Loop {} dgain: {}".format(loopstr, temp.decode('utf-8')))
        
        interf.write(b'LOOP '+loop+':PMAN? \n')
        time.sleep(0.010)
        temp = interf.readline()
        print("Loop {} pman: {}".format(loopstr, temp.decode('utf-8')))
        
        interf.write(b'LOOP '+loop+':MAXPWR? \n')
        time.sleep(0.010)
        temp = interf.readline()
        print("Loop {} maxpower: {}".format(loopstr, temp.decode('utf-8')))
        
        interf.write(b'LOOP '+loop+':OUTPWR? \n')
        time.sleep(0.010)
        temp = interf.readline()
        print("Loop {} output power: {}".format(loopstr, temp.decode('utf-8')))
        
        interf.write(b'LOOP '+loop+':TABLE? \n')
        time.sleep(0.010)
        temp = interf.readline()
        print("Loop {} table number: {}".format(loopstr, temp.decode('utf-8')))
    
    
    def lazyfn(self):
        print("lazyfn()")


    def printMenu(self):
        print("\n** MENU **\n")
        print("1. Print loop 1's settings")
        print("2. Print loop 2's settings")
        
        print("3. Set loop 1's settings")
        print("4. Set loop 2's settings")
        
        print("5. Change Loop 1's Setpoint")
        print("6. Change Loop 2's setpoint")

        print("7. upload PID table")
        
        print("8. Enable Loops (control button on panel)")
        print("9. Stop Loops (stop button on panel")
        
        print("CTRL + c to exit")
        
    
    
    def menuControl(self):
        cls()
        self.printMenu()
        
        
        while True:
            # Get user input
            usrinpt = ""
            try:
                usrinpt = input(prompt="Please enter choice 1-7: ")
            except KeyboardInterrupt:
                print("\nKeyboard Interupt, Exiting\n")
                return
            
            # Act on user input
            if usrinpt == "1":
                self.getLoopSettings(self.SerialIfc, b'1')
            elif usrinpt == "2":
                self.getLoopSettings(self.SerialIfc, b'2')
        

if __name__ == "__main__":
    # Test
    cryo = cryoconHeater()
    cryo.menuControl()