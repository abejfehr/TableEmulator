###
# File:    Table.py
# Author:  Abe Fehr
# Revised: March 12, 2014
###

###
# Class:       Table
# Description: The facade class which will be communicating with
#      	       the table simulator
###
class Interface:
	###
	# Function: __init__
	# Purpose:  The actual constructor for the table facade class
	###
	def __init__(self, form):
		self.emulator = form	

	###
	# Function: draw
	# Purpose:  Draws the current screen to the emulator
	###
	def draw(self, screen):
		self.emulator.Update(screen)


	###
	# Function: getInput
	# Purpose:  Gets a 2D array containing the input locations
	###
	def getInput(self):
		return self.emulator.GetInput()