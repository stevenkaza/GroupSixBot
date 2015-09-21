from Tkinter import *
from UI import *
import threading
import thread
import os
from socket import *

class GUI(Tk):
	def __init__(self):
		Tk.__init__(self)
		frameT = Frame(self)
		frameC = Frame(self)
		frameC.pack(side = RIGHT)
		frameT.pack(side = RIGHT)
		
		self.t = Text(frameT,width = 10,height = 10)
		self.t.pack()

		self.c = Canvas(frameC,bg = 'red',height = 200, width = 200)
		self.c.pack()
		self.u = UI()

	def drawOnMap(self, data):
		#date is a 4 tuple ie (0,0,100,100)
		x0 = int(data[0])
		y0 = int(data[1])
		x1 = int(data[2])
		y1 = int(data[3])
		self.c.create_line(x0,y0,x1,y1)

	def displayMessage(self, message):
		self.t.insert(INSERT, message)

	def display(self):
		while 1:
			(data, self.u.addr) = self.u.UDPSock.recvfrom(self.u.buf)			
			print "Received message: " + data
			if data == "exit":
				break
			elif data == "draw":
				self.drawOnMap((0,0,55,55))
			else:
				self.displayMessage(data)
		self.u.UDPSock.close()
		os._exit(0)

class TextFrame(Text):
	def __init__(self,top):
		Text.__init__(self,top,width = 10,height = 10)
		self.pack()

	def displayMessage(self,message):
		self.insert(INSERT, message)

class CanFrame(Canvas):
	def __init__(self,top):
		Canvas.__init__(self,top,bg = 'red',height = 200, width = 200)
		self.pack()

	def draw(self):
		self.create_line(1,1,40,40)

if __name__ == "__main__":

	g = GUI()

	thread.start_new_thread ( g.display,())

	g.mainloop()