from Tkinter import *
from SocketHelper import *
import threading
import thread
import os
from socket import *
import sys
from Map import *

class GUI(Tk):
	
	def __init__(self,port = 13000):
		
		Tk.__init__(self)
		frameT = Frame(self)
		frameC = Frame(self)
		frameC.pack(side = RIGHT)
		frameT.pack(side = RIGHT)
		
		self.t = Text(frameT,width = 10,height = 10)
		self.t.pack()

		self.c = Canvas(frameC,bg = 'red',height = 200, width = 200)
		self.c.pack()

		
		self.sh = SocketHelper(port = port, handler = self) #GUI needs this line

	def drawOnMap(self, data):
		#date is a 4 tuple ie (0,0,100,100)
		x0 = int(data[0])
		y0 = int(data[1])
		x1 = int(data[2])
		y1 = int(data[3])
		self.c.create_line(x0,y0,x1,y1)

	def displayMessage(self, message):
		self.t.insert(INSERT, message)


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

	g = GUI(port)

	thread.start_new_thread ( g.sh.display,())

	g.mainloop()