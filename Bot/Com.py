import os
from socket import *
import json
import time

class Com:

	def __init__(self, port = 13000, host = "192.168.0.101"):
		"""
		This constructor initiatizes addr (the addresss of the server) and UDPSock (how 
		the client talks to the server)
		
		Args:
			port(int): an open port (may need to be changed)
			host(string): IP address of the SERVER. will need to be updated before we run the bot.

		"""
		self.addr = (host, port)
		self.client = socket()
		self.client.connect(self.addr)

	"""
		for now the following two functions do the exact same thing.
		I think it maybe best to only have one function call the server and based on what message
		the client sends have the server parse it and perform the right operations
	"""

	def split_list(self, a_list):
		half = int(float(len(a_list))/2.0)
		q = half/2

		s = a_list[:half]
		e = a_list[half:]

		return s[:q], s[q:] , e[:q], e[q:]

	def split (self, data):
		s1 = []
		s2 = []
		e1 = []
		e2 = []

		for line in data:
			start1,start2,end1,end2 = self.split_list(line)
			s1.append(start1)
			s2.append(start2)
			e1.append(end1)
			e2.append(end2)

		return s1,s2,e1,e2

	def sendMessage(self, message):
		self.client.send(str(message))

	def updateMap(self,data):

		#data needs to be turn into a string (for now). It will be a 2D array
		'''
		s1,s2,e1,e2 = self.split(data)

		dataStr = json.dumps(s1)
		self.client.send(dataStr)

		time.sleep(1)
		dataStr = json.dumps(s2)
		self.client.send(dataStr)

		time.sleep(1)

		dataStr = json.dumps(e1)
		self.client.send(dataStr)
		
		time.sleep(1)

		dataStr = json.dumps(e2)

		'''
		dataStr = json.dumps(data)

		self.client.send(dataStr)


	def sendBotLocation(self,location):
		dataStr = json.dumps(location)
		self.client.send(dataStr)

	def end(self):
		"""
			This function simply closes the socket
		"""
		self.client.close()
		os._exit(0)