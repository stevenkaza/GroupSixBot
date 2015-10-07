import math #Used for drawing the facing direction line

import tkFileDialog
import tkMessageBox
from Tkinter import *

from PIL import Image, ImageTk

#from SocketHelper import * #Uncomment
import threading
import time
import thread
import os
#from socket import * #Uncomment
import sys
#from Map import * #Uncomment
import Queue
from ProcessRoom import *

windowWidth = 675
windowHeight = 550

canvasWidth = 450.0
canvasHeight = 450.0

mapWidth = 500.0
mapHeight = 500.0

mapOffset = 25

currentData = [[]]

"""
Debug Code
"""

#Grabs data from file and returns it in a 2D array
def readTestFile(fileName):
	with open(fileName, "r") as file:
		info = file.read().replace('\n', '')

	data = [[]]
	row = 0

	for char in info:
		if char == "]":
			row += 1
			data.append([])
		elif char != "[" and char != "," and char != " ":
			data[row].append(int(char))
	return data

"""
End Debug Code
"""

#Position is (x,y), returns new position as (x,y) in canvas space
def worldSpaceToCanvasSpace(position):
	newPosition = ((position[0] / mapWidth) * canvasWidth + mapOffset, (position[1] / mapHeight) * canvasHeight + mapOffset)
	return newPosition

def exitRoomMapper():
	if tkMessageBox.askyesno('Quitting . . .', 'Are you sure you want to quit?'):
		gui.quit()

		
def saveMapComparison(self):
	print "Saved map to rooms" 
	filename = "./rooms/testRoom" #Find next room number, no .txt it seems
	pr = ProcessRoom()
	pr.saveFile(filename, currentData)
		
def saveMap(self):
	self.canvas.postscript(file = "map.ps", colormode = 'color')
	
def saveTextLog(self):
	filename = tkFileDialog.asksaveasfilename(defaultextension='.txt',filetypes = (('Text files', '*.txt'),('Python files', '*.py *.pyw'),('All files', '*.*')))
	if filename is None:
		return
	file = open (filename, mode = 'w')
	file.write(self.textBox.get(1.0, END))
	file.close()

def aboutRoomMapper():
	tkMessageBox.showinfo("About Room Mapper", "Room Mapper Beta V 1.0 \n\nTeam: \nKory Bryson - Communications Lead, \nMitchell Cook - AI Lead, \nSteven Kazavchinski - Movement and Sensor Lead, \nZack Licastro - UI Co-Lead, \nAmanda Reuillon - UI Co-Lead \n\n A tool to visualize room mapper from a Pi Bot room mapper.")
	
#Set Up Menu
def mainMenu(r):
	m = Menu(r)

	global fileMenu
	global helpMenu

	#File
	fileMenu = Menu(m, tearoff=0)
	#fileMenu.add("command", label="Save Map", command = saveMap, state = DISABLED)
	#fileMenu.add("command", label="Save As", command = saveFileAs, state = DISABLED)
	
	fileMenu.add("command", label="Save Map for Comparison", command = lambda: saveMapComparison(r))
	fileMenu.add("command", label="Save Map to PostScript", command = lambda: saveMap(r))
	fileMenu.add("command", label="Save Text Log", command = lambda: saveTextLog(r))
	fileMenu.add("command", label="Exit", command = exitRoomMapper)

	#Help
	helpMenu = Menu(m, tearoff = 0)
	helpMenu.add("command", label = "About", command = aboutRoomMapper)
	

	m.add("cascade", menu = fileMenu, label = "File")
	m.add("cascade", menu = helpMenu, label = "Help")

	return m
	

def mapText(self, data, info, colour):
	data = worldSpaceToCanvasSpace(data)
	
	x0 = int(data[0])
	y0 = int(data[1])
	self.labels.append(self.canvas.create_text(x0, y0, text = info, fill = colour))
	
def drawPoint(self, data, colour):
	data = worldSpaceToCanvasSpace(data)
	
	x0 = int(data[0])
	y0 = int(data[1])
	self.points.append(self.canvas.create_rectangle(x0 - 2.5, y0 - 2.5, x0 + 2.5, y0 + 2.5, 
		outline='black', fill=colour))

