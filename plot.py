'''
    author: Cody Roberson
    date: 1/13/2020
    description: This is the main executable for the readout software. Here, we use the keithley and cryocon interfaces to gather our data
    and plot it.
    Based off of an example from https://matplotlib.org/3.1.1/gallery/user_interfaces/embedding_in_qt_sgskip.html
'''

import sys
import time
import os
import numpy as np
import keithley
import cryocon

import matplotlib
matplotlib.use('TKAgg')
####################################### CONFIG ############################################
cryoconPort = ""
keithleyPort = ""
###########################################################################################

from matplotlib.backends.qt_compat import QtCore, QtWidgets, is_pyqt5
if is_pyqt5():
    from matplotlib.backends.backend_qt5agg import (
        FigureCanvas, NavigationToolbar2QT as NavigationToolbar)
else:
    from matplotlib.backends.backend_qt4agg import (
        FigureCanvas, NavigationToolbar2QT as NavigationToolbar)
from matplotlib.figure import Figure


def init_cryocon():
    return cryocon.Cryocon(cryoconPort)


def init_keithley():
    dev_keith = keithley.Keithley2400LV(keithleyPort, True)
    dev_keith.openPort()
    dev_keith.initResistanceMeasurement()
    dev_keith.setSourceCurrent(10.0e-3)
    dev_keith.turnOutput_ON()
    return dev_keith


class ApplicationWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self._main = QtWidgets.QWidget()
        self.setCentralWidget(self._main)
        layout = QtWidgets.QVBoxLayout(self._main)

        # Ask user for filename to save data to
        self.filename = QtWidgets.QFileDialog.getSaveFileName(self, "Save Measurement Data", "", "data csv (*.csv)")
        if self.filename == ("",""):
            self.filename = "cryoreadout_dat_{}.csv".format(time.time())
        print("[CRYOREADOUT] save file set to {}".format(self.filename[0]))
        
        # Open data file
        self.dfHandle = None
        try:
            self.dfHandle = open(self.filename[0], 'w')
        except IOError:
            print("[CRYOREADOUT] ERROR: Can't save to selected file or path")
            exit()
        
        # init devices
        self.cryo = init_cryocon()
        self.keith = init_keithley()

        self.temps = []
        self.resistances = []


        # Create and add canvas + figure to the qt widget
        restemp_canvas = FigureCanvas(Figure(figsize=(5, 3)))
        layout.addWidget(restemp_canvas)
        self.addToolBar(QtCore.Qt.BottomToolBarArea,
                        NavigationToolbar(restemp_canvas, self))


        self._restempPlot = restemp_canvas.figure.subplots()
        self._timer = restemp_canvas.new_timer(
            1000, [(self._update_canvas, (), {})])
        self._timer.start()

    def _update_canvas(self):
        self._restempPlot.clear()
        
        # Get resistance and add to list
        bytestring = self.keith.getMeasermentResistance()
        resistance = float(bytestring[29:41])
        self.resistances.append(resistance)
        
        # Get temperature and add to list
        tempr = self.cryo.getTemperatures()
        self.temps.append(tempr)

        # draw plot
        self._restempPlot.plot(self.temps, self.resistances)
        self._restempPlot.figure.canvas.draw()


if __name__ == "__main__":
    qapp = QtWidgets.QApplication(sys.argv)
    app = ApplicationWindow()
    app.show()
    qapp.exec_()
    