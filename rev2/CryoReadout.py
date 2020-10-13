#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct  3 16:41:50 2020

@author: cody
"""

import tkinter as tk
from tkinter import ttk
from SerialHelper import serial_ports

class serialPortsWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        pad = 10
        cbb1_str = tk.StringVar()
        cbb2_str = tk.StringVar()
        tk.Label(self, text="Please select ports",  font=("Helvetica", 16)).grid(row = 1, column = 1, pady = pad, padx = pad)
        self.tkl1 = tk.Label(self, text="Keithly Port")
        self.cbb1 = ttk.Combobox(self, width = 25, textvariable=cbb1_str)
        self.cbb2 = ttk.Combobox(self, width = 25, textvariable=cbb2_str)

        SerialOptions = serial_ports()
        # TODO: FILL COMBOBOX WITH VALUES FROM SERIAL PORT QUERY
        self.cbb1['values'] = SerialOptions
        self.cbb2['values'] = SerialOptions
        self.tkl2 = tk.Label(self, text="cryocon Port")

        self.tkl1.grid(row = 2, column = 1, padx = pad, pady = pad)
        self.cbb1.grid(row = 2, column = 2, padx = pad, pady = pad)
        self.tkl2.grid(row = 3, column = 1, padx = pad, pady = pad)
        self.cbb2.grid(row = 3, column = 2, padx = pad+10, pady = pad+10)
        self.btn1 = tk.Button(self, text="Connect", command=self.bind_connect_button)
        self.btn1.grid(row=4, column=1, padx=pad, pady=pad)
    def bind_connect_button(self):
        print("button pressed")
        self.destroy()
        

    def show(self):
        self.grab_set()
        self.wait_window()


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.win = serialPortsWindow(self)



if __name__=='__main__':
    app = App()
    app.mainloop()

        