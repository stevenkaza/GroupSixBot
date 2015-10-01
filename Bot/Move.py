from discovery_bot import pins
from discovery_bot import Movement
from discovery_bot import Ultrasound
from servo import Servo
import time
import datetime


class Move:
	TOO_CLOSE  = "Too Close";

	def __init__(self, start = (0,0),leftSpeed = 100, rightSpeed = 100):
		self.location = start
		self.x = start[0]
		self.y = start[1]

		self.leftSpeed = leftSpeed
		self.right = rightSpeed

		self.left = Servo(pins.SERVO_LEFT_MOTOR)
		self.right = Servo(pins.SERVO_RIGHT_MOTOR)

		self.us = Ultrasound()
		self.movement = Movement()

	def checkBoundary(self,cmSent):
		# situation 1
		# we send something and we find out that the robot is going to hit the wall if it continues, meaning the distance is greater
		#than the closest thing away, that the worst possible thing, so lets check for that first.

		#if the desired distance is greater or equal to the distance away from the closest obstacle
		cmAwayFromWall = self.us.read_normalized()
		if (cmSent >  cmAwayFromWall):
			return "STOP"
		elif (cmSent > (cmAwayFromWall - 10)):
			return "STOP"
		elif (cmSent < (cmAwayFromWall - 10)):
			return "GOOD"

	 def normalize(self, val):
		scale = 0.5 / 100
		speed = val * scale

		if val >= 0:
			speed += 0.5

		return speed

	def forward(self, speed = 100):
		self.left.set_normalized(self.normalize(self.leftSpeed))
		self.right.set_normalized(self.normalize(-self.rightSpeed))

	def move(self,distance):
		status = True
		result = self.checkBoundary(distance)
		cmAwayFromWall = self.us.read_normalized()
		if (result == "STOP"):

			distanceMoved = 0
			self.movement.stop()
			return distanceMoved
		elif (result =="GOOD"):
			print "should be here"
			self.forward(100)
			time.sleep(distance/12)
		#	return status
		#account for the 5 degrees a second/ every 12 cm of curvature to the left
		distanceMoved = cmAwayFromWall - self.us.read_normalized()
		#anglesToTurn = (distance/12) * 5
		#spinTime = anglesToTurn*0.0053763408602 # degrees per second
		# telling the robot to spin back since it turns left on its own
		#self.timedSpin(spinTime,'right')
		self.movement.stop()
		return distanceMoved

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

bot = Move(leftSpeed = 100, rightSpeed = 35)
s = ""
while(s !='s'):
	s = raw_input()
	if (s!='s'):
		print "distance away from closest: "
		print bot.us.read_normalized()
		print bot.move(float(s))
bot.movement.stop()
