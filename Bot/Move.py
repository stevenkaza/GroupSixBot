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
		self.movement = Movement()

	def move(self, x ,y):
		self.y += y
		self.x += x

		self.location = (self.x,self.y)

	def timedSpin(self,spinTime,direction):
			while time.time() < spinTime:
				if (direction == 'left'):
					self.movement.rotate_left();
				elif (direction == 'right'):
					self.movement.rotate_right()
			self.movement.stop()

	def turn(self,angle):
		# 90 degrees of rotation comes to approx 0.66 seconds, 2 seconds = 270* of rotation on a smooth surface
		angle = float(angle)
		timeToSpin = angle*0.00740740741
		spinTime = time.time() + timeToSpin
		if (angle == 'left' or angle == -90 or angle == 270):
			self.timedSpin(spinTime,'left')
		elif (angle == 'right' or angle == 90 or angle == -270):
			self.timedSpin(spinTime,'right')
		elif (angle == 'around' or angle ==180):
			self.timedSpin(spinTime,'right')
		elif (angle == 360 or angle == 'fullspin'):
			self.timedSpin(spinTime,'right')
		elif (angle > 0):
			self.timedSpin(spinTime,'right')
		else:
			self.timedSpin(spinTime,'left')



bot = Move()
s = raw_input()
if (s =='s'):
	exit()
bot.turn(s)
