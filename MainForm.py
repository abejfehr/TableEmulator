###
# File:    MainForm.py
# Author:  Abe Fehr
# Revised: March 12, 2014
###

import System.Drawing
import System.Windows.Forms

from System.Drawing import *
from System.Windows.Forms import *

LANDSCAPE = 1
PORTRAIT  = 0

class MainForm(Form):
	###
	# Function: __init__
	# Purpose:  The constructor for this window
	###
	def __init__(self):
		self.xCoordMax = 10
		self.yCoordMax = 16
		self.marginX   = 20
		self.marginY   = 20
		self.orientation = LANDSCAPE
		
		self.InitializeComponent()
	
	###
	# Function: InitializeComponent
	# Purpose:  initializes all the screen components
	###
	def InitializeComponent(self):

		self.InitializePixels()
		self.InitializeInput()
		
		self._button1 = System.Windows.Forms.Button()
		self.SuspendLayout()
		# 
		# button1
		# 
		self._button1.Location = System.Drawing.Point(12, 450)
		self._button1.Name = "button1"
		self._button1.Size = System.Drawing.Size(130, 23)
		self._button1.TabIndex = 0
		self._button1.Text = "Switch Orientation"
		self._button1.UseVisualStyleBackColor = True
		# 
		# MainForm
		# 
		self.ClientSize = System.Drawing.Size(self.xCoordMax*24+2*self.marginX, self.yCoordMax*24+2*self.marginY)
		self.Controls.Add(self._button1)
		
		for x in range(self.xCoordMax):
			for y in range(self.yCoordMax):
				self.Controls.Add(self.pixels[x][y])
		
		self.Name = "MainForm"
		self.Text = "TableEmulator"
		self.ResumeLayout(False)
				
				
				
	###
	# Function: InitializePixels
	# Purpose:  Populates a list of Label elements and initializes them
	###
	def InitializePixels(self):
		self.pixels = []
		for x in range(self.xCoordMax):
			self.pixels.append([])
			for y in range(self.yCoordMax):
				pixel = System.Windows.Forms.Label()
				color = Color.FromArgb(255,255,255)
				pixel.BackColor = color
				pixel.Location = System.Drawing.Point(self.marginX + 24*x, self.marginY + 24*y)
				pixel.Size = System.Drawing.Size(24, 24)
				pixel.MinimumSize = System.Drawing.Size(x, y)
				pixel.MouseDown += self.MouseDown
				pixel.MouseUp   += self.MouseUp
				self.pixels[x].append(pixel)



	###
	# Function: InitializeInput
	# Purpose:  Populates a 2D list of zeroes for the input
	###
	def InitializeInput(self):
		self.input = []
		for x in range(self.xCoordMax):
			self.input.append([])
			for y in range(self.yCoordMax):
				self.input[x].append(0)



	###
	# Function: ClearInput
	# Purpose:  Sets everything in the input array to zero
	###
	def ClearInput(self):
		for x in range(self.xCoordMax):
			for y in range(self.yCoordMax):
				self.input[x][y] = 0


	###
	# Function: Update
	# Purpose:  Updates the pixels to show the correct color
	###
	def Update(self, screen):
		for x in range(self.xCoordMax):
			for y in range(self.yCoordMax):
				color = Color.FromArgb(screen[x][y][0],screen[x][y][1],screen[x][y][2])
				self.pixels[x][y].BackColor = color


	###
	# Function: GetInput
	# Purpose:  Returns an array containing input
	# Returns:  A 2D array containing the touches
	###
	def GetInput(self):
		return self.input
	
	
	###
	# Function: MouseDown
	# Purpose:  The event handler for a pixel click
	###
	def MouseDown(self, sender, e):
		self.ClearInput()
		x = sender.MinimumSize.Width
		y = sender.MinimumSize.Height
		print "Touch @x:%g, y:%g" % (x, y)
		self.input[x][y] = 1
		
	###
	# Function: MouseUp
	# Purpose:  The event handler that clears the pixel grid
	###
	def MouseUp(self, sender, e):
		self.ClearInput()