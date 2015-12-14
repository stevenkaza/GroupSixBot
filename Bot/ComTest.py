from Com import *
import time
import sys
import json

class ComTest:
	def __init__(self, port = 13000, host = "localhost"):
		"""
			This function has two objects right now
			move will control the movement of the pibot
			com controls the communication.
			Basically the AI gets information from the sensors (Maybe thats a class aswell?)
			does its AI stuff, calls move to move the bot and calls com to update the laptop
		"""

		self.com = Com(port = port, host = host)

	def sense(self):
		command = raw_input("mes or data or bot?: ")

		if command == "exit":
			self.com.sendMessage(command)
			self.com.end()
			return command

		if command == "mes":

			self.com.sendMessage('mes')
			mes = raw_input("Whats your message: ")

			if mes == "exit":
				self.com.sendMessage(mes)
				self.com.end()
				return mes
			else:
				self.com.sendMessage(mes)
		elif command == "bot": #sends bot location
			self.com.sendMessage('bot')
			self.com.sendBotLocation((4,4,90))
		elif command == "data":			
			while 1:
				m = [[1]*100] * 100
			
				#test data

				self.com.sendMessage("data")
				self.com.updateMap(m)
				self.com.sendMessage(":end")
				break
		else:
			self.com.sendMessage("Mapping Complete!")

		return command

if __name__ == "__main__":

	port = 13000
	ip = "localhost"

	if len(sys.argv) == 1:
		print "using default port number 13000 and IP address localhost"
		print "To use a different port number and IP address include the number at the end of the command"
		print "ex: python AI.py 8080 192.168.0.101"
	elif len(sys.argv) == 2:
		try:
			port = int(sys.argv[1])
		except ValueError:
			print "Please enter an integer for the port number"
			print "using default port number 13000"
	else:
		ip = sys.argv[2]
		try:
			port = int(sys.argv[1])
		except ValueError:
			print "Please enter an integer for the port number"
			print "using default port number 13000"

	print "Using port:" + str(port) + " and IP " + ip

	c = ComTest(port = port, host = ip)

	while True:
		c.sense()