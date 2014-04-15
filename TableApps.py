###
# File:    TableApps.py
# Author:  Abe Fehr
# Revised: March 12, 2014
###

import sys
#obviously won't work under linux, it will have to be removed
sys.path.append(r'c:\python27\Lib')

import random

from TableApp import TableApp

###
# Module:      TableApps
# Description: This module will contain several apps that can be run on the table.
#          The apps that it contains so far are:
#			* ColorTest     - test of the rgb values changing with time
#			* FallingBlocks - precursor to tetris
#			* Tetris        - will-be tetris game
#			* TouchTest		- first input test, screen changes color on touch 
#			* GameOfLife	- Conway's Game of Life for the table
#			* ScreenSaver	- Beautiful animation intended to be a screensaver
###


###
# App:     FallingBlocks
# Purpose: This game is a simulation of blocks
#          falling from the top of the screen
###
class FallingBlocks(TableApp):	
	
	class Block:
		def __init__(self):
			self.xCoordMax = 10
			self.yCoordMax = 16
			self.x = random.randint(0,self.xCoordMax-1)
			self.y = 0
			
		def move(self):
			self.y += 1


	def __init__(self, interface, table):
		TableApp.__init__(self, interface, table, 15)
		self.blocks = []


	def update(self):
		for block in self.blocks:
			if(block.y < self.yCoordMax and self.elapsed % 3 == 0):
				block.move()
		if(self.elapsed % 15 == 0):
			self.blocks.append(self.Block())
		if(self.touches[self.xCoordMax-1][0] == 1):
			self.table.quit()


	def draw(self):
		self.clearScreen()
		for block in self.blocks:
			if(block.y < self.yCoordMax):
				self.screen[block.x][block.y] = [255,255,255]

###
# App:     ColorTest
# Purpose: A test that showscases the blending of colors
#          and tests their change over a period of time.
###
class ColorTest(TableApp):
	###
	# Function: __init__
	# Purpose:  The main constructor for the game
	# Input:    interface - the interface object which handles drawing the
	#			view and receiving the input
	###
	def __init__(self, interface, table):
		TableApp.__init__(self, interface, table, 30)

	def draw(self):
		for x in range(self.xCoordMax):
			for y in range(self.yCoordMax):
					self.screen[x][y] = [(self.elapsed%255)*x/self.xCoordMax, 255*x/self.xCoordMax, 255*y/self.yCoordMax]
		
	def update(self):
		if(self.anyInput()):
			self.table.quit()
	
	
###
# App:     TouchTest
# Purpose: A test app where each touch changes the color
###
class TouchTest(TableApp):
	###
	# Function: __init__
	# Purpose:  The main constructor for the game
	# Input:    interface - the interface object which handles drawing the
	#			view and receiving the input
	###
	def __init__(self, interface, table):
		TableApp.__init__(self, interface, table, 15)
		self.randomizeColor()

	###
	# Function: draw
	# Purpose:  Draws the color to the table
	###
	def draw(self):
		for x in range(self.xCoordMax):
			for y in range(self.yCoordMax):
					self.screen[x][y] = self.color


	###
	# Function: update
	# Purpose:  Changes the color if there's any input
	###		
	def update(self):
		if(self.touches[self.xCoordMax-1][0] == 1):
			self.table.quit()
		if(self.anyInput()):
			self.randomizeColor()


	###
	# Function: randomizeColor
	# Purpose:  stores a brand new random color to be used
	###
	def randomizeColor(self):
		self.color = [random.randint(0,255), random.randint(0,255), random.randint(0,255)]

	
