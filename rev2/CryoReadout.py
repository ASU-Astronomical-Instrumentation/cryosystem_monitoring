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
        # self.win = serialPortsWindow(self)
        pad = 10

        self.labelframe_loop1 = tk.LabelFrame(self, text="LOOP 1", padx = pad, pady = pad)
        self.labelframe_loop2 = tk.LabelFrame(self, text="LOOP 2", padx = pad, pady = pad)
        self.labelframe_usercontrols = tk.LabelFrame(self, text = "CONTROLS", padx = pad, pady = pad)
        self.labelframe_loop1.grid(row = 1, column = 1, padx = pad, pady = pad)
        self.labelframe_loop2.grid(row = 2, column = 1, padx = pad, pady = pad)
        self.labelframe_usercontrols.grid(row = 3, column = 1, padx = pad, pady = pad)
        
        # LOOP 1 LABELS
        tk.Label(self.labelframe_loop1, text="source: ").grid(row = 1, column = 1)
        tk.Label(self.labelframe_loop1, text="setpoint: ").grid(row = 2, column = 1)
        tk.Label(self.labelframe_loop1, text="type: ").grid(row = 3, column = 1)
        tk.Label(self.labelframe_loop1, text="max-setpt: ").grid(row = 4, column = 1)
        tk.Label(self.labelframe_loop1, text="resistance: ").grid(row = 5, column = 1)
        tk.Label(self.labelframe_loop1, text="ramprate: ").grid(row = 6, column = 1)
        tk.Label(self.labelframe_loop1, text="range: ").grid(row = 7, column = 1)
        tk.Label(self.labelframe_loop1, text="pgain: ").grid(row = 8, column = 1)
        tk.Label(self.labelframe_loop1, text="igain: ").grid(row = 9, column = 1)
        tk.Label(self.labelframe_loop1, text="dgain: ").grid(row = 10, column = 1)
        tk.Label(self.labelframe_loop1, text="pman: ").grid(row = 11, column = 1)
        tk.Label(self.labelframe_loop1, text="max-power: ").grid(row = 12, column = 1)
        tk.Label(self.labelframe_loop1, text="outputpower: ").grid(row = 13, column = 1)
        tk.Label(self.labelframe_loop1, text="table-number: ").grid(row = 14, column = 1)

        # LOOP 1 ENTRIES
        self.loop1_entries = []
        for i in range(1, 15):
            entry = tk.Entry(self.labelframe_loop1, width = 12, state=tk.DISABLED)
            entry.grid(row = i, column = 2)
            self.loop1_entries.append(entry)

        # LOOP 2 LABELS
        tk.Label(self.labelframe_loop2, text="source: ").grid(row = 1, column = 1)
        tk.Label(self.labelframe_loop2, text="setpoint: ").grid(row = 2, column = 1)
        tk.Label(self.labelframe_loop2, text="type: ").grid(row = 3, column = 1)
        tk.Label(self.labelframe_loop2, text="max-setpt: ").grid(row = 4, column = 1)
        tk.Label(self.labelframe_loop2, text="resistance: ").grid(row = 5, column = 1)
        tk.Label(self.labelframe_loop2, text="ramprate: ").grid(row = 6, column = 1)
        tk.Label(self.labelframe_loop2, text="range: ").grid(row = 7, column = 1)
        tk.Label(self.labelframe_loop2, text="pgain: ").grid(row = 8, column = 1)
        tk.Label(self.labelframe_loop2, text="igain: ").grid(row = 9, column = 1)
        tk.Label(self.labelframe_loop2, text="dgain: ").grid(row = 10, column = 1)
        tk.Label(self.labelframe_loop2, text="pman: ").grid(row = 11, column = 1)
        tk.Label(self.labelframe_loop2, text="max-power: ").grid(row = 12, column = 1)
        tk.Label(self.labelframe_loop2, text="outputpower: ").grid(row = 13, column = 1)
        tk.Label(self.labelframe_loop2, text="table-number: ").grid(row = 14, column = 1)

        # LOOP 2 ENTRIES
        self.loop2_entries = []
        for i in range(1, 15):
            entry = tk.Entry(self.labelframe_loop2, width = 12, state=tk.DISABLED)
            entry.grid(row = i, column = 2)
            self.loop2_entries.append(entry)

        # USER CONTROLS
        

if __name__=='__main__':
    app = App()
    app.mainloop()

