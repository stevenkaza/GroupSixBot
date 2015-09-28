#Completely work in progress, will be merged with UI port code after and moved into appropriate file

import math #Used for drawing the facing direction line

import tkFileDialog
import tkMessageBox
from Tkinter import *


from PIL import Image, ImageTk

def exitRoomMapper():
	if tkMessageBox.askyesno('Quitting . . .', 'Are you sure you want to quit?'):
		g.quit()

def aboutRoomMapper():
	tkMessageBox.showinfo("About Room Mapper", "Room Mapper Beta V 1.0 \n\n Team: Kory Bryson, Mitchell Cook, Steven Kazavchinski, Zack Licastro, Amanda Reuillon \n\n A tool to visualize room mapper from a Pi Bot room mapper.")
	
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
	helpMenu = Menu(m, tearoff=0)
	helpMenu.add("command", label="About", command = aboutRoomMapper)
	

	m.add("cascade", menu=fileMenu, label="File")
	m.add("cascade", menu=helpMenu, label="Help")

	return m
	
def buildCanvas(root):
	global canvas 
	canvas = Canvas(root)
	canvas.create_rectangle(30, 10, 120, 80, 
			outline="#fb0", fill="#fb0")
	canvas.pack()
	

def drawPoint(self, data):
	x0 = int(data[0])
	y0 = int(data[1])
	self.c.create_rectangle(x0, y0, x0 + 5, y0 + 5, 
		outline='black', fill='blue')

def drawLine(self, data):
	#date is a 4 tuple ie (0,0,100,100)
	x0 = int(data[0])
	y0 = int(data[1])
	x1 = int(data[2])
	y1 = int(data[3])
	self.c.create_line(x0,y0,x1,y1)

def displayMessage(self, message):
	self.t.insert(INSERT, message)
	
def setupBotIcon(self, data):
	x0 = int(data[0])
	y0 = int(data[1])
	
	self.botPos = data
	self.piBotImage = PhotoImage(file = './piBotTest.gif')
	self.bot = self.c.create_image(x0, y0, image = self.piBotImage)

#Updates where the pi bot is drawn in the canvas
def updateBotPos(self, data):
	x0 = int(data[0])
	y0 = int(data[1])
	
	self.c.coords(self.bot, x0, y0)
	self.botPos = data

#Indicate bots facing direction with a line
# Takes angle as degrees for now
# **Needs updated to a updateBotAngle and createBotAngle function
def drawBotAngle(self, data):
	angle = data
	angle = angle / 180.0 * math.pi
	
	x0 = int(self.botPos[0])
	y0 = int(self.botPos[1])
	
	difX = math.sin(angle)
	difY = math.cos(angle)
	print(difX)
	print(difY)
	
	x1 = x0 + (30 * difX)
	y1 = y0 - (30 * difY)
	
	self.c.create_line(x0,y0,x1,y1)
	
class UITesting(Tk):
	canvas = 0
	
	def __init__(self):
		Tk.__init__(self)
		
		#Set window title
		self.title("AnonymousBot's Visual Room Mapper")
		
		#Set window minimum size
		self.minsize(650, 475)

		#Set 'X' close behaviour
		self.protocol("WM_DELETE_WINDOW", exitRoomMapper)

		#Change Background Color
		self.configure(background="lavender")
		
		frameT = Frame(self)
		frameC = Frame(self)
		frameC.pack(side = RIGHT)
		frameT.pack(side = RIGHT)
		
		#self.t = Text(frameT,width = 10,height = 10)
		self.t = Text(frameT, width = 20, bg = 'grey')
		self.t.pack()

		#self.c = Canvas(frameC,bg = 'red',height = 200, width = 200)
		self.c = Canvas(frameC, bg = 'white', height = 490)
		self.c.pack()
		
		m = mainMenu(self)
		self.configure(menu=m)
	


	
#Main Starts here
g = UITesting()

#Testing
drawLine(g, (0, 0, 50, 50))
drawPoint(g, (50, 50))
displayMessage(g, "Test")

setupBotIcon(g, (50, 50))
updateBotPos(g, (150, 200))

drawBotAngle(g, 0)

g.mainloop()