###
# App:     Ripples
# Purpose: A test app for ripples
###
class Ripples(TableApp):
	###
	# Function: __init__
	# Purpose:  The main constructor for the game
	# Input:    interface - the interface object which handles drawing the
	#			view and receiving the input
	###
	def __init__(self, interface, table):
		TableApp.__init__(self, interface, table, 15)
		self.initializeWorld()
		
	def initializeWorld(self):
		self.buffer1 = []
		self.buffer2 = []
		for x in range(self.xCoordMax):
			self.buffer1.append([])
			self.buffer2.append([])
			for y in range(self.yCoordMax):
				self.buffer1[x].append(0)
				self.buffer2[x].append(0)
		
	###
	# Function: draw
	# Purpose:  Draws the color to the table
	###
	def draw(self):
		for x in range(self.xCoordMax):
			for y in range(self.yCoordMax):
				if(self.elapsed % 2 == 0):
					self.drawColor(self.buffer1, x, y)
				else:
					self.drawColor(self.buffer2, x, y)
					
	def drawColor(self, buffer, x, y):
		value = 127 + buffer[x][y] >> 4;

		#clamp the value
		if(value > 255 ):
			value = 255
		elif(value < 0):
			value = 0

		self.screen[x][y] = [value, value, value]    
    
    
	###
	# Function: update
	# Purpose:  Changes the color if there's any input
	###		
	def update(self):
		if(self.touches[self.xCoordMax-1][0] == 1):
			self.table.quit()
		for x in range(self.xCoordMax):
			for y in range(self.yCoordMax):
				if(self.touches[x][y]):
					if(self.elapsed % 2 == 0):
						self.buffer1[x][y] = 2048
					else:
						self.buffer2[x][y] = 2048
		if(self.elapsed % 2 == 0):
			self.processWater(self.buffer1, self.buffer2)
		else:
			self.processWater(self.buffer2, self.buffer1)
						
	def processWater(self, source, dest):
		for x in range(0, self.xCoordMax):
			for y in range(0, self.yCoordMax):
				sum = 0
				if(x != self.xCoordMax-1):
					sum += source[x+1][y]
				if(x != 1):
					sum += source[x-1][y]
				if(y != self.yCoordMax-1):
					sum += source[x][y+1]
				if(y != 1):
					sum += source[x][y-1]
				dest[x][y] = (sum  >> 1) - dest[x][y]
				dest[x][y] -= (dest[x][y] >> 3)


