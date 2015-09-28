from discovery_bot import pins
from discovery_bot import Movement
from discovery_bot import Ultrasound
import time
import datetime


class Move:

	def __init__(self, start = (0,0)):
		self.location = start
		self.x = start[0]
		self.y = start[1]

		self.us = Ultrasound()
		self.movement = Movement()

	def checkBoundary(self,distance):
		if (self.us.read_normalized() - distance >= 10):
			return True
		return False


	def move(self,distance):
		status = True
		if (self.checkBoundary(distance)):
			if (distance>0):
				self.movement.forward(100)
			else:
				self.movement.backward(100)
			distance = abs(distance)
			time.sleep(distance/12)
		else:
			status = False
		self.movement.stop()
		return status

	def timedSpin(self,spinTime,direction):
			if (direction == 'left'):
				self.movement.rotate_left();
			elif (direction == 'right'):
				self.movement.rotate_right()
			time.sleep(spinTime)
			self.movement.stop()

	def turn(self,angle):
		# 90 degrees of rotation comes to approx 0.66 seconds, 2 seconds = 270* of rotation on a smooth surface
		angle = float(angle)
		if (angle >0):
			direction = 'right'
		else:
			direction = 'left'
		angle = abs(angle)
		spinTime = angle*0.0053763408602 # degrees per second
		self.timedSpin(spinTime,direction)
bot = Move()
s = ""
while(s !='s'):
	s = raw_input()
	if (s!='s'):
		bot.move(float(s))
bot.movement.stop()
