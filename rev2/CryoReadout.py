#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct  3 16:41:50 2020

@author: cody
"""

import tkinter as tk
from tkinter import ttk

class serialPortsWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.geometry('680x420')
        cbb1_str = tk.StringVar(value="please select COM port")
        self.tkl1 = tk.Label(self, text="Keithly Port")
        self.cbb1 = ttk.Combobox(self, width = 25, textvariable=cbb1_str)
        # TODO: FILL COMBOBOX WITH VALUES FROM SERIAL PORT QUERY
        self.cbb1['values'] = ('/dev/ttyUSB0', '/dev/ttyUSB1')
        self.tkl2 = tk.Label(self, text="cryocon Port")
        
        self.tkl1.grid(column = 1, row = 1)


    def show(self):
        self.grab_set()
        self.wait_window()


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.win = serialPortsWindow(self)
        self.win.show()

if __name__=='__main__':
    app = App()
    app.mainloop()

        