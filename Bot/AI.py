from Move import *
from Sensor import *
from Com import *
import time
import sys
import json
from Map import *

MAXVIEW = 90

class AI:
	room = Map([])
	movement = Move()
	sensor = Sensor()
	botAngle = 0
	botPos = [0,0]
    
	turnAngle  = 15 # the angle the bot will turn to sense
	'''
	def mapRoom(self):
		if 
		
		while not room.isMapped():
			sense()
			route = room.nextRoute()
			for i in route:
				break
			break
		return
	'''
	def __init__(self, port = 13000, host = "localhost"):
		"""
			This function has two objects right now
			move will control the movement of the pibot
			com controls the communication.
			Basically the AI gets information from the sensors (Maybe thats a class aswell?)
			does its AI stuff, calls move to move the bot and calls com to update the laptop
		"""
		self.move = Move()
		self.room = Map([[0,0]])
		self.com = Com(port = port, host = host)
	def sense(self):
		"""
			This function is a temp function it just takes in input from the user
			The user can send a message to the laptop or update the map (the map right now is
			just a X Y coordination)
			This entire function will be replaced its just for testing
		"""
		points = list()
		for i in range(360/self.turnAngle):
			if self.botAngle ==0:
				points.insert(0,[self.sensor.getDistance(),self.botAngle])
			elif self.botAngle == 90:
				points.insert(1,[self.sensor.getDistance(),self.botAngle])
			elif self.botAngle == 180:
				points.insert(2,[self.sensor.getDistance(),self.botAngle])
			elif self.botAngle == 270:
				points.insert(3,[self.sensor.getDistance(),self.botAngle])
			else:
				points.append([self.sensor.getDistance(),self.botAngle])
			self.movement.turn(self.turnAngle)
			self.botAngle = self.botAngle+self.turnAngle
			time.sleep(1)
			if self.botAngle >= 360:
				self.botAngle = self.botAngle-360
				#self.movement.turn(self.turnAngle)
				#self.botAngle = self.botAngle+self.turnAngle
			
				#break
			#if self.botAngle == 0:
			#	break
		return points

	def mapRoom90(self):
		self.turnAngle = 90
		while(not self.room.isMapped()):
			points = self.sense()
			self.botPos = self.room.updateMap(points)
			self.room.fillMap90()
			nextDir = self.room.nextRoute90()
			if nextDir=="U":
				if self.botAngle!=0:
					self.movement.turn(360-self.botAngle)
					self.botAngle=0
				self.movement.move(MAXVIEW-20)
				self.botPos[0]=self.botPos[0]-MAXVIEW+20
				self.room.updatePos(self.botPos)
			elif nextDir=="D":
				if self.botAngle!=180:
					self.movement.turn(180-self.botAngle)
					self.botAngle=180
				self.movement.move(MAXVIEW-20)
				self.botPos[0]=self.botPos[0]+MAXVIEW-20###################
				self.room.updatePos(self.botPos)
			elif nextDir=="R":
				if self.botAngle!=90:
					self.movement.turn(90-self.botAngle)
					self.botAngle=90
				self.movement.move(MAXVIEW-20)
				self.botPos[1]=self.botPos[1]+MAXVIEW-20###################
				self.room.updatePos(self.botPos)
			elif nextDir=="L":
				if self.botAngle!=270:
					self.movement.turn(270-self.botAngle)
					self.botAngle=270
				self.movement.move(MAXVIEW-20)
				self.botPos[1]=self.botPos[1]-MAXVIEW+20###################
				self.room.updatePos(self.botPos)
			elif nextDir == None:
				self.room.showRoom()
				self.com.sendMessage("data")
				time.sleep(1)
				u=0
				d=0
				l=0
				r=0
				m = self.room.getMap()
				for i in range(len(m)):
					if m[i][self.botPos[1]]==1 and i<self.botPos[0]:
						u=i
						break
				for i in range(len(m)):
					if m[i][self.botPos[1]]==1 and i>self.botPos[0]:
						d=i
						break
				for i in range(len(m[0])):
					if m[self.botPos[0]][i]==1 and i<self.botPos[1]:
						l = i
						break
				for i in range(len(m[0])):
					if m[self.botPos[0]][i]==1 and i>self.botPos[1]:
						r = i
						break
				print u,d,l,r
				self.com.updateMap((l,r,u,d))
				#self.com.updateMap(self.room.getMap())
				time.sleep(5)
				self.com.sendMessage("bot")
				time.sleep(1)
				self.com.sendBotLocation((self.botPos[0],self.botPos[1],self.botAngle))
				time.sleep(1)
				self.com.sendMessage("mes")
				time.sleep(1)
				self.com.sendMessage("Mapping Complete!")
				break
				#complete
			'''
			self.com.sendMessage("data")
			time.sleep(1)
			self.com.updateMap(self.room.getMap())
			time.sleep(5)
			self.com.sendMessage("bot")
			time.sleep(1)
			self.com.sendBotLocation((self.botPos[0],self.botPos[1],self.botAngle))
			time.sleep(1)
			'''
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

	raw_input("press the 'any' key")
	
	a.mapRoom90()
	
	
	#room = Map([0,0])
	
	'''
	p = a.sense()
	print p
	room.updateMap(p)
	r = room.getMap()
	for i in r:
		print i
	'''
	#a.com.updateMap(room.getMap())
	
'''
	while 1:
		c = a.sense()
		if c == "exit":
			break
'''

#move.move(dist)