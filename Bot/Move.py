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

	def turn(self,angle):
		# 90 degrees of rotation comes to approx 0.66 seconds, 2 seconds = 270* of rotation on a smooth surface
		if (angle == 'left' or angle == -90 or angle == 270):
				t_end = time.time() + 0.6666
				while time.time() < t_end:
					self.movement.rotate_left();
				self.movement.stop()
		elif (angle == 'right' or angle == 90 or angle == -270):
				t_end = time.time() + 0.6666
				while time.time() < t_end:
					self.movement.rotate_right();
				self.movement.stop()
		elif (angle == 'around' or angle ==180):
				t_end = time.time() + 1.3333
				while time.time() < t_end:
					self.movement.rotate_right();
				self.movement.stop()
		elif (angle == 360 or angle == 'fullspin'):
				t_end = time.time() + 2.66666
				while time.time() < t_end:
					self.movement.rotate_right();
				self.movement.stop()
bot = Move()
s = raw_input()
if (s =='s'):
	exit()
bot.turn(s)
