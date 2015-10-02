import sys

from PIL import Image

class ImageProcess:

	def __init__(self, name = 'testPic.jpeg'):

		splitName = name.split('.')
		self.name = splitName[0]
		self.extention = splitName[1]
		self.blackValue = 5

	def process(self, name = "testPic", extention = "jpeg"):

		im = Image.open(name)
		white = 0
		black = 0

		'''
		This just test for one colour: Black, anything that isn't black (define as a y value less than 5) is white (for now)

		'''
		
		for i in im.getdata():
			if i[1] < self.blackValue:
				black += 1
			else:
				# we assume white everything that is not black:
				white += 1

		#print im.getcolors()
		print "Size: ",im.size[0],im.size[1],"White: ",white,"Black: ",black
		return {'white':white, 'black' : black}