###
# App:     GameOfLife
# Purpose: A version of John Conway's Game of Life for the table
###
class GameOfLife(TableApp):
	###
	# Function: __init__
	# Purpose:  The main constructor for the game
	# Input:    interface - the interface object which handles drawing the
	#			view and receiving the input
	###
	def __init__(self, interface, table):
		TableApp.__init__(self, interface, table, 15)
		self.initializeWorld()
		self.editMode = True #if it's not editMode, it's playMode

	###
	# Function: initializeWorld
	# Purpose:  Populates a 2D list of zeroes for the game
	###
	def initializeWorld(self):
		self.world  = []
		self.future = []
		for x in range(self.xCoordMax):
			self.world.append([])
			self.future.append([])
			for y in range(self.yCoordMax-1):
				self.world[x].append(0)
				self.future[x].append(0)


	###
	# Function: draw
	# Purpose:  Draws the world to the table
	###
	def draw(self):
		#this line optional in case you don't want a transition
		for x in range(self.xCoordMax):
			for y in range(self.yCoordMax-1):
				if(self.world[x][y] == 1):
					self.screen[x][y] = [255,255,255]
				else:
					self.screen[x][y] = [0, 0, 0]
			if(x < 5):
				self.screen[x][self.yCoordMax-1] = [255,0,0]
			else:
				self.screen[x][self.yCoordMax-1] = [0,255,0]
		
	###
	# Function: update
	# Purpose:  Either steps the world each frame or checks for input
	#           and allows the user to modify the world
	###
	def update(self):
		if(self.touches[self.xCoordMax-1][0] == 1):
			self.table.quit()
		self.listen()
		if(self.editMode):
			self.editWorld()
		else:
			self.copy(self.future, self.world)
			self.stepWorld()
			self.copy(self.world, self.future)
			
	###
	# Function: listen
	# Purpose:  Listens for button presses and delegates tasks
	###
	def listen(self):
		for x in range(self.xCoordMax):
			if(self.touches[x][self.yCoordMax-1] == 1):
				if(x < 5):
					self.stopPressed()
				else:
					self.startPressed()
	
	
	###
	# Function: stepWorld
	# Purpose:  Tells each square in the world to step(execute game logic)
	###
	def stepWorld(self):
		for x in range(self.xCoordMax):
			for y in range(self.yCoordMax-1):
				self.step(x,y)
	
	
	###
	# Function: editWorld
	# Purpose:  Listens for user input and lets user edit the world
	###
	def editWorld(self):
		for x in range(self.xCoordMax):
			for y in range(self.yCoordMax-1):
				if(self.touches[x][y] == 1):
					self.toggle(x,y)


	###
	# Function: step
	# Purpose:  The game logic for each square
	###
	def step(self, x, y):
		numNeighbours = self.getNumNeighbours(x, y)
		if(self.world[x][y] == 1):
			if(numNeighbours < 2):
				self.die(x,y)
			elif(numNeighbours > 3):
				self.die(x,y)
		else:
			if(numNeighbours == 3):
				self.live(x,y)
		
		
		
	###
	# Function: getNumNeighbours
	# Purpose:  Gets the number of surrounding neighbours that are alive
	# Input:    x - the x coordinate of the square to check
	#			y - the y coordinate of the square to check
	# Returns:  the number of immediately surrounding neighbours that are alive
	###
	def getNumNeighbours(self, x, y):
		num = 0
		if(x != 0):
			if(self.world[x-1][y] == 1):
				num+=1
		if(x != self.xCoordMax-1):
			if(self.world[x+1][y] == 1):
				num+=1
		if(y != 0):
			if(self.world[x][y-1] == 1):
				num += 1
		if(y != self.yCoordMax-2):
			if(self.world[x][y+1] == 1):
				num += 1
				
		if(x != 0 and y != 0):
			if(self.world[x-1][y-1] == 1):
				num+=1
		if(x != self.xCoordMax-1 and y != 0):
			if(self.world[x+1][y-1] == 1):
				num+=1
		if(x != self.xCoordMax-1 and y != self.yCoordMax-2):
			if(self.world[x+1][y+1] == 1):
				num += 1
		if(x != 0 and y != self.yCoordMax-2):
			if(self.world[x-1][y+1] == 1):
				num += 1
			
		return num

	def toggle(self, x, y):
		if(self.world[x][y] == 1):
			self.world[x][y] = 0
		else:
			self.world[x][y] = 1
			
			
	###
	# Function: stopPressed
	# Purpose:  Receiver function for the stop button
	###
	def stopPressed(self):
		self.editMode = True
		
	
	###
	# Function: startPressed
	# Purpose:  Receiver function for the start button
	###
	def startPressed(self):
		self.editMode = False
		

	###
	# Function: die
	# Purpose:  Sets a square to die for the next turn
	###
	def die(self, x, y):
		self.future[x][y] = 0
	
	
	###
	# Function: live
	# Purpose:  Sets a square to be born for the next turn
	###
	def live(self, x, y):
		self.future[x][y] = 1


