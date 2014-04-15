from TableApps import *

class Table:
	def __init__(self, interface):
		self.interface = interface
		self.currentApp = Menu(self.interface, self)
		
	###
	# Function: start
	# Purpose:  starts the table up and shows an app
	###
	def start(self):
		self.currentApp.start()
		
	###
	# Function: quit
	# Purpose:  quits the current app and loads the menu
	###
	def quit(self):
		self.currentApp = Menu(self.interface, self)
		self.start()

	###
	# Function: open
	# Purpose:  opens a given app, replacing the menu
	# Input:    app - the app to start
	###
	def open(self, app):
		self.currentApp = app(self.interface, self)
		self.start()