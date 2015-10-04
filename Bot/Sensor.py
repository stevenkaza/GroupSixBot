from discovery_bot import Ultrasound
from picamera import PiCamera
from ImageProcess import *

class Sensor:
	def __init__(self):

		self.us = Ultrasound()
	#	self.camera = PiCamera(resolution = (512,320))
	#	self.camera.hflip = True
	#	self.camera.vflip = True

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

	def getDistance(self):

		listSense = []

		for i in range(10):
			listSense.append(self.us.read_normalized())

		listSense = self.removeOutLiers(listSense)
		return float(sum(listSense))/float(len(listSense))

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




if __name__ == "__main__":

	s = Sensor()
	i = ImageProcess('black1.jpeg')
	raw_input("Start")
	s.takePicture(i.name, i.extention)
	print s.isWall(i.process(i.name, i.extention))
