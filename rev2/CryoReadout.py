#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct  3 16:41:50 2020

@author: cody
"""

######################################################################################################
cryoconPORT = ""
keithleyPort = ""
######################################################################################################

import tkinter as tk
from tkinter import ttk
from tkinter import font
from SerialHelper import serial_ports
import CryoconSI
import KeithlySI
import time

cc = CryoconSI.Cryocon(cryoconPORT)
keith = KeithlySI.Keithley2400LV(keithleyPort, False)
keith.openPort()
keith.initResistanceMeasurement()
keith.setSourceCurrent(1e-5) # 1.0e-7 For Nanos
keith.turnOutput_ON()

# TODO: ENABLE ME FOR PORT PROTEC
if cc.status == "dcd":
    print("ERROR, COULDNT CONNECT TO PORT")
    exit(0)

import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

#  NOT IMPLEMENTED
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

        # GUI SECTION
        # self.win = serialPortsWindow(self)
        pad = 5
        default_font = font.nametofont("TkTextFont")
        default_font.configure(size=12)
        self.graphFrame = tk.Frame(self)
        self.controlFrame = tk.Frame(self)
        self.controlFrame.grid(row = 1, column = 1, padx = pad, pady = pad)
        ttk.Separator(self, orient=tk.VERTICAL).grid(row = 1, column = 2, rowspan=3, sticky='ns', padx = pad, pady = pad)
        self.graphFrame.grid(row = 1, column = 3, padx = pad, pady = pad)


        self.labelframe_temp = tk.LabelFrame(self.controlFrame, text = "CURRENT TEMPS", padx = pad, pady = pad)
        self.labelframe_loop1 = tk.LabelFrame(self.controlFrame, text="LOOP 1", padx = pad, pady = pad)
        self.labelframe_loop2 = tk.LabelFrame(self.controlFrame, text="LOOP 2", padx = pad, pady = pad)
        self.labelframe_usercontrols = tk.LabelFrame(self.controlFrame, text = "CONTROLS", padx = pad, pady = pad)



        self.labelframe_temp.grid(row = 1, column = 1, padx = pad, pady = pad)
        self.labelframe_loop1.grid(row = 2, column = 1, padx = pad, pady = pad)
        self.labelframe_loop2.grid(row = 3, column = 1, padx = pad, pady = pad)
        self.labelframe_usercontrols.grid(row = 4, column = 1, padx = pad, pady = pad)
        
        ## place holder figure until a redraw update can occur
        self.mainFigure = Figure(figsize=(10,10), dpi=100)
        self.fig_subplotA = self.mainFigure.add_subplot(211)
        self.fig_subplotB = self.mainFigure.add_subplot(212)
        canvas = FigureCanvasTkAgg(self.mainFigure, self.graphFrame)
        canvas.get_tk_widget().grid(row=1, column = 1)


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
        self.loop1_button_edit = tk.Button(self.labelframe_loop1, text="EDIT", command=self.binding_loop1_changeParams)
        self.loop1_button_edit.grid(row = 15, column=1, pady = pad)
        self.loop1_button_done = tk.Button(self.labelframe_loop1, text="DONE", state = tk.DISABLED, command=self.binding_loop1_saveParams)
        self.loop1_button_done.grid(row = 15, column=2, pady = pad)

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
        self.loop2_button_edit = tk.Button(self.labelframe_loop2, text="EDIT")
        self.loop2_button_edit.grid(row = 15, column=1, pady = pad)
        self.loop2_button_done = tk.Button(self.labelframe_loop2, text="DONE", state = tk.DISABLED)
        self.loop2_button_done.grid(row = 15, column=2, pady = pad)

        # LOOP 2 ENTRIES
        self.loop2_entries = []
        for i in range(1, 15):
            entry = tk.Entry(self.labelframe_loop2, width = 12, state=tk.DISABLED)
            entry.grid(row = i, column = 2)
            self.loop2_entries.append(entry)

        # temp status
        tk.Label(self.labelframe_temp, text = "TEMPA:").grid(row=1, column = 1)
        self.label_tempa = tk.Label(self.labelframe_temp, text = "N/A")
        self.label_tempa.grid(row=1, column=2)
        tk.Label(self.labelframe_temp, text = "TEMPB:").grid(row=2, column = 1)
        self.label_tempb = tk.Label(self.labelframe_temp, text="N/A")
        self.label_tempb.grid(row=2, column=2)

        # User Controls
        self.usercontrols_button_viewpid = tk.Button(self.labelframe_usercontrols, text="VIEW PID TABLE (NOT IMTD)", state=tk.DISABLED)
        self.usercontrols_button_viewpid.grid(row=1, column=1, pady=pad)

        self.usercontrols_button_uploadpid = tk.Button(self.labelframe_usercontrols, text="UPLOAD PID TABLE (NOT IMTD)", state=tk.DISABLED)
        self.usercontrols_button_uploadpid.grid(row=1, column=2, pady=pad)
        
        self.usercontrols_button_start = tk.Button(self.labelframe_usercontrols, text="START LOOPS")
        self.usercontrols_button_start.grid(row=3, column=1, pady = pad)
        
        self.usercontrols_button_stop = tk.Button(self.labelframe_usercontrols, text="STOP LOOPS")
        self.usercontrols_button_stop.grid(row=3, column=2, pady=pad)

        self.usercontrols_button_refresh = tk.Button(self.labelframe_usercontrols, text="REFRESH LOOOPS", command=self.binding_refresh_loopData)
        self.usercontrols_button_refresh.grid(row=4, column=1, pady=pad, padx=12)


        # non gui section
        filename = "cryoreadout_dat_{}.csv".format(time.time())
        self.fileHandle = open(filename, "a")
        self.times = []
        self.tempA = []
        self.tempB = []
        self.resistances = []



    def binding_loop1_changeParams(self):
        self.loop1_button_edit.configure(state=tk.DISABLED)
        for i in self.loop1_entries:
            i.configure(state=tk.NORMAL)
        self.loop1_button_done.configure(state=tk.NORMAL)

    def binding_loop1_saveParams(self):
        vals = []
        self.loop1_button_edit.configure(state=tk.NORMAL)
        for i in self.loop1_entries:
            vals.append(i.get())
            i.configure(state=tk.DISABLED)
        self.loop1_button_done.configure(state=tk.DISABLED)

        # Push them values forward
        cc.setLoopSettings(b'1', vals)

    def binding_loop2_changeParams(self):
        self.loop2_button_edit.configure(state=tk.DISABLED)
        for i in self.loop2_entries:
            i.configure(state=tk.NORMAL)
        self.loop2_button_done.configure(state=tk.NORMAL)

    def binding_loop2_saveParams(self):
        vals = []
        self.loop2_button_edit.configure(state=tk.NORMAL)
        for i in self.loop2_entries:
            vals.append(i.get())
            i.configure(state=tk.DISABLED)
        self.loop2_button_done.configure(state=tk.DISABLED)

        # Push them values forward
        cc.setLoopSettings(b'2', vals)

    def binding_refresh_loopData(self):
        loop1data = cc.getLoopSettings(b'1')
        loop2data = cc.getLoopSettings(b'2')

        if len(loop1data) < 15 or len(loop2data) < 15:
            tk.messagebox.showerror(title="ERROR, SERIAL PORT PROBLEMS", message="ERROR, length of data pulled was less than expected")
            self.destroy()

        # loop1data = [1,2,3,4,5,6,7,8,9,10,11,12,13,14]
        # loop2data = [15,16,17,18,19,20,21,22,23,24,25,26,27,28]
        for i in range(0, 14):
            self.loop1_entries[i].configure(state=tk.NORMAL)
            self.loop1_entries[i].delete(0, tk.END)
            self.loop1_entries[i].insert(0, loop1data[i])
            self.loop1_entries[i].configure(state=tk.DISABLED)

            self.loop2_entries[i].configure(state=tk.NORMAL)
            self.loop2_entries[i].delete(0, tk.END)
            self.loop2_entries[i].insert(0, loop2data[i])
            self.loop2_entries[i].configure(state=tk.DISABLED)


    def poll_and_plot(self):
        """
        The bread and butter of this software is to get the temperature stats and redraw the figures here.
        """
        self.fig_subplotA.clear()
        self.fig_subplotB.clear()

        self.fig_subplotA.set_xlabel("Time (Seconds)")
        self.fig_subplotA.set_ylabel("Temperature (K)")

        self.fig_subplotB.set_xlabel("Temperature (K)")
        self.fig_subplotB.set_ylabel("Resistance (Ohms)")
        
        # Get resistance and add to list
        bytestring = keith.getMeasermentResistance()
        resistance = 0
        try:
            resistance = float(bytestring[29:41])
        except ValueError:
            print("[CRYOREADOUT] Something went wrong when attempting to convert response to values. Perhaps the connection is invalid?")
            print("Try closing the IPython Kernel and swapping the ports.")
            self._timer.stop()
            self.close()
            return

        self.resistances.append(resistance)

        # SAMPLE TEMPERATURES
        tempr = cc.getTemperatures()
        self.tempA.append(tempr[0])
        self.tempB.append(tempr[1])
        currentTime = time.time()
        self.times.append(currentTime)


        # DO PLOT
        self.fig_subplotB.plot(self.tempA, self.resistances)
        self.fig_subplotA.plot(self.times, self.tempA, 'r', self.times, self.tempB, 'b')
        self.fig_subplotB.figure.canvas.draw()
        self.fig_subplotA.figure.canvas.draw()

        # No we need to schedule this again
        self.after(1000, self.poll_and_plot)


if __name__=='__main__':
    app = App()
    app.mainloop()

