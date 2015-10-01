from discovery_bot import Ultrasound
from picamera import PiCamera

class Sensor:
	def __init__(self):
		self.us = Ultrasound()
		self.camera = PiCamera()
		self.camera.hflip = True
		self.camera.vflip = True

	def takePicture(self):

		return self.camera.capture("testPic","jpeg")

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

if __name__ == "__main__":

	s = Sensor()
	raw_input("Start")
	s.takePicture()


