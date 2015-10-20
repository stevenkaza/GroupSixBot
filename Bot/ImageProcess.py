import sys

from PIL import Image
import numpy as np

class ImageProcess:

	def __init__(self, name = 'testPic.jpeg'):

		splitName = name.split('.')
		self.name = splitName[0]
		self.extention = splitName[1]
		self.blackValue = 5

	def process(self, name = "testPic.jpeg", extention = "jpeg"):

		im = Image.open(name)
		white = 0
		black = 0
		#converting to grayscale using opencv

		im=im.convert('L') #makes it greyscale
		y=np.asarray(im.getdata(),dtype=np.float64).reshape((im.size[1],im.size[0]))
		y=np.asarray(y,dtype=np.uint8) #if values still in range 0-255!
		w=Image.fromarray(y,mode='L')
		w.save('out.jpg')

		'''
		This just test for one colour: Black, anything that isn't black (define as a y value less than 5) is white (for now)


		for i in im.getdata():
			if i[1] < self.blackValue:
				black += 1
			else:
				# we assume white everything that is not black:
				white += 1

		#print im.getcolors()
		print "Size: ",im.size[0],im.size[1],"White: ",white,"Black: ",black
		return {'white':white, 'black' : black}
		'''
ip = ImageProcess()
ip.process()