###
# App:     Screensaver
# Purpose: A potential ScreenSaver for the table or possibly a menu feature
###
class ScreenSaver(TableApp):
	
	###
	# Function: __init__
	# Purpose:  The main constructor for the screensaver
	# Input:    interface - the interface object which handles drawing the
	#			view and receiving the input
	###
	def __init__(self, interface, table):
		TableApp.__init__(self, interface, table, 30)
		self.blips = []
		#how much the brightness of each blip goes down each frame
		self.fadeSpeed   = 7 
		#how many frames before each new blip
		self.newBlipRate = 6 

	def draw(self):
		self.clearScreen()
		self.drawBlips()
		
	def update(self):
		if(self.anyInput()):
			self.table.quit()
		if(self.elapsed % self.newBlipRate == 0):
			self.createBlip()
		self.updateBlips()
		self.clearDeadBlips()
		
	def drawBlips(self):
		#go through each of the blips
		for blip in self.blips:
			self.screen[blip[0]][blip[1]] = [blip[2],blip[2],blip[2]]
			
	def createBlip(self):
		self.blips.append( [ random.randint(0, self.xCoordMax-1), random.randint(0,self.yCoordMax-1), 200 ] )
	
	def updateBlips(self):
		for blip in self.blips:
			blip[2] -= self.fadeSpeed
				
	def clearDeadBlips(self):
		liveOnes = []
		for blip in self.blips:
			if(blip[2] > self.fadeSpeed):
				liveOnes.append(blip)
		self.blips = liveOnes
###
# App:     Tetris
# Purpose: Tetris for the table
###
class Tetris(TableApp):	
	
	def __init__(self, interface, table):
		TableApp.__init__(self, interface, table, 5)
		self.blockFalling = False
		self.initTetrominoes()
		self.initWorld()

	def initWorld(self):
		self.static  = []
		self.dynamic = []
		for x in range(self.xCoordMax):
			self.static.append([])
			self.dynamic.append([])
			for y in range(self.yCoordMax-1):
				self.static[x].append(0)
				self.dynamic[x].append(0)

	def initTetrominoes(self):

		self.colors = [ [0,0,0], [255,255,0], [128,128,255], [255,0,0],\
                        [0,255,0], [255,128,128], [0,0,255], [255,0,255] ]
		
		self.O = [[[0,0,0,0], [0,0,0,0], [0,0,0,0], [0,0,0,0]],\
       			  [[0,1,1,0], [0,1,1,0], [0,1,1,0], [0,1,1,0]],\
          		  [[0,1,1,0], [0,1,1,0], [0,1,1,0], [0,1,1,0]],\
          		  [[0,0,0,0], [0,0,0,0], [0,0,0,0], [0,0,0,0]]]

		self.I = [[[0,0,0,0], [0,0,2,0], [0,0,0,0], [0,2,0,0]],\
       			  [[2,2,2,2], [0,0,2,0], [0,0,0,0], [0,2,0,0]],\
          		  [[0,0,0,0], [0,0,2,0], [2,2,2,2], [0,2,0,0]],\
          		  [[0,0,0,0], [0,0,2,0], [0,0,0,0], [0,2,0,0]]]

		self.S = [[[0,0,0,0], [0,0,3,0], [0,0,0,0], [0,0,3,0]],\
       			  [[0,0,3,3], [0,0,3,3], [0,0,3,3], [0,0,3,3]],\
          		  [[0,3,3,0], [0,0,0,3], [0,3,3,0], [0,0,0,3]],\
          		  [[0,0,0,0], [0,0,0,0], [0,0,0,0], [0,0,0,0]]]
          		  
		self.Z = [[[0,0,0,0], [0,0,0,4], [0,0,0,0], [0,0,0,4]],\
				  [[0,4,4,0], [0,0,4,4], [0,4,4,0], [0,0,4,4]],\
				  [[0,0,4,4], [0,0,4,0], [0,0,4,4], [0,0,4,0]],\
				  [[0,0,0,0], [0,0,0,0], [0,0,0,0], [0,0,0,0]]]

		self.L = [[[0,0,0,0], [0,0,5,0], [0,0,0,5], [0,5,5,0]],\
				  [[0,5,5,5], [0,0,5,0], [0,5,5,5], [0,0,5,0]],\
        		  [[0,5,0,0], [0,0,5,5], [0,0,0,0], [0,0,5,0]],\
        		  [[0,0,0,0], [0,0,0,0], [0,0,0,0], [0,0,0,0]]]

		self.J = [[[0,0,0,0], [0,0,6,6], [0,6,0,0], [0,0,6,0]],\
				  [[0,6,6,6], [0,0,6,0], [0,6,6,6], [0,0,6,0]],\
				  [[0,0,0,6], [0,0,6,0], [0,0,0,0], [0,6,6,0]],\
				  [[0,0,0,0], [0,0,0,0], [0,0,0,0], [0,0,0,0]]]

		self.T = [[[0,0,0,0], [0,0,7,0], [0,0,7,0], [0,0,7,0]],\
				  [[0,7,7,7], [0,0,7,7], [0,7,7,7], [0,7,7,0]],\
				  [[0,0,7,0], [0,0,7,0], [0,0,0,0], [0,0,7,0]],\
				  [[0,0,0,0], [0,0,0,0], [0,0,0,0], [0,0,0,0]]]

	def update(self):
		if(self.touches[self.xCoordMax-1][0] == 1):
			self.table.quit()
		if(self.elapsed % 5 == 0):
			if(not self.blockFalling):
				self.dropBlock()
			else:
				self.moveDynamicBlocks()
	
	def dropBlock(self):
		for x in range(0,4):
			for y in range(0,4):
				z = random.randint(1, 7)
				if(z == 1):
					self.dropO()
				elif(z == 2):
					self.dropI()
				elif(z == 3):
					self.dropS()
				elif(z == 4):
					self.dropZ()
				elif(z == 5):
					self.dropL()
				elif(z == 6):
					self.dropJ()
				else:
					self.dropT()
