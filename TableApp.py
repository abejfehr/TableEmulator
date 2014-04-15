###
# File:    TableApp.py
# Author:  Abe Fehr
# Revised: March 12, 2014
###

import time

###
# Class:       TableApp
# Description: This class must be inherited by all classes that wish
#              to be run on the table as an app.
#
# NOTE: in order to create an app for the table you must call this class's
# ctor in your ctor, as well as override the update and draw methods
###
class TableApp:
	
	###
	# Function: __init__
	# Purpose:  The constructor for the abstract class TableApp
	# Input:    interface  - the interface facade with which we'll be communicating
	#           frameramte - the real number of frames per second you wish to
	#                        call draw/update with the app
	###
	def __init__(self, interface, table, framerate):
		self.interface = interface
		self.table = table
		self.xCoordMax = 10
		self.yCoordMax = 16
		self.elapsed = 0 #not seconds, but frames elapsed
		self.framerate = framerate
		self.initScreen()
		self.initInput()

	###
	# Function: initScreen
	# Purpose:  Populates a list of coordinates with their initial colors
	###
	def initScreen(self):
		self.screen = []
		for x in range(self.xCoordMax):
			self.screen.append([])
			for y in range(self.yCoordMax):
				self.screen[x].append( [255, 255, 255] )
	
	###
	# Function: initInput
	# Purpose:  Populates a list of coordinates with their initial colors
	###
	def initInput(self):
		self.input    = []
		self.oldinput = []
		self.touches  = []
		for x in range(self.xCoordMax):
			self.input.append([])
			self.oldinput.append([])
			self.touches.append([])
			for y in range(self.yCoordMax):
				self.input[x].append(0)
				self.oldinput[x].append(0)
				self.touches[x].append(0)
	
	###
	# Function: clearScreen
	# Purpose:  Changes each pixel of the screen to black
	###
	def clearScreen(self):
		for x in range(self.xCoordMax):
			for y in range(self.yCoordMax):
				self.screen[x][y] = [0,0,0]
	
	###
	# Function: start
	# Purpose:  Starts the game
	###
	def start(self):
		while 1:
			#deal with all the input
			if(self.elapsed != 0):
				self.copy(self.oldinput, self.input)
				self.copy(self.input,self.interface.getInput())
				self.maskTouches()
			
			#update the game and the time elapsed
			self.update()
			self.elapsed+=1
			
			#draw everything to the screen
			self.draw()
			self.interface.draw(self.screen)

			#wait and do it again later
			time.sleep(1./self.framerate)
			
	###
	# Function: anyInput
	# Purpose:  Checks the input to see if there are any
	#			touches(regardless of where)
	# Returns:  True if there is a touch, False if not
	###
	def anyInput(self):
		for x in range(self.xCoordMax):
			for y in range(self.yCoordMax):
				if(self.input[x][y] == 1):
					return True
		return False
		
		
	###
	# Function: maskTouches
	# Purpose:  Compares the input to the oldinput and only keeps new touches
	###
	def maskTouches(self):
		for x in range(self.xCoordMax):
			for y in range(self.yCoordMax):
				if(self.input[x][y] == 1 and self.oldinput[x][y] == 0):
					self.touches[x][y] = 1
				else:
					self.touches[x][y] = 0
					
										
					
	###
	# Function: copy
	# Purpose:  copies contents of list src to list dest
	# NOTE:     assumes that dest is the same size or bigger than src
	###
	def copy(self, dest, src):
		for x in range(len(src)):
			for y in range(len(src[0])):
				dest[x][y] = src[x][y]
				
				
	###
	# Function: list
	# Purpose:  returns a new 2D list of a certain size initialized with zeroes
	# Input:    xMax - the x size of the list to create
	#           yMax - the y size of the list to create
	###
	def list(self, xMax, yMax, initValue):
		matrix = []
		for x in range(xMax):
			matrix.append([])
			for y in range(yMax):
				matrix[x].append(initValue)
		return matrix