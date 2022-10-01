#!/usr/bin/env python
#
# Author : Digvijay Patankar dbpatankar@gmail.com
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#

import xarray as xa
import numpy as np
import pandas as pd

import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
from matplotlib import style
style.use("ggplot")

from tkinter import filedialog
from tkinter import *
from tkinter.ttk import *


def readASCII(filename, separator):
    return pd.read_csv(filename, sep=separator)

def readNC(filename):
    return xa.open_dataset(filename)


class App:

    def __init__(self, master):
        """
        Draw root window and components
        """
        ## Define frames
        self.topleft_frame = Frame(master, relief=SUNKEN, height=300)
        self.topright_frame = Frame(master, relief=SUNKEN, height=300)
        self.middle_frame = Frame(master, relief=GROOVE)
        self.canvas_frame = Frame(master)
        self.toolbar_frame = Frame(master)

        self.topleft_frame.grid(row=0, column=0)
        self.topright_frame.grid(row=0, column=1)
        self.middle_frame.grid(row=2, columnspan=2)
        self.canvas_frame.grid(row=4, columnspan=2)
        self.toolbar_frame.grid(row=5, columnspan=2, sticky=W)
        
        ## Top left frame 
        self.ascii_filename = StringVar()
        self.ascii_label = Label(self.topleft_frame, text="Select ASCII file ")
        self.ascii_entry = Entry(self.topleft_frame, textvariable=self.ascii_filename)
        self.ascii_btn = Button(self.topleft_frame, text="Open", command=self.openAsciiFile)

        self.ascii_label.grid(row=0, column=0, ipady=4)
        self.ascii_entry.grid(row=0, column=1, columnspan=2, sticky=E+W, ipady=4)
        self.ascii_btn.grid(row=0, column=3, sticky=W, ipady=4)

        self.ascii_year_col = StringVar()
        self.ascii_year_col_label = Label(self.topleft_frame, text="Select year column")
        self.ascii_year_col_combo = Combobox(self.topleft_frame, textvariable=self.ascii_year_col)
        self.ascii_month = StringVar()
        self.ascii_month_label = Label(self.topleft_frame, text="Select month")
        self.ascii_month_combo = Combobox(self.topleft_frame, textvariable=self.ascii_month, values=[" "])
        
        self.ascii_year_col_label.grid(row=1, column=0, ipady=4)
        self.ascii_year_col_combo.grid(row=1, column=1, ipady=4)
        self.ascii_month_label.grid(row=1, column=2, ipady=4)
        self.ascii_month_combo.grid(row=1, column=3, ipady=4)

        ## Top right frame
        self.nc_filename = StringVar()
        self.nc_label = Label(self.topright_frame, text="Select netCDF file ")
        self.nc_entry = Entry(self.topright_frame, textvariable=self.nc_filename)
        self.nc_btn = Button(self.topright_frame, text="Open", command=self.openNcFile)

        self.nc_label.grid(row=0, column=0, ipady=4)
        self.nc_entry.grid(row=0, column=1, columnspan=2, sticky=E+W, ipady=4)
        self.nc_btn.grid(row=0, column=3, sticky=W, ipady=4)


        self.nc_var = StringVar()
        self.nc_var_label = Label(self.topright_frame, text="Select variable")
        self.nc_var_combo = Combobox(self.topright_frame, textvariable=self.nc_var)

        self.nc_var_label.grid(row=1, column=0, ipady=4)
        self.nc_var_combo.grid(row=1, column=1, ipady=4)

        self.nc_season = StringVar()
        self.nc_season_label = Label(self.topright_frame, text="Select season")
        self.nc_season_combo = Combobox(self.topright_frame, textvariable=self.nc_season, values=["DJF", "MAM", "JJA", "SAN"])
        self.nc_season_combo.current(0)

        self.nc_season_label.grid(row=1, column=2, ipady=4)
        self.nc_season_combo.grid(row=1, column=3, ipady=4)

        Separator(master, orient=HORIZONTAL).grid(row=1, columnspan=2, sticky="ew")

        ## Middle frame
        self.year_from = StringVar()
        self.year_from_label = Label(self.middle_frame, text = "Year from")
        self.year_from_combo = Combobox(self.middle_frame, textvariable=self.year_from)
        self.year_to = StringVar()
        self.year_to_label = Label(self.middle_frame, text="To")
        self.year_to_combo = Combobox(self.middle_frame, textvariable=self.year_to)

        self.year_from_label.grid(row=0, column=0, ipady=4)
        self.year_from_combo.grid(row=0, column=1, ipady=4)
        self.year_to_label.grid(row=0, column=2, ipady=4)
        self.year_to_combo.grid(row=0, column=3, ipady=4)
        
        self.plot_btn = Button(self.middle_frame, text="Plot")
        self.plot_btn.bind("<Button-1>", func=self.plotData)
        self.plot_btn.grid(row=0, column=4, ipady=4)

        Separator(master, orient=HORIZONTAL).grid(row=3, columnspan=2, sticky="ew")
        
        ## Canvas + toolbar frame
        self.f = Figure(figsize=(12, 6))
        self.a = self.f.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.f, self.canvas_frame)
        self.toolbar = NavigationToolbar2Tk(self.canvas, self.toolbar_frame)
        self.canvas.get_tk_widget().grid(row=0, column=0)
        self.f.tight_layout()
    
    def openAsciiFile(self):
        fname = filedialog.askopenfilename()
        self.ascii_filename.set(fname)
        self.df = readASCII(fname, "\t")
        self.ascii_month_combo.config(values=self.df.columns.tolist())
        self.ascii_month_combo.current(1)
        self.ascii_year_col_combo.config(values=self.df.columns.tolist())
        self.ascii_year_col_combo.current(0)
        self.setYears()

    def openNcFile(self):
        fname = filedialog.askopenfilename()
        self.nc_filename.set(fname)
        self.nc = readNC(fname)
        variables = [i for i in self.nc.data_vars.variables.mapping.keys()]
        self.nc_var_combo.config(values=variables)
        self.nc_var_combo.current(1)

    def setYears(self):
        year_col = self.ascii_year_col_combo.get()
        self.year_from_combo.config(values=self.df[year_col].tolist())
        self.year_from_combo.current(0)
        self.year_to_combo.config(values=self.df[year_col].tolist()[::-1])
        self.year_to_combo.current(0)

    def plotData(self, event):
        ds = self.df
        nc = self.nc
        lats = nc.lat.data.tolist()
        lons = nc.lon.data.tolist()
        year_start = int(self.year_from_combo.get())
        year_end = int(self.year_to_combo.get())
        ascii_month = self.ascii_month_combo.get()
        nc_var = self.nc_var_combo.get() # Variable to find correlation with

        season_cond = (nc.time.dt.season==self.nc_season_combo.get())
        year_cond = (nc.time.dt.year >= year_start) & (nc.time.dt.year <=year_end)
        year = self.ascii_year_col_combo.get()

        nc = nc.where(year_cond & season_cond, drop=True)
        ds = ds[(ds[year] >= year_start) & (ds[year] <= year_end)]
        
        n = nc.groupby('time.year').mean(dim='time')
        
        # Correlation coefficient values cc
        cc = np.zeros([len(lats), len(lons)])
        for i in range(len(lats)) :
            for j in range(len(lons)) :
                cc[i, j] = np.corrcoef(ds[ascii_month], n.variables[nc_var][:, i, j])[0, 1]
        
        cca = xa.DataArray(data=cc, coords=(lats, lons), dims=['lat', 'lon'])
        
        n['cca'] = cca
        
        self.toolbar.update()
        if hasattr(self, 'c'):
            self.c.remove()
        else:
            pass
        self.ax = self.a.pcolormesh(n.lon, n.lat, n.cca)
        self.c = self.f.colorbar(self.ax)
        self.canvas.draw()
        
root = Tk(className=" Correlation between rainfall and SST")
if __name__ == "__main__":
    app = App(root)


root.mainloop()