###move this code into dropT
#self.dynamic[x][y] = self.T[0][x][y]
#		self.blockFalling = True
	
	def moveDynamicBlocks(self):
		tempDyn = self.list(self.xCoordMax, self.yCoordMax-1, 0)
		for x in range(self.xCoordMax):
			for y in range(self.yCoordMax-2):
				if(not self.isCollision()):
					tempDyn[x][y+1] = self.dynamic[x][y]
					#change the location of the block stored in memory somehow
				else:
					self.blockFalling = False
					#move the dynamic array's contents into the static
					self.mergeDynStat()
		self.dynamic = tempDyn
	
	def mergeDynStat(self):
		for x in range(self.xCoordMax):
			for y in range(self.yCoordMax-1):
				if(not self.isDynamicEmpty(x, y)):
					self.static[x][y] = self.dynamic[x][y]
					self.dynamic[x][y] = 0
	
	def isCollision(self):
		for x in range(self.xCoordMax):
			for y in range(self.yCoordMax-1):
				if(not self.isDynamicEmpty(x, y)):
					if(y == self.yCoordMax-2):
						return True
					elif(not self.isStaticEmpty(x, y+1)):
						return True
	
	def isDynamicEmpty(self, x, y):
		return (self.dynamic[x][y] == 0)

	def isStaticEmpty(self, x, y):
		return (self.static[x][y] == 0)
	
	def draw(self):
		self.clearScreen()
		self.drawButtons()
		self.drawWorld()
		
	def drawWorld(self):
		for x in range(self.xCoordMax):
			for y in range(self.yCoordMax-1):
				if(not self.isDynamicEmpty(x, y)):
					self.screen[x][y] = self.colors[self.dynamic[x][y]]
				else:
					self.screen[x][y] = self.colors[self.static[x][y]]
		
	def drawButtons(self):
		self.screen[0][self.yCoordMax-1] = [75,75,75]
		self.screen[1][self.yCoordMax-1] = [75,75,75]
		self.screen[2][self.yCoordMax-1] = [255,0,0]
		self.screen[3][self.yCoordMax-1] = [255,0,0]
		self.screen[4][self.yCoordMax-1] = [255,0,0]
		self.screen[5][self.yCoordMax-1] = [255,0,0]
		self.screen[6][self.yCoordMax-1] = [255,0,0]
		self.screen[7][self.yCoordMax-1] = [255,0,0]
		self.screen[8][self.yCoordMax-1] = [75,75,75]
		self.screen[9][self.yCoordMax-1] = [75,75,75]
				

