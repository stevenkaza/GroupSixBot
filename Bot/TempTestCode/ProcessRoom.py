from os import listdir
from os.path import isfile, join

class ProcessRoom:

	def findAdjustedNums(self, room):

		length =len(room)
		width = len(room[0])
		top = 0
		foundTop = False
		foundLeft = False
		rowNum = 0
		bottom = 0
		bottomTotal = 0
		right = 0
		rightTotal = 0
		left = 0

		for x in range(width):
			for y in range(length):
		
				if room[y][x] == 1:
					if not foundTop:
						top += y
						foundTop = True
					bottom = y
					right = x
			
			rightTotal+=right
			bottomTotal += bottom
			foundTop = False

		rightTotal = 0

		for y in range(length):
			for x in range(width):
				if room[y][x] == 1:
					if not foundLeft:
						left += x
						foundLeft = True
					right = x
			rightTotal+=right

			foundLeft = False


		print ""
		leftNum = int(round(float(left)/float(length)))
		rightNum =  int(round(float(rightTotal)/float(length)))
		botNum = int(round(float(bottomTotal)/float(width)))
		topNum = int(round(float(top)/float(width)))

		return (topNum,botNum,leftNum,rightNum)

	def fixRoom(self, y, x, newNums, oldRoom):
		
		room = []

		top = newNums[0]
		bottom = newNums[1]
		left = newNums[2]
		right = newNums[3]
		
		print newNums

		for i in range(y):
			line = []
			for j in range(x):

				if (i == top and (j >= left and j < right)) or (i == bottom and (j >= left and j< right)) or (j == left and (i >= top and i <= bottom)) or (j == right and (i >= top and i <= bottom)):
					line.append(1)
				elif oldRoom[i][j] == 2:
					line.append(2)
				else:
					line.append(0)

			room.append(line)

		return room

	#all rooms must be saved in the directory 'rooms' with the name
	#convention 'room_#' ie "room_6" 
	def saveFile(self, fileName = "newRoom", room = []):

		f = open(fileName,"w")

		for i in room:
			for j in i:
				f.write(str(j))
			f.write("\n")

		f.close()

	def openFile(self, fileName = "room_1"):

		f = open(fileName, "r")

		room = []

		for i in f:
			line = []
			for j in i:
				if j != '\n':
					line.append(int(j))
			room.append(line)

		return room

	def flip(self, room):

		length = len(room)
		width = len(room[0])

		newRoom = []

		for i in range(width - 1,-1,-1):
			line = []
			for j in range(length):
				line.append(room[j][i])
			newRoom.append(line)

		return newRoom

	def flip2(self, room):

		length = len(room)
		width = len(room[0])

		newRoom = []

		for i in range(width ):
			line = []
			for j in range(length- 1,-1,-1):
				line.append(room[j][i])
			newRoom.append(line)

		return newRoom

	def checkInside(self, one, two):

		for i in range(len(one)):
			for j in range(len(one[0])):
				if one[i][j] != two[i][j]:
					return False

		return True

	def sameRoom(self, one, two):

		oneY = len(one)
		oneX = len(one[0])

		twoY = len(two)
		twoX = len(two[0])

		offY = int(round(float(oneY) * 0.10 )) #rooms can be off by 10% in size
		offX = int(round(float(oneX) * 0.10 ))


		if ((oneY <= twoY + offY) and (oneY >= twoY - offY)) and ((oneX <= twoX + offX) and (oneX >= twoX - offX)):
			#return self.checkInside(one, two)
			return True


		if ((oneY <= twoX + offY) and (oneY >= twoX - offY)) and ((oneX <= twoY + offX) and (oneX >= twoY - offX)):
			return True
			'''
			if not self.checkInside(one,sel.flip(two)):
				return self.checkInside(one,self.flip2(two))
			return True
			'''

		return False

if __name__ == "__main__":

	mypath = "./rooms"
	onlyfiles = [ f for f in listdir(mypath) if isfile(join(mypath,f)) ]

	pr = ProcessRoom()

	room = pr.openFile("./rooms/room_2")

	for i in onlyfiles:
		r = pr.openFile(mypath+'/'+i)
		if pr.sameRoom(room,r):
			print "Same! rooms2 ",i


	'''
	room = openFile("room1")

	newNums = findAdjustedNums(room)

	newRoom = fixRoom(len(room),len(room[0]),newNums,room)

	flippedRoom = flip2(newRoom)

	print sameRoom(newRoom,room)

	saveFile("newRoom.txt",flippedRoom)

	'''
