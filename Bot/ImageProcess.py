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

		if (windowStarts>=0 and windowEnds <= 256):
			return "completeLeft"
		if (windowStarts>=256 and windowEnds <=512):
			return "completeRight"
	def isWindowFull(self,windowFound,windowStarts):
			if (windowFound ==1 or (windowFound==2 and windowStarts<10)):
				return 1
			return 0

	def getApproxWindow(self,x1,x2,width):
		print x1,x2
		if (x1 > 208 and x1 <313):
			return "middle"
		if (x2 > 208 and x2 < 313):

			return "middle"
		if (x1 >= 0 and( x2 < 313 or x2 > 208) and x2!= -1):

			return "middle"
		if (x1>=0 and x2<208 and x2!=-1):
			return "left"
		if (x1>311 and x2 <= 510):
			return "right"

		return "none"

	def getWindowSize(self, distance):
		name = str(sys.argv[1])
		image = Image.open(name)
		returnString = ""
		image = self.grayScale(image)
		PxlsPerCM = float(int(distance)+2)/512
		print PxlsPerCM
		width = image.size[0]
		height = image.size[1]
		closestEdgeToMid = 0
		windowData = self.searchImageForWindow(image,distance,1)
		if windowData == "partialLeft" or windowData == "partialRight":
			print "partial here"
			return windowData
		#middle case
		if '%' in windowData:
			print"wfsdf"
			windowList = windowData.split("%")
			leftEdgeToMidInCM = str(float(int(windowList[0]) * PxlsPerCM))
			RightEdgeToMidInCM = str(float(int(windowList[1]) * PxlsPerCM))
			return "{" +"M" +"," + leftEdgeToMidInCM + "," + RightEdgeToMidInCM + "}"
		#complete left, complete right
		if '/' in windowData:
			returnString = ""

			windowList = windowData.split("/")
			print windowList
			windowWidthPxl = int(windowList[3]) - int(windowList[2])
			print windowWidthPxl
			windowWidthCM = PxlsPerCM * windowWidthPxl
			print int(windowList[1])
			closestEdgeToMid = int(windowList[1]) * PxlsPerCM
			returnString = "{" + windowList[0] + "," + str(closestEdgeToMid) + "," + str(windowWidthCM) + "}"
			print returnString
			return returnString
			print windowWidthCM

			print windowList

	def initImageForSearching(self,image):
		im = image.load()
		width = image.size[0]
		height = image.size[1]
	def calcDisClosestEdgeToMid(self,x1,x2):
		if (x2 < 256 and x1 >=0 and x2 <=256):
			print "left here" , x2
			return 256 - x2
		if (x1 > 256 and x2 < 513):
			return x1 - 256

	def calcDisEachEdgeToMid(self,x1,x2):
		if (x1>=0 and x2 >=256):
			#returning left edge to mid and
			return str(256 - x1) + "%" + str(x2-256)
		return -1





	def searchImageForWindow(self,image,distance,size):
		#figure this shit out
		# different lighting based on how far away robot is
		if (size > 15):
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
		minEdgeList =""
		for xPxl in range(0,width):
			#searching for black, 150 is the color seperation for black and white pixels
			if im[xPxl,yMid] < blackWhiteBorder:
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
		windowString = self.getApproxWindow(windowStarts,windowEnds,width)
		if (size==0):
			return windowString
		#if we are doing the second function
		if (size ==1):
			print "test",windowString
			if (windowString == "none"):
				return "none"
			midEdgeList = self.calcDisEachEdgeToMid(windowStarts,windowEnds)
			windowSide = self.getWindowSide(windowStarts,windowEnds,width)

			if midEdgeList == -1: #not direct middle
					#complete window, not in direct middle
				if (windowSide=="partialLeft" or windowSide =="partialRight"):
					return windowSide
				closestEdgeCM = self.calcDisClosestEdgeToMid(windowStarts,windowEnds)
				if (windowSide == "completeLeft"):
					return "L" + "/" + str(closestEdgeCM) + "/" + str(windowStarts) + "/" + str(windowEnds)
				elif (windowSide == "completeRight"):
					return "R" + "/" + str(closestEdgeCM) + "/" + str(windowStarts) + "/" + str(windowEnds)
			#direct middle
			else:
				return midEdgeList
				#return str(windowSide) + "," + str(minEdgeList) + "," + str(windowStarts) + "," + str(windowEnds)

				#	return windowString + "/" +  windowSide + "/" + str(windowStarts) + "/" + str(windowEnds)
				#Direct middle

	#	return windowString + " " + windowSide

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
