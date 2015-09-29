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
		x = 0
		#draw on the map.

	def displayMessage(self, message):
		self.t.insert(INSERT, message)

	def botLocation(self, location):
		#location is a 3 tuple. (y,x,a)
		#y = the bots y cord
		#x =the bots x cord
		#a = angle the bot is at. 0 = up, 90 = right etc
		x = 0
		self.t.insert(INSERT, str(location)) #just a test

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