#Data is (x0, y0, x1, y1)
def drawLine(self, data):

	startPoint = (data[0], data[1])
	endPoint = (data[2], data[3])
	
	startPoint = worldSpaceToCanvasSpace(startPoint)
	endPoint = worldSpaceToCanvasSpace(endPoint)
	
	x0 = int(startPoint[0])
	y0 = int(startPoint[1])
	x1 = int(endPoint[0])
	y1 = int(endPoint[1])
	self.walls.append(self.canvas.create_line(x0,y0,x1,y1))

def setupBotIcon(self, data):
	data = worldSpaceToCanvasSpace(data)
	x0 = int(data[0])
	y0 = int(data[1])
	
	self.botPos = data
	self.piBotImage = PhotoImage(file = './anonBot.gif')
	self.bot = self.canvas.create_image(x0, y0, image = self.piBotImage)

#Updates where the pi bot is drawn in the canvas
def updateBotPos(self, data):
	data = worldSpaceToCanvasSpace(data)
	x0 = int(data[0])
	y0 = int(data[1])
	
	self.canvas.coords(self.bot, x0, y0)
	self.botPos = data

#Indicate bots facing direction with a line
#Takes angle as degrees for now
def setupBotAngle(self, data):
	angle = data
	angle = angle / 180.0 * math.pi
	
	x0 = int(self.botPos[0])
	y0 = int(self.botPos[1])
	
	difX = math.sin(angle)
	difY = math.cos(angle)
	
	x1 = x0 + (30 * difX)
	y1 = y0 - (30 * difY)
	
	self.botAngleLine = self.canvas.create_line(x0,y0,x1,y1)
	
def updateBotAngle(self, data):
	angle = data
	angle = angle / 180.0 * math.pi
	
	x0 = int(self.botPos[0])
	y0 = int(self.botPos[1])
	
	difX = math.sin(angle)
	difY = math.cos(angle)
	
	x1 = x0 + (30 * difX)
	y1 = y0 - (30 * difY)
	
	#Remove Old Line
	self.canvas.delete(self.botAngleLine)
	#Place New Line
	self.botAngleLine = self.canvas.create_line(x0,y0,x1,y1)
	
def setupMapping(self):
	self.points = []
	self.walls = []
	self.labels = []

def makeBox(loc = ()):

	length = int(loc[0] + loc[1]) + 5
	width = int(loc[2] + loc[3]) + 5

	room = []

	for i in range(length):
		line = []
		for j in range(width):
			if (i == 0 or j == 0) or (i == length - 1) or (j == width - 1):
				line.append(1)
			else:
				line.append(0)

		room.append(line)

	return room
	
"""
	This function checks the socket for messages for the GUI
"""
def display(queue, running, sh, root):
	
	while running:

		message = sh.listener.recv(sh.buf)

		if message == "exit":
			break

		if message == 'mes':
			mes = sh.listener.recv(sh.buf)
			if mes == "exit":
				break
			queue.put((root.displayMessage,[mes]))

		elif message == "data":

			mesStr = sh.listener.recv(sh.buf)
			print mesStr
			s = json.loads(mesStr)
			m = makeBox(s)

			queue.put((root.drawOnMap,[m]))
	
		elif message == "bot":
			mesStr = sh.listener.recv(sh.buf)
			m = json.loads(mesStr)
			queue.put((root.botLocation,[m]))		

	sh.listener.close()
	sh.server.close()
	os._exit(0)
			
