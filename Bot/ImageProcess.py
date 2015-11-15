import sys

from PIL import Image
import numpy as np
import png


class ImageProcess:

	def __init__(self, name = 'pic0.jpeg'):

		splitName = name.split('.')
		self.name = splitName[0]
		self.extention = splitName[1]
		self.blackValue = 5
	def hasWindow(self,name = "grayScaled.jpeg"):
		im = Image.open(name)
		## code here to detremine that there is a window in this image 
	def grayScale(self,im):

		im=im.convert('L') #makes it greyscale
		y=np.asarray(im.getdata(),dtype=np.float64).reshape((im.size[1],im.size[0]))
		y=np.asarray(y,dtype=np.uint8) #if values still in range 0-255!
		w=Image.fromarray(y,mode='L')
		w.save('grayScaled.jpg')
	def process(self, name = "pic0.jpeg", extention = "jpeg"):

		im = Image.open(name)
		white = 0
		black = 0
		xMiddleLeft = 0
		xMiddleRight =0
		yMiddleBottom = 0
		yMiddleTop = 0
		self.grayScale(im)
		#converting to grayscale using opencv


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


		def middleSearch(self,im,xMiddleLeft,xMiddleRight,xMiddle):
			for x in range(0,width)

		def middleSearch(self,im,xMiddleLeft,xMiddleRight,xMiddle):
		for x in range(0,width):

			#	print i[x,100]
				if i[x,yMiddle] < 20:
					black +=1
				else:
					white +=
'''


ip = ImageProcess()
ip.process()
