from discovery_bot import Ultrasound
from picamera import PiCamera
from ImageProcess import *
import subprocess, signal
import os
import shlex
import serial

class Sensor:

	def __init__(self):

		self.us = Ultrasound()

		try:
			p = subprocess.Popen(['pidof','raspberry_pi_camera_streamer'], stdout=subprocess.PIPE)
			out,err = p.communicate()
			pid = int(out.strip('\n'))
			os.kill(pid,signal.SIGKILL)
			try:
				self.camera = PiCamera(resolution = (512,320))
				self.camera.hflip = True
				self.camera.vflip = True
			except:
				pass
			print "Camera killed"
		except:
			print "Camera already dead"

		#need to fix this
		try:
			self.ser = serial.Serial(port = '/dev/ttyUSB0',baudrate = 9600,timeout = 1)
		except Exception as e:
			print e
			self.ser = serial.Serial(port = '/dev/ttyUSB1',baudrate = 9600,timeout = 1)



		
		self.angle = 0
		self.top = 0
		self.bottom = 0
		self.right = 0
		self.left = 0

	def takePicture(self, name = "testPic", extention = "jpeg"):

		self.camera.capture(name, extention)
		print self.camera.resolution

	def removeOutLiers(self, listS):

		low = 100
		high = 0

		for i in listS:
			if i < low:
				low = i
			elif i > high:
				high = i

		listS.remove(low)
		listS.remove(high)

		return listS

	def getSensor(self, side = 'r'):

		self.ser.flushInput()
		self.ser.write(side)
		dist = self.ser.readline(),

		return dist


	def getDistance(self):

		listSense = []

		for i in range(10):
			listSense.append(self.us.read_normalized())

		listSense = self.removeOutLiers(listSense)

		dist = float(sum(listSense))/float(len(listSense))

		if self.angle == 0:
			self.top = dist
		if self.angle == 90:
			self.right = dist
		if self.angle == 180:
			self.bottom = dist
		if self.angle == 270:
			self.left = dist

		self.angle += 15

		return dist

	def isWall(self, colours={'white':1,'black' :1}):
		'''
		colours dictionary of colours in a picture.
		returns odds of the picture being a Wall
		'''
		black = float(colours['black'])

		if black == 0.0:
			return 0

		others = float(sum(v for k,v in colours.iteritems() if k != 'black'))

		if others == 0.0:
			return 100 #only black in the picture

		print black,others

		return black/(others + black)

	def makeBox(self):

		length = int(self.top + self.bottom)
		width = int(self.left + self.right)

		room = []

		for i in range(length):
			line = []
			for j in range(width):
				if (i == 0 or j == 0) or (i == length - 1) or (j == width - 1):
					line.append(1)
				else:
					line.append(0)

			room.append(line)

		room[int(self.top)][int(self.left)] = 8

		return room

if __name__ == "__main__":

	s = Sensor()
	i = ImageProcess('black1.jpeg')
	inp = raw_input("Start: ")

	count = 0

	while inp != 's':
		inp = raw_input("Take picture or (s)top: ")
		if inp == 's':
			break
		s.takePicture("pic" + str(count))
		count += 1
