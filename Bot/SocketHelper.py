import os
import socket               # Import socket module

class SocketHelper:
	def __init__(self,host = "",port = 13000,buf = 1024):
		
		self.buf = buf
		self.addr = (host, port)
		#self.server = socket.socket(AF_INET, SOCK_DGRAM)
		#self.server.bind(self.addr)
		#self.server.listen(1)


		self.server = socket.socket()  # Reserve a port for your service.
		self.server.bind(self.addr)        # Bind to the port

		self.server.listen(1)                 # Now wait for client connection.
		print "Waiting: ", self.addr
		self.listener,addr = self.server.accept()
		


	def display(self):

		while 1:
			data = self.listener.recv(self.buf)			
			print "Received message: " + data
			if data == "exit":
				break

		self.server.close()
		os._exit(0)

if __name__ == "__main__":

	s = SocketHelper()

	s.display()