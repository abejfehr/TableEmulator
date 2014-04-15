###
# File:    Program.py
# Author:  Abe Fehr
# Revised: March 12, 2014
###

import clr
clr.AddReference('System.Windows.Forms')
clr.AddReference('System.Drawing')

import thread

from System.Windows.Forms import Application
import MainForm
from Interface import Interface #the facade class
from Table import Table

Application.EnableVisualStyles()

form  = MainForm.MainForm()
interface = Interface(form)
table = Table(interface)

def RunEmulator():
	Application.Run(form)

def RunApplication():
	global table
	table.start()

thread.start_new_thread(RunEmulator, ())
thread.start_new_thread(RunApplication, ())

while 1:
	pass