###
# App:     Menu
# Purpose: The main menu of the table.
###
class Menu(TableApp):
	###
	# Function: __init__
	# Purpose:  The main constructor for the menu
	# Input:    interface - the interface object which handles drawing the
	#			view and receiving the input
	#           table - the controller object representing the table
	###
	def __init__(self, interface, table):
		self.framerate = 30
		TableApp.__init__(self, interface, table, self.framerate)
		self.framesopen = 0
		self.showConfirm = False
		self.selectedApp = -1

	def draw(self):
		self.clearScreen()
		self.screen[0][self.yCoordMax-1] = [255, 0, 0]
		self.screen[0][self.yCoordMax-2] = [255, 0, 0]
		self.screen[0][self.yCoordMax-3] = [255, 128, 0]
		self.screen[0][self.yCoordMax-4] = [255, 128, 0]
		self.screen[0][self.yCoordMax-5] = [255, 255, 0]
		self.screen[0][self.yCoordMax-6] = [255, 255, 0]
		self.screen[0][self.yCoordMax-7] = [0, 255, 0]
		self.screen[0][self.yCoordMax-8] = [0, 255, 0]
		self.screen[0][self.yCoordMax-9] = [0, 128, 255]
		self.screen[0][self.yCoordMax-10] = [0, 128, 255]
		self.screen[0][self.yCoordMax-11] = [0, 0, 255]
		self.screen[0][self.yCoordMax-12] = [0, 0, 255]
		self.screen[0][self.yCoordMax-13] = [128, 0, 255]
		self.screen[0][self.yCoordMax-14] = [128, 0, 255]
		self.screen[0][self.yCoordMax-15] = [255, 0, 255]
		self.screen[0][self.yCoordMax-16] = [255, 0, 255]
		
	def update(self):
		if(self.framesopen >= 30 * self.framerate): #30 seconds
			self.table.open(ScreenSaver)
		
		if(self.anyInput()):
			self.framesopen = 0
		
		if(self.appSelected() == 0):
			if(self.selectedApp == 0):
				self.table.open(ColorTest)
		elif(self.appSelected() == 1):
			if(self.selectedApp == 1):
				self.table.open(TouchTest)
		elif(self.appSelected() == 2):
			if(self.selectedApp == 3):
				self.table.open(FallingBlocks)
		elif(self.appSelected() == 3):
			if(self.selectedApp == 3):
				self.table.open(GameOfLife)
		elif(self.appSelected() == 4):
			if(self.selectedApp == 4):
				self.table.open(Ripples)
		elif(self.appSelected() == 5):
			if(self.selectedApp == 5):
				pass
		elif(self.appSelected() == 6):
			pass
		elif(self.appSelected() == 7):
			pass
		
		if(self.appSelected() != -1):
			self.selectedApp = self.appSelected()
		self.framesopen += 1;
		
	def appSelected(self):
		if(self.touches[0][self.yCoordMax-1] or self.touches[0][self.yCoordMax-2]):
			return 0
		elif(self.touches[0][self.yCoordMax-3] or self.touches[0][self.yCoordMax-4]):
			return 1
		elif(self.touches[0][self.yCoordMax-5] or self.touches[0][self.yCoordMax-6]):
			return 2
		elif(self.touches[0][self.yCoordMax-7] or self.touches[0][self.yCoordMax-8]):
			return 3
		elif(self.touches[0][self.yCoordMax-9] or self.touches[0][self.yCoordMax-10]):
			return 4
		elif(self.touches[0][self.yCoordMax-11] or self.touches[0][self.yCoordMax-12]):
			return 5
		elif(self.touches[0][self.yCoordMax-13] or self.touches[0][self.yCoordMax-14]):
			return 6
		elif(self.touches[0][self.yCoordMax-15] or self.touches[0][self.yCoordMax-16]):
			return 7
		else:
			return -1