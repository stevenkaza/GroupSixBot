import os
import socket               # Import socket module

class SocketHelper:
	
	def __init__(self,host = "",port = 13000,buf = 1024,handler = None):
		
		self.handler = handler #handles delegation from communication to GUI

		self.buf = buf
		self.addr = (host, port)

		self.server = socket.socket()  # Reserve a port for your service.
		self.server.bind(self.addr)        # Bind to the port

		self.server.listen(1)                 # Now wait for client connection.
		print "Waiting: ", self.addr
		self.listener,addr = self.server.accept() #waits until 1 socket connects to it
		
	def displayMes(self,mes):
		func = getattr(self.Handler,"displayMes")
		func(mes)

	def drawOnMap(self,data):
		func = getattr(self.Handler,"drawOnMap")
		func(mes)

	def display(self):
		
		while 1:

			message = self.listener.recv(self.buf)			
			print "Received message: " + message

			if message == 'mes':
				mes = self.listener.recv(self.buf)	
				self.displayMessage(mes)

			if data == "exit":
				break
			elif data == "draw":
				self.drawOnMap((0,0,55,55))
		

		self.listener.close()
		self.server.close()
		os._exit(0)

if __name__ == "__main__":

	s = SocketHelper()

	s.display()