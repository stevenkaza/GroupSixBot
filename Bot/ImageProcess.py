import sys

from PIL import Image
import numpy as np
import png
#from Sensor import *

#figure out how to reorganize it for Mitch based on what he wants returned
#add code to determine height of the window, edge detection

class ImageProcess:

	def __init__(self, name = str(sys.argv[1])):

		splitName = name.split('.')
		self.name = splitName[0]
		self.extention = splitName[1]
		self.blackValue = 5
		#self.sensor = Sensor()


	def hasWindow(self,image):
		#im = Image.open(name)
		## code here to detremine that there is a window in this image
		return 0

	def whereWindow(self, name = str(sys.argv[1]), extention = "jpeg"):
		image = Image.open(name)
		image = self.grayScale(image)
		cmAwayFromWall = 30
        #cmAwayFromWall = self.sensor.getDistance()
		windowString = self.searchImageForWindow(image,30,0)
		return windowString
	def grayScale(self,im):

		im=im.convert('L') #makes it greyscale
		y=np.asarray(im.getdata(),dtype=np.float64).reshape((im.size[1],im.size[0]))
		y=np.asarray(y,dtype=np.uint8) #if values still in range 0-255!
		w=Image.fromarray(y,mode='L')
		w.save('grayScaled.jpg')
		w = Image.open('grayScaled.jpg')
		return w
	def process(self):
		if (sys.argv[2]=="where"):
			windowString = self.whereWindow()
		if (sys.argv[2]=="size"):
			windowString = self.getWindowSize(sys.argv[3])
		print windowString
		#result = self.hasWindow(im)
		#converting to grayscale using opencv

	def getWindowSide(self,windowStarts,windowEnds,width):
		#the case where the rest of the window is to the left
		print windowStarts,windowEnds
		if (windowStarts ==0 and windowEnds > 500):
			# figure out a variable for the case where the window never ends
			return "full window"
			#this case is very unlikely
		if (windowStarts < 20 and windowEnds < width and windowStarts != -1):
			return "partialLeft"
		if (windowStarts > 1 and (windowEnds==512 or windowEnds ==0 or windowEnds ==-1)):
			return "partialRight"
		return "complete"
	def isWindowFull(self,windowFound,windowStarts):
			if (windowFound ==1 or (windowFound==2 and windowStarts<10)):
				return 1
			return 0

	def getWindowPos(self,x1,x2,width):
		print x1,x2
		if (x1 > 208 and x1 <313):
			return "middle"
		if (x2 > 208 and x2 < 313):

			return "middle"
		if (x1 >= 0 and( x2 < 313 and x2> 208)):

			return "middle"
		if (x1>=0 and x2<208 and x2!=-1):
			return "left"
		if (x1>311 and x2 <= 510):
			return "right"
		return "none"

	def getWindowSize(self, distance):
		name = str(sys.argv[1])
		image = Image.open(name)
		image = self.grayScale(image)
		PxlsPerCM = float(int(distance)+2)/520
		print PxlsPerCM
		width = image.size[0]
		height = image.size[1]
		windowData = self.searchImageForWindow(image,distance,1)
		windowList = windowData.split("/")
		print windowList
		windowWidthPxl = int(windowList[3]) - int(windowList[2])
		windowWidthCM = PxlsPerCM * windowWidthPxl
		print windowWidthCM

		print windowList

	def initImageForSearching(self,image):
		im = image.load()
		width = image.size[0]
		height = image.size[1]

	def searchImageForWindow(self,image,distance,size):
		#figure this shit out

		if (size == 1):
			blackWhiteBorder = 120
		else:
			blackWhiteBorder = 120
		print "bb = " + str(blackWhiteBorder)
		im = image.load()
		width = image.size[0]
		height = image.size[1]
		yMid = height*0.5
		windowEnds = -1
		windowStarts = -1
		windowFound = 0
		whitePxlCount = 0
		blackPxlCount = 0
		for xPxl in range(0,width):
			print im[xPxl,yMid]
			#searching for black, 150 is the color seperation for black and white pixels
			if im[xPxl,yMid] < blackWhiteBorder:
				#print "pix = " + str(im[xPxl,yMid])
				#print "bb = " + str(blackWhiteBorder)
				#print im[xPxl,yMid]
				blackPxlCount = blackPxlCount + 1
				if (windowFound == 1):
					windowEnds = xPxl
					windowFound = 2
				if (whitePxlCount<=5 and blackPxlCount > 4):
					whitePxlCount = 0
			else:
			#	print im[xPxl,yMid], xPxl
				if (windowFound ==0):
					#Disregarding outliers, must be white pixels for at least 3 before it counts as a window
					whitePxlCount = whitePxlCount + 1
					if (whitePxlCount > 2):
						windowFound=1
						windowStarts = xPxl
		windowSide = ""
		windowString = self.getWindowPos(windowStarts,windowEnds,width)
		if (size ==1):
			if (windowString == "none"):
				return "none"
			windowSide = self.getWindowSide(windowStarts,windowEnds,width)
			return windowString + "/" +  windowSide + "/" + str(windowStarts) + "/" + str(windowEnds)
		return windowString + " " + windowSide

	def middleCheck(self,im):
		'''
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
		windowFound =0
		blackStarts = 0
		rightBlackPxlCount = 0
		windowStarts = 1212
		windowEnds = 0
		#algorithim for average pixel?
		for x in range(0,width):
			if i[x,yMiddleTop] < 120:
#S				print i[x,yMiddleTop]
				if (windowFound==1):
					blackStarts = x
					#only works for one side, need to get edges of entire window
					windowEnds = x
					windowFound = 2
					result = self.getWindowSide(windowStarts,windowEnds,width)
					if (result!= "complete"):
						print result
						return result

				black+=1
			#	print x
				if (x>xMiddleLeft and x<xMiddleRight):
				 	midBlackPxlCount= midBlackPxlCount + 1
				if (x<xMiddleLeft):
					leftBlackPxlCount = leftBlackPxlCount + 1
				if (x>xMiddleRight):
					rightBlackPxlCount =  rightBlackPxlCount + 1
			else:
				white +=1
				#need to change my white and black values
			#	print "white x " + str(x),
				if (windowFound == 0 ):
					windowFound= 1
					windowStarts = x
				if (x>xMiddleLeft and x<xMiddleRight):
				 	midWhitePxlCount= midWhitePxlCount + 1
				if (x<xMiddleLeft):
					leftWhitePxlCount = leftWhitePxlCount + 1
				if (x>xMiddleRight):
					rightWhitePxlCount =  rightWhitePxlCount + 1

		if(self.isWindowFull(windowFound,windowStarts)):
			result = self.getWindowSide(windowStarts,windowEnds,width)
			print result
			return result


		print "window starts = " + str(windowStarts) + " and ends = " + str(windowEnds)

		self.newCheck(windowStarts,windowEnds,width)

		#there is a window that starts and ends
		if (windowStarts>=0 and windowFound == 2):
			result = self.getWindowSide(windowStarts,windowEnds,width)
			return result
		if (black > white and white <20):
			print black, white
			print "no window"
			return
		# if statement here

		if (midWhitePxlCount > midBlackPxlCount):
			print "window in the middle"
			#return 1

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

		# how do we determine black pixels then white, create a state


		print  "middle white count = " + str(midWhitePxlCount) + "\n",
		print  "left white count = " + str(leftWhitePxlCount) + "\n" ,
		print "right white count = " + str(rightWhitePxlCount) + "\n" ,

		print  "middle black count = " + str(midBlackPxlCount)+ "\n" ,
		print  "left black count = " + str(leftBlackPxlCount)+ "\n" ,
		print "right black count = " + str(rightBlackPxlCount)+ "\n" ,
		print "black starts @ = " + str(blackStarts)
		print "window starts @ = " + str(windowStarts)
		print "window ends @ = " + str(windowEnds)


		print 'Argument List:', str(sys.argv[1])

		'''


ip = ImageProcess()
ip.process()