class GUI(Tk):	
	def __init__(self, port = 13000 , queue = None):
		Tk.__init__(self)
		
		#Set window title
		self.title("AnonymousBot's Visual Room Mapper")
		
		#Set window minimum size
		self.minsize(windowWidth, windowHeight)
		self.maxsize(windowWidth, windowHeight)

		#Set 'X' close behaviour
		self.protocol("WM_DELETE_WINDOW", exitRoomMapper)

		#Change Background Color
		self.configure(background = "lavender")
		
		rightSide = Frame(self)
		textFrame = Frame(self)
		canvasFrame = Frame(rightSide)
		compareFrame = Frame(rightSide)
		
		rightSide.pack(side = RIGHT)
		canvasFrame.pack(side = TOP)
		textFrame.pack(side = RIGHT)
		compareFrame.pack(side = BOTTOM)
		
		#Create the Textbox
		self.textBox = Text(textFrame, width = 20, height = canvasHeight + 40, bg = 'grey')
		self.textBox.pack()

		#Create the Canvas
		self.canvas = Canvas(canvasFrame, width = canvasHeight + 40, height = canvasHeight + 40, bg = 'white')
		self.canvas.pack()
		
		#Create Compare Button
		self.compareButton = Button(compareFrame, text = "Compare Room", command = lambda: gui.displayMessage(gui.compareRoom()))
		self.compareButton.pack()
		
		m = mainMenu(self)
		self.configure(menu = m)
		
		self.queue = queue #this is the job queue

		#self.textBox.after(50, self.check_queue) #Uncomment
		
		self.currentRoom = [] #current 2D array(used for comparing rooms)
	
	def compareRoom(self):

		mypath = "./rooms"
		onlyfiles = [ f for f in listdir(mypath) if isfile(join(mypath,f)) ]

		pr = ProcessRoom()

		room = pr.openFile("./rooms/rooms2")

		roomList = ""

		for i in onlyfiles:
			r = pr.openFile(mypath+'/'+i)
			if pr.sameRoom(room,r):
				roomList += i + "\n"

		if roomList == "":
			return "No similar rooms found"
		else:
			return "Similar Rooms: \n" + roomList
	
	def clearMap(self):
		print "Clear Map"
		for point in self.points:
			self.canvas.delete(point)
		self.points = []
		
		for wall in self.walls:
			self.canvas.delete(wall)
		self.walls = []
		
		for label in self.labels:
			self.canvas.delete(label)
		self.labels = []
	
	#Checks if a point is a part of a wall, or is a lose point
	# Returns True if has neighbour points, false if isolated
	def neighbourWall(self, row, column):
		if column < len(currentData[0]) - 1:
			if currentData[row][column + 1] == 1:
				return True
		if column > 0:
			if currentData[row][column - 1] == 1:
				return True
		if row < len(currentData) - 1:
			if currentData[row + 1][column] == 1:
				return True
		if row > 0:
			if currentData[row - 1][column] == 1:
				return True
		
		return False
	
	#Returns true if diagonal wall
	def checkDiagonals(self, row, column):
		if column < len(currentData[0]) - 1 and row < len(currentData) - 1:
			if currentData[row + 1][column + 1] == 1:
				return True
		if column > 0 and row > 0:
			if currentData[row - 1][column - 1] == 1:
				return True
		if column < len(currentData[0]) - 1 and row > 0:
			if currentData[row - 1][column + 1] == 1:
				return True
		if column > 0 and row < len(currentData) - 1:
			if currentData[row + 1][column - 1] == 1:
				return True
				
		return False
	
	def drawWall(self, wallStart, wallEnd, length):
		labelPos = ((wallStart[0] + wallEnd[0]) / 2.0, (wallStart[1] + wallEnd[1]) / 2.0)
		mapText(gui, labelPos, str(length) + "cm", 'black')
		drawLine(self, (wallStart[0], wallStart[1], wallEnd[0], wallEnd[1]))
	
	def drawDiagonalWall(self, row, column):
		startPos = (row, column)
		direction = (0, 0)
		
		longestLength = 1
		length = 1
		
		if column < len(currentData[0]) - 1 and row < len(currentData) - 1:
			if currentData[row + 1][column + 1] == 1 and gui.neighbourWall(row + 1, column + 1) == False:
				direction = (1, 1)
				while currentData[row + direction[0]][column + direction[1]] == 1 and gui.neighbourWall(row + direction[0], column + direction[1]) == False:
					row = row + direction[0]
					column = column + direction[1]
					length += 1
					if row + direction[0] > len(currentData) - 1 or row + direction[0] < 0:
						break
					if column + direction[1] > len(currentData[row]) - 1 or column + direction[1] < 0:
						break
		
		if length > longestLength:
			endPos = (row, column)
			longestLength = length
		length = 1
		
		if column > 0 and row > 0:
			if currentData[row - 1][column - 1] == 1 and gui.neighbourWall(row - 1, column - 1) == False:
				direction = (-1, -1)
				while currentData[row + direction[0]][column + direction[1]] == 1 and gui.neighbourWall(row + direction[0], column + direction[1]) == False:
					row = row + direction[0]
					column = column + direction[1]
					length += 1
					if row + direction[0] > len(currentData) - 1 or row + direction[0] < 0:
						break
					if column + direction[1] > len(currentData[row]) - 1 or column + direction[1] < 0:
						break
		
		if length > longestLength:
			endPos = (row, column)
			longestLength = length
		length = 1
		
		
		if column < len(currentData[0]) - 1 and row > 0 and gui.neighbourWall(row - 1, column + 1) == False:
			if currentData[row - 1][column + 1] == 1:
				direction = (-1, 1)
				while currentData[row + direction[0]][column + direction[1]] == 1 and gui.neighbourWall(row + direction[0], column + direction[1]) == False:
					row = row + direction[0]
					column = column + direction[1]
					length += 1
					if row + direction[0] > len(currentData) - 1 or row + direction[0] < 0:
						break
					if column + direction[1] > len(currentData[row]) - 1 or column + direction[1] < 0:
						break
		
		if length > longestLength:
			endPos = (row, column)
			longestLength = length
		length = 1
		
		if column > 0 and row < len(currentData) - 1 and gui.neighbourWall(row + 1, column - 1) == False:
			if currentData[row + 1][column - 1] == 1:
				direction = (1, -1)
				while currentData[row + direction[0]][column + direction[1]] == 1 and gui.neighbourWall(row + direction[0], column + direction[1]) == False:
					row = row + direction[0]
					column = column + direction[1]
					length += 1
					if row + direction[0] > len(currentData) - 1 or row + direction[0] < 0:
						break
					if column + direction[1] > len(currentData[row]) - 1 or column + direction[1] < 0:
						break
		
		if length > longestLength:
			endPos = (row, column)
			longestLength = length
			
		gui.drawWall(startPos, endPos, longestLength)
		
	def drawHorizontalWalls(self):
		row = 0
		column = 0
		wall = False
		wallStart = (0, 0)
		wallEnd = (0, 0)
		length = 0
		
		#Horizontal Walls
		i = 0
		j = 0
		
		for j in range(0, len(currentData[0])):
			for i in range(0, len(currentData) - 1):
				entry = currentData[i][j]
				if entry == 1:
					length += 1
					if wall == False:
						wall = True
						wallStart = (row, column)
				else:
					if wall == True:
						wall = False
						if length > 1:
							wallEnd = (row, column)
							gui.drawWall(wallStart, wallEnd, length)
						elif gui.neighbourWall(row - 1, column) == False: #If Not a solid wall, check for diagonals
							if gui.checkDiagonals(row - 1, column) == False: #If not a diagonal wall, mark point
								drawPoint(self, wallStart, 'black')
							else:
								gui.drawDiagonalWall(row - 1, column)
					length = 0
				row += 1				
			#If Wall goes to final column
			if wall == True:
				row -= 1
				wall = False
				if length > 1:
					wallEnd = (row, column)
					gui.drawWall(wallStart, wallEnd, length)
				elif gui.neighbourWall(row, column) == False: #If Not a solid wall, check for diagonals
					if gui.checkDiagonals(row, column) == False: #If not a diagonal wall, mark point
						drawPoint(self, wallStart, 'black')
					else:
						gui.drawDiagonalWall(row, column)
					
			length = 0
			row = 0
			column += 1
		
	def drawVerticalWalls(self):
		row = 0
		column = 0
		wall = False
		wallStart = (0, 0)
		wallEnd = (0, 0)
		length = 0
		
		#Vertical Walls
		for dataRow in currentData:
			for entry in dataRow:	
				if entry == 1:
					length += 1
					if wall == False:
						wall = True
						wallStart = (row, column)
				else:
					if wall == True:
						wall = False
						if length > 1:
							wallEnd = (row, column)
							gui.drawWall(wallStart, wallEnd, length)
						elif gui.neighbourWall(row, column - 1) == False: #If Not a solid wall, check for diagonals
							if gui.checkDiagonals(row, column - 1) == False: #If not a diagonal wall, mark point
								drawPoint(self, wallStart, 'black')
							else:
								gui.drawDiagonalWall(row, column - 1)
						
					length = 0
				column += 1
				
			#If Wall goes to final row
			if wall == True:
				column -= 1
				wall = False
				if length > 1:
					wallEnd = (row, column)
					gui.drawWall(wallStart, wallEnd, length)
				elif gui.neighbourWall(row, column) == False: #If Not a solid wall, check for diagonals
					if gui.checkDiagonals(row, column) == False: #If not a diagonal wall, mark point
						drawPoint(self, wallStart, 'black')
					else:
						gui.drawDiagonalWall(row, column)
			length = 0
			row += 1
			column = 0
		
	
	def processMap(self):
		global currentData
		
		gui.clearMap()
		print "Process Map"
		
		gui.drawHorizontalWalls()
		gui.drawVerticalWalls()
		
		
	#Map Data Legend
	# 0 -> Empty
	# 1 -> Wall
	# 8 -> Robot
	# 9 -> Unreachable Space	
	
	def mapPoints(self, row, column, entry):		
		if (entry == 1):
			drawPoint(self, (row, column), 'blue')
		elif (entry == 8):
			drawPoint(self, (row, column), 'green')
		elif (entry == 9):
			drawPoint(self, (row, column), 'black')
	
	"""
		Functions called by AI
	"""
	def drawOnMap(self, data):
		global currentData
		global mapWidth
		global mapHeight
		
		self.currentRoom = data
		
		mapWidth = float(len(data))
		mapHeight = float(len(data[0]))
		
		#Copy data in case final map
		currentData = data[:]
		gui.clearMap()
		
		row = 0
		column = 0
		for dataRow in data:
			for entry in dataRow:
				column += 1
				self.mapPoints(row, column, entry)
			row += 1
			column = 0

	def displayMessage(self, message):
		self.textBox.insert(INSERT, message + "\n")
		#Change to actual done message
		if (message == "Mapping Complete!"):
			gui.processMap()
		
	def botLocation(self, location):
		#location is a 3 tuple (ints). (y,x,a)
		#y = the bots y cord
		#x = the bots x cord
		#a = angle the bot is at. 0 = up, 90 = right etc
		y = location[0]
		x = location[1]
		angle = location[2]
		
		updateBotPos(self, (x,y))
		updateBotAngle(self, angle)
		
		self.textBox.insert(INSERT, str(location)) #just a test
	
	"""
		This function checks queue intermittently.
	"""
	def check_queue(self):
		try:
			f, arg = self.queue.get(block = False)
		except Queue.Empty:
			pass#queue is empty. Nothing to do
		else:
			f(*arg)

		self.textBox.after(50, self.check_queue)
	
