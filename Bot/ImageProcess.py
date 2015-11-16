import sys

from PIL import Image
import numpy as np
import png


class ImageProcess:

	def __init__(self, name = str(sys.argv[1])):

		splitName = name.split('.')
		self.name = splitName[0]
		self.extention = splitName[1]
		self.blackValue = 5

	def hasWindow(self,image):
		#im = Image.open(name)
		## code here to detremine that there is a window in this image
		return 0

	def grayScale(self,im):

		im=im.convert('L') #makes it greyscale
		y=np.asarray(im.getdata(),dtype=np.float64).reshape((im.size[1],im.size[0]))
		y=np.asarray(y,dtype=np.uint8) #if values still in range 0-255!
		w=Image.fromarray(y,mode='L')
		w.save('grayScaled.jpg')
		w = Image.open('grayScaled.jpg')
		return w
	def process(self, name = str(sys.argv[1]), extention = "jpeg"):

		im = Image.open(name)
		white = 0
		black = 0
		xMiddleLeft = 0
		xMiddleRight =0
		yMiddleBottom = 0
		yMiddleTop = 0
		im = self.grayScale(im)

		result = self.hasWindow(im)
		self.middleCheck(im)
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
				if (x < xMiddleLeft):
				# lets also make sure there are no white pixles in the right side of the image
					leftCount = leftcount + 1
				if (x > xMiddleRight): # if we have white right pixels too, then our left count is invalid s
					leftCount = leftCount  - 1

		if middleCount >= (xMiddleRight-xMiddleLeft-2):
			print "window in the middle"
	#	elif


		#print im.getcolors()
		print "Size: ",im.size[0],im.size[1],"White: ",white,"Black: ",black
		return {'white':white, 'black' : black}
'''
	def middleCheck(self,im):
	#	im = im.load()
		white = 0
		black = 0
		i = im.load()
		width  = im.size[0]
		height = im.size[1]
		# getting the middle points for x
		xMiddleLeft = int(width*0.4)
		xMiddleRight = int(width*0.6)
		yMiddleTop = int(height*0.6)
		yMiddleBottom = int(height*0.4)



		print width, height, xMiddleLeft,xMiddleRight

		midWhitePxlCount = 0
		leftWhitePxlCount = 0
		rightWhitePxlCount = 0
		status =0
		midBlackPxlCount = 0
		leftBlackPxlCount = 0
		rightBlackPxlCount = 0
		for x in range(0,width):

			if i[x,yMiddleTop] < 100:
				#print i[x,yMiddleTop]
				black+=1
				if (x>xMiddleLeft and x<xMiddleRight):
				 	midBlackPxlCount= midBlackPxlCount + 1
				if (x<xMiddleLeft):
					leftBlackPxlCount = leftBlackPxlCount + 1
				if (x>xMiddleRight):
					rightBlackPxlCount =  rightBlackPxlCount + 1
			else:
				white +=1
				if (x>xMiddleLeft and x<xMiddleRight):
				 	midWhitePxlCount= midWhitePxlCount + 1
				if (x<xMiddleLeft):
					leftWhitePxlCount = leftWhitePxlCount + 1
				if (x>xMiddleRight):
					rightWhitePxlCount =  rightWhitePxlCount + 1

		if (black > white and white <20):
			print "no window"
			return
		if (midWhitePxlCount>40):
			print "in the middle"
			return
		if (leftWhitePxlCount > leftBlackPxlCount):
			print "window to the left"
			status = status +1
		if (rightWhitePxlCount > rightBlackPxlCount and rightBlackPxlCount < 80):
			print "window to the right"
			status = status +1

		if (rightWhitePxlCount > rightBlackPxlCount	 and midBlackPxlCount < 15 and rightBlackPxlCount < 30):
			print "Window to the right \n\n"
			status = status +1
		elif (leftWhitePxlCount > leftBlackPxlCount and midBlackPxlCount < 15):
			print "Window to the left \n\n"
			status = status + 1

		if (midBlackPxlCount < 15):
			if (rightBlackPxlCount > rightWhitePxlCount or leftBlackPxlCount > leftWhitePxlCount):
				if (status<2):
					print "Window in the middle \n\n"


		print  "middle white count = " + str(midWhitePxlCount) + "\n",
		print  "left white count = " + str(leftWhitePxlCount) + "\n" ,
		print "right white count = " + str(rightWhitePxlCount) + "\n" ,

		print  "middle black count = " + str(midBlackPxlCount)+ "\n" ,
		print  "left black count = " + str(leftBlackPxlCount)+ "\n" ,
		print "right black count = " + str(rightBlackPxlCount)+ "\n" ,
		print 'Argument List:', str(sys.argv[1])


		def middleSearch(self,im,xMiddleLeft,xMiddleRight,xMiddle):
			for x in range(0,width):

				'''
	for x in range(0,width):

			#	print i[x,100]
				if i[x,yMiddle] < 20:
					black +=1
				else:
					white +=
'''


ip = ImageProcess()
ip.process()
