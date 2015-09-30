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
	
	def __init__(self,port = 13000 ,queue= None):
		
		Tk.__init__(self)

		#all GUI related objects can be changed. However we need to have a Text widget and a Canvas
		frameT = Frame(self)
		frameC = Frame(self)
		frameC.pack(side = RIGHT)
		frameT.pack(side = RIGHT)
		
		#feel free to rename these.
		self.t = Text(frameT,width = 10,height = 10)
		self.t.pack()

		self.c = Canvas(frameC,bg = 'red',height = 200, width = 200)
		self.c.pack()

		self.queue = queue #this is the job queue

		self.t.after(50, self.check_queue)#this line needs to stay the same. the variable name can be changed

	"""The following 3 functions can be changed to do whatever is best. The only thing that needs to stay the same
		are the function names and parameter types.
	"""
	def drawOnMap(self, data):
		#date is a 4 tuple ie (0,0,100,100)
		self.c.create_line(0,0,55,34)
		#draw on the map.

	def displayMessage(self, message):
		self.t.insert(INSERT, message)

	def botLocation(self, location):
		#location is a 3 tuple (ints). (y,x,a)
		#y = the bots y cord
		#x =the bots x cord
		#a = angle the bot is at. 0 = up, 90 = right etc
		self.t.insert(INSERT, str(location)) #just a test

	"""
	This function is complete and shouldn't be modified unless you change the 
	name for the Text widget
	"""
	def check_queue(self):
		
		try:
			f,arg = self.queue.get(block=False)
		except Queue.Empty:
			pass#queue is empty. Nothing to do
		else:
			f(*arg)

		self.t.after(50, self.check_queue)#the name 't' can be changed

"""This function is complete. It does not need any modification
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

"""
This main should not be changed
"""
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
	
	root = GUI(queue = q,port = port)

	sh = SocketHelper(port = port)

	root.t.bind('<Destroy>', lambda x: (running.pop(), x.widget.destroy()))

	thread = threading.Thread(target=display, args=(q,running,sh,root))
	thread.setDaemon(True)
	thread.start()

	root.mainloop()