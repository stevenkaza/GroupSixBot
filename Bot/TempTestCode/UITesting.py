#Completely work in progress, will be merged with UI port code after and moved into appropriate file

import math #Used for drawing the facing direction line

import tkFileDialog
import tkMessageBox
from Tkinter import *

from PIL import Image, ImageTk

#from SocketHelper import *
import threading
import time
import thread
import os
#from socket import *
import sys
#from Map import *
import Queue

windowWidth = 675
windowHeight = 500

canvasWidth = 450
canvasHeight = 450

mapWidth = 1200.0
mapHeight = 1200.0

#Map Data Legend
# 0 -> Empty
# 1 -> Wall
# 8 -> Robot
# 9 -> Unreachable Space

#Position is (x,y), returns new position as (x,y) in canvas space
def worldSpaceToCanvasSpace(position):
	newPosition = ((position[0] / mapWidth) * canvasWidth, (position[1] / mapHeight) * canvasHeight)
	return newPosition

def exitRoomMapper():
	if tkMessageBox.askyesno('Quitting . . .', 'Are you sure you want to quit?'):
		gui.quit()
		
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
	
	fileMenu.add("command", label="Save Map to PostScript", command = lambda: saveMap(r))
	fileMenu.add("command", label="Save Text Log", command = lambda: saveTextLog(r))
	fileMenu.add("command", label="Exit", command = exitRoomMapper)

	#Help
	helpMenu = Menu(m, tearoff = 0)
	helpMenu.add("command", label = "About", command = aboutRoomMapper)
	

	m.add("cascade", menu = fileMenu, label = "File")
	m.add("cascade", menu = helpMenu, label = "Help")

	return m
	

def mapText(self, data, info):
	data = worldSpaceToCanvasSpace(data)
	
	x0 = int(data[0])
	y0 = int(data[1])
	self.canvas.create_text(x0, y0, text = info, fill = 'black')
	
def drawPoint(self, data):
	data = worldSpaceToCanvasSpace(data)
	
	x0 = int(data[0])
	y0 = int(data[1])
	self.canvas.create_rectangle(x0, y0, x0 + 5, y0 + 5, 
		outline='black', fill='blue')

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
	self.canvas.create_line(x0,y0,x1,y1)

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
	
	
	
"""
	This function checks the socket for messages for the GUI
"""
def display(queue, running, sh, root):
	
	while running:

		message = sh.listener.recv(sh.buf)

		print "Received message: " + message

		if message == "exit":
			break

		if message == 'mes':
			mes = sh.listener.recv(sh.buf)
			if mes == "exit":
				break
			queue.put((root.displayMessage,[mes]))

		elif message == "data":
			mesStr = sh.listener.recv(sh.buf)
			m = json.loads(mesStr)
			queue.put((root.drawOnMap,[m]))

		elif message == "bot":
			mesStr = sh.listener.recv(sh.buf)
			m = json.loads(mesStr)
			queue.put((root.botLocation,[m]))
		

	sh.listener.close()
	sh.server.close()
	os._exit(0)
	
class UITesting(Tk):	
	def __init__(self):
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
		
		textFrame = Frame(self)
		canvasFrame = Frame(self)
		canvasFrame.pack(side = RIGHT)
		textFrame.pack(side = RIGHT)
		
		#Create the Textbox
		self.textBox = Text(textFrame, width = 20, height = canvasHeight + 40, bg = 'grey')
		self.textBox.pack()

		#Create the Canvas
		self.canvas = Canvas(canvasFrame, width = canvasHeight + 40, height = canvasHeight + 40, bg = 'white')
		self.canvas.pack()
		
		m = mainMenu(self)
		self.configure(menu = m)
		
		#self.queue = queue #this is the job queue

		#self.textBox.after(50, self.check_queue)
	
	"""
		Functions called by AI
	"""
	def drawOnMap(self, data):
		#draw the map.
		print data	

	def displayMessage(self, message):
		self.textBox.insert(INSERT, message)
		
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
			f,arg = self.queue.get(block = False)
		except Queue.Empty:
			pass#queue is empty. Nothing to do
		else:
			f(*arg)

		self.textBox.after(50, self.check_queue)
	
#Main Starts here

"""
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
"""

gui = UITesting()
"""
	sh = SocketHelper(port = port)

	gui.textBox.bind('<Destroy>', lambda x: (running.pop(), x.widget.destroy()))

	thread = threading.Thread(target = display, args = (q, running, sh, gui))
	thread.setDaemon(True)
	thread.start()
"""
setupBotIcon(gui, (mapWidth / 2.0, mapHeight / 2.0))
setupBotAngle(gui, 0)

#Testing
isTesting = True

if isTesting == True:
	drawLine(gui, (0, 0, 50, 50))
	drawPoint(gui, (50, 50))
	gui.displayMessage("Test")
	updateBotPos(gui, (600, 600))
	updateBotAngle(gui, 90)
	mapText(gui, (300, 300), "Test")


gui.mainloop()
