import sys

from PIL import Image
import numpy as np
import png


class ImageProcess:

	def __init__(self, name = 'testPic.jpeg'):

		splitName = name.split('.')
		self.name = splitName[0]
		self.extention = splitName[1]
		self.blackValue = 5
	def grayScale(self,im):

		im=im.convert('L') #makes it greyscale
		y=np.asarray(im.getdata(),dtype=np.float64).reshape((im.size[1],im.size[0]))
		y=np.asarray(y,dtype=np.uint8) #if values still in range 0-255!
		w=Image.fromarray(y,mode='L')
		w.save('grayScaled.jpg')
	def process(self, name = "testPic.jpeg", extention = "jpeg"):

		im = Image.open(name)
		white = 0
		black = 0
		xMiddleLeft = 0
		xMiddleRight =0
		yMiddleBottom = 0
		yMiddleTop = 0
		self.grayScale(im)
		#converting to grayscale using opencv


		im = Image.open('grayScaled.jpg')
		i = im.load()
		width  = im.size[0]
		height = im.size[1]
		# getting the middle points for x
		xMiddleLeft = int(width*0.4)
		xMiddleRight = int(width*0.6)
		yMiddleTop = int(height*0.6)
		yMiddleBottom = int(height*0.4)
		yMiddle = int(height*0.5)


		print im.size[0]
		print im.size[1]

		#This just test for one colour: Black, anything that isn't black (define as a y value less than 5) is white (for now)
		self.middleSearch(i,xMiddleRight,xMiddleLeft)
		middleCount =0
		leftCount = 0
		'''
		for x in range(0,width):
		#	print i[x,100]
			if i[x,yMiddle] < 20:
				black +=1
			else:
				# we assume white everything that is not black:
				white += 1
			#we know we are in the middle here, and if the pixels in the middle are white, the window is in the middle
				#middle window check
				if (x > xMiddleLeft) and (x<xMiddleRight):
					middleCount = middleCount +1
				#checking left side for window
				if (x < xMiddleLeft)
				# lets also make sure there are no white pixles in the right side of the image
					leftCount = leftcount + 1
				if (x > xMiddleRight) # if we have white right pixels too, then our left count is invalid s
					leftCount = leftCount  - 1

		if middleCount >= (xMiddleRight-xMiddleLeft-2):
			print "window in the middle"
		elif


		#print im.getcolors()
		print "Size: ",im.size[0],im.size[1],"White: ",white,"Black: ",black
		return {'white':white, 'black' : black}
'''
		def middleSearch(self,im,xMiddleLeft,xMiddleRight,xMiddle):
		'''	for x in range(0,width):
			#	print i[x,100]
				if i[x,yMiddle] < 20:
					black +=1
				else:
					white +=
'''


ip = ImageProcess()
ip.process()