#Main Starts here

if __name__ == "__main__":

	port = 13000

	if len(sys.argv) != 2:
			print "using default port number 13000"
			print "To use a different port number include the number at the end of the command"
			print "ex: python GUI.py 8080"
	else:
		try:
			port = int(sys.argv[1])
		except ValueError:
			print "Please enter an integer for the port number"
			print "using default port number 13000"

	print "Using port:" + str(port)

	q = Queue.Queue()
	running = [True]


	gui = GUI(port = 13000,queue = q)
	""" # Uncomment
	sh = SocketHelper(port = port)

	gui.textBox.bind('<Destroy>', lambda x: (running.pop(), x.widget.destroy()))

	thread = threading.Thread(target = display, args = (q, running, sh, gui))
	thread.setDaemon(True)
	thread.start()
	"""

	setupMapping(gui)
	setupBotIcon(gui, (mapWidth / 2.0, mapHeight / 2.0))
	setupBotAngle(gui, 0)

	#Testing
	isTesting = True

	if isTesting == True:
		drawLine(gui, (0, 0, 50, 50))
		drawPoint(gui, (50, 50), 'blue')
		gui.displayMessage("Test")
		updateBotPos(gui, (250, 250))
		updateBotAngle(gui, 90)
		mapText(gui, (300, 300), "Test", 'blue')
		map = readTestFile("sampleMap01.txt")
		#map = readTestFile("sampleMap02.txt")
		#map = readTestFile("sampleMap03.txt")
		#map = readTestFile("sampleMap04.txt")
		#map = readTestFile("sampleMap05.txt")
		gui.drawOnMap(map)
		
		gui.displayMessage("Mapping Complete!")

	gui.mainloop()
