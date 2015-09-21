import os
from socket import *

class UI:
	def __init__(self,host ="",port = 13000,buf = 1024):
		self.buf = buf
		self.addr = (host, port)
		self.UDPSock = socket(AF_INET, SOCK_DGRAM)
		self.UDPSock.bind(self.addr)

	def display(self):
		globals.message = "cat"
		while 1:
			(data, self.addr) = self.UDPSock.recvfrom(self.buf)			
			print "Received message: " + data
			if data == "exit":
				break
		self.UDPSock.close()
		os._exit(0)