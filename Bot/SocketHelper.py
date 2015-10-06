import os
import socket               # Import socket module
from Map import *
import json
import sys
class SocketHelper:
	
	def __init__(self,host = "",port = 13000,buf = 2070000000,handler = None):
		
		self.handler = handler #handles delegation from communication to GUI

		self.buf = buf
		self.addr = (host, port)

		self.server = socket.socket()  # Reserve a port for your service.
		self.server.bind(self.addr)        # Bind to the port

		self.server.listen(1)                 # Now wait for client connection.
		print "Waiting: ", self.addr
		self.listener,addr = self.server.accept() #waits until 1 socket connects to it
		
	def displayMessage(self,mes):
		func = getattr(self.handler,"displayMessage")
		func(mes)

	def drawOnMap(self,data):
		func = getattr(self.handler,"drawOnMap")
		func(data)

	def botLocation(self,data):
		func = getattr(self.handler,"botLocation")
		func(data)

	def display(self):
		
		while 1:

			message = self.listener.recv(self.buf)

			print "Received message: " + message

			if message == "exit":
				break

			if message == 'mes':
				mes = self.listener.recv(self.buf)
				if mes == "exit":
					break
				try:
					self.displayMessage(mes)
				except Exception:
					pass

			elif message == "data":
				mesStr = self.listener.recv(self.buf)
				m = json.loads(mesStr)
				self.drawOnMap(m)

			elif message == "bot":
				mesStr = self.listener.recv(self.buf)
				m = json.loads(mesStr)
				self.botLocation(m)
		

		self.listener.close()
		self.server.close()
		os._exit(0)

if __name__ == "__main__":

	s = SocketHelper()

	s.display()