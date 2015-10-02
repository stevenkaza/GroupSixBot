#from Move import *
from Com import *
import sys
import json
from Map import *

class AI:
	room = Map([])
	#movement = Move()
	#sensor = Sensor()
    
    #bot = BOT()
	botAngle = 0
	botPos = [0,0]
    
	turnAngle  = 5 # the angle the bot will turn to sense
    
	def mapRoom(self):
		while not room.isMapped():
			sense()
			route = room.nextRoute()
			for i in route:
				break
			break
		return
    
	def __init__(self, port = 13000, host = "localhost"):
		"""
			This function has two objects right now
			move will control the movement of the pibot
			com controls the communication.
			Basically the AI gets information from the sensors (Maybe thats a class aswell?)
			does its AI stuff, calls move to move the bot and calls com to update the laptop
		"""
		#self.move = Move()
		self.com = Com(port = port, host = host)

	def sense(self):

		"""
			This function is a temp function it just takes in input from the user
			The user can send a message to the laptop or update the map (the map right now is
			just a X Y coordination)
			This entire function will be replaced its just for testing
		"""
		points = list()
		for i in range(360/turnAngle):
			movement.turn(turnAngle)
			botAngle = botAngle+turnAngle
			if turnAngle ==0:
				points.insert(0,[sensor.getDistance(),botAngle])
			elif turnAngle == 90:
				points.insert(1,[sensor.getDistance(),botAngle])
			elif turnAngle == 180:
				points.insert(2,[sensor.getDistance(),botAngle])
			elif turnAngle == 270:
				points.insert(3,[sensor.getDistance(),botAngle])
			else:
				points.append([dist,botAngle])
			if turnAngle >= 360:
				turnAngle = turnAngle-360
			if botAngle == 0:
				break
		return points

		#print "Location: " + str(self.move.location)

        '''
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
		elif command == "bot":
			self.com.sendMessage('bot')
			self.com.sendBotLocation((4,4,90))
		else:
			
			while 1:
				data = raw_input("Enter x0,y0,x1,y1: ")
				inp = data.split(",")

				if len(inp) != 4:
					print "Invalid input"
				else:
					m = []
					#test data
					m.append([1,1,1,1,1,1])
					m.append([2,2,2,2,2,2])
					self.com.sendMessage("data")
					self.com.updateMap(m)
					break


		return command
        '''

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
	a = AI(port,ip)

	print "Starting AI"

	room = Map([])
	p = sense()
	room.updateMap(p)
	r = room.getMap()
	for i in r:
		for j in i:
			print j
	a.com.updateMap(room.getMap())
	
'''
	while 1:
		c = a.sense()
		if c == "exit":
			break
'''