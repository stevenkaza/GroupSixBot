#Completely work in progress, will be merged with UI port code after and moved into appropriate file

import math #Used for drawing the facing direction line

import tkFileDialog
import tkMessageBox
from Tkinter import *


from PIL import Image, ImageTk

windowWidth = 650
windowHeight = 475

#Map Data Legend
# 0 -> Empty
# 1 -> Wall
# 8 -> Robot
# 9 -> Unreachable Space

def exitRoomMapper():
	if tkMessageBox.askyesno('Quitting . . .', 'Are you sure you want to quit?'):
		gui.quit()

def aboutRoomMapper():
	tkMessageBox.showinfo("About Room Mapper", "Room Mapper Beta V 1.0 \n\nTeam: \nKory Bryson - Communications Lead, \nMitchell Cook - AI Lead, \nSteven Kazavchinski - Movement and Sensor Lead, \nZack Licastro - UI Co-Lead, \nAmanda Reuillon - UI Co-Lead \n\n A tool to visualize room mapper from a Pi Bot room mapper.")
	
#Set Up Menu
def mainMenu(r):
	m = Menu(r)

	global fileMenu
	global helpMenu

	#File
	fileMenu = Menu(m, tearoff=0)
	#fileMenu.add("command", label="Save", command = saveFile, state = DISABLED)
	#fileMenu.add("command", label="Save As", command = saveFileAs, state = DISABLED)
	fileMenu.add("command", label="Exit", command = exitRoomMapper)

	#Help
	helpMenu = Menu(m, tearoff = 0)
	helpMenu.add("command", label = "About", command = aboutRoomMapper)
	

	m.add("cascade", menu = fileMenu, label = "File")
	m.add("cascade", menu = helpMenu, label = "Help")

	return m
	

def mapText(self, data, info):
	x0 = int(data[0])
	y0 = int(data[1])
	self.canvas.create_text(x0, y0, text = info)
	
def drawPoint(self, data):
	x0 = int(data[0])
	y0 = int(data[1])
	self.canvas.create_rectangle(x0, y0, x0 + 5, y0 + 5, 
		outline='black', fill='blue')

def drawLine(self, data):
	#date is a 4 tuple ie (0,0,100,100)
	x0 = int(data[0])
	y0 = int(data[1])
	x1 = int(data[2])
	y1 = int(data[3])
	self.canvas.create_line(x0,y0,x1,y1)

def displayMessage(self, message):
	self.textBox.insert(INSERT, message)
	
def setupBotIcon(self, data):
	x0 = int(data[0])
	y0 = int(data[1])
	
	self.botPos = data
	self.piBotImage = PhotoImage(file = './anonBot.gif')
	self.bot = self.canvas.create_image(x0, y0, image = self.piBotImage)

#Updates where the pi bot is drawn in the canvas
def updateBotPos(self, data):
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
	
class UITesting(Tk):
	
	def __init__(self):
		Tk.__init__(self)
		
		#Set window title
		self.title("AnonymousBot's Visual Room Mapper")
		
		#Set window minimum size
		self.minsize(windowWidth, windowHeight)

		#Set 'X' close behaviour
		self.protocol("WM_DELETE_WINDOW", exitRoomMapper)

		#Change Background Color
		self.configure(background = "lavender")
		
		textFrame = Frame(self)
		canvasFrame = Frame(self)
		canvasFrame.pack(side = RIGHT)
		textFrame.pack(side = RIGHT)
		
		#Create the Textbox
		self.textBox = Text(textFrame, width = 20, bg = 'grey')
		self.textBox.pack()

		#Create the Canvas
		self.canvas = Canvas(canvasFrame, bg = 'white', height = 490)
		self.canvas.pack()
		
		m = mainMenu(self)
		self.configure(menu = m)
	
#Main Starts here
gui = UITesting()

setupBotIcon(gui, (50, 50))
setupBotAngle(gui, 0)

#Testing
isTesting = True

if isTesting == True:
	drawLine(gui, (0, 0, 50, 50))
	drawPoint(gui, (50, 50))
	displayMessage(gui, "Test")
	updateBotPos(gui, (150, 200))
	updateBotAngle(gui, 90)
	mapText(gui, (300, 300), "Test")


gui.mainloop()
