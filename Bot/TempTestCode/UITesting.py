#Completely work in progress, will be merged with UI port code after and moved into appropriate file

#import Tix as tix
import tkFileDialog
import tkMessageBox
from Tkinter import *
#from Tkinter import tix
#from Tkinter.filedialog import *
#from Tkinter.messagebox import *

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
	
	
	

#Set Up Main Window
#def buildMainWindow():
#	global root
#	root = Tk()
#	
#	#Set window title
#	root.title("AnonymousBot's Visual Room Mapper")
	
	#Set window minimum size
#	root.minsize(650, 625)
#
#	#Set 'X' close behaviour
#	root.protocol("WM_DELETE_WINDOW", exitRoomMapper)
#
#	#Change Background Color
#	root.configure(background="lavender")
	
	#Set up Menu
#	m = mainMenu(root)
#	root.configure(menu=m)
	
#	return root

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
		
		#Testing
		drawLine(self, (0, 0, 50, 50))
		drawPoint(self, (50, 50))
		displayMessage(self, "Test")
		
	


	
#Main Starts here
g = UITesting()
#mw=buildMainWindow()
g.mainloop()
