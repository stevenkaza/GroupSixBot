from Tkinter import *
from SocketHelper import *
import threading
import time
import thread
import os
from socket import *
import sys
from Map import *
import Queue

class GUI(Tk):
	
	def __init__(self,port = 13000 ,q= None):
		
		Tk.__init__(self)
		frameT = Frame(self)
		frameC = Frame(self)
		frameC.pack(side = RIGHT)
		frameT.pack(side = RIGHT)
		
		self.t = Text(frameT,width = 10,height = 10)
		self.t.pack()

		self.c = Canvas(frameC,bg = 'red',height = 200, width = 200)
		self.c.pack()

		
		#self.sh = SocketHelper(port = port, handler = self) #GUI needs this line

		self.q = q

		self.t.after(50, self.check_queue)

	def drawOnMap(self, data):
		#date is a 4 tuple ie (0,0,100,100)
		self.c.create_line(0,0,55,34)
		#draw on the map.

	def displayMessage(self, message):
		self.t.insert(INSERT, message)

	def botLocation(self, location):
		#location is a 3 tuple. (y,x,a)
		#y = the bots y cord
		#x =the bots x cord
		#a = angle the bot is at. 0 = up, 90 = right etc
		self.t.insert(INSERT, str(location)) #just a test

	def check_queue(self):
		
		try:
			f,arg = self.q.get(block=False)
		except Queue.Empty:
			pass
		else:
			f(*arg)
		self.t.after(50, self.check_queue)

def display(q,running):
	
	global sh
	global root

	while running:

		message = sh.listener.recv(sh.buf)

		print "Received message: " + message

		if message == "exit":
			break

		if message == 'mes':
			mes = sh.listener.recv(sh.buf)
			if mes == "exit":
				break
			
			q.put((root.displayMessage,[mes]))

		elif message == "data":
			mesStr = sh.listener.recv(sh.buf)
			m = json.loads(mesStr)
			q.put((root.drawOnMap,[m]))

		elif message == "bot":
			mesStr = sh.listener.recv(sh.buf)
			m = json.loads(mesStr)
			q.put((root.botLocation,[m]))
		

	sh.listener.close()
	sh.server.close()
	os._exit(0)

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
	global root
	root = GUI(q = q,port = port)

	global sh
	sh = SocketHelper(port = port)

	root.t.bind('<Destroy>', lambda x: (running.pop(), x.widget.destroy()))

	thread = threading.Thread(target=display, args=(q,running))
	thread.setDaemon(True)
	thread.start()

	root.mainloop()