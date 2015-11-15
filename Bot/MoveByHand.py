
class MoveByHand:

	TOO_CLOSE  = "Too Close";

	def __init__(self, start = (0,0),leftSpeed = 100, rightSpeed = 55, dps = 14.6):
		
		self.location = start
		self.leftSpeed = leftSpeed
		self.rightSpeed = rightSpeed
		self.distancePerSecond = dps

	def turn(self, angle):

		print "Turn bot ",angle, " degrees"
		s = raw_input("Press enter after bot is turned")

	def move(self, distance):

		print "Move bot ",distance, " forward"
		s = raw_input("Press enter after bot is moved")

		return distance

	def scanHallway(self):
		print "Move bot down the hallway"
		s = raw_input("Press enter when done: ")
		dis = raw_input("How far did it move (in cms): ")

		return float(dist)

	def findDoor(self, side = 'r', distance = 10):

		print ("Side: ", side, " Distance: ", distance)

		print "Please move bot until is reaches a door"

		dis = raw_input("How far did it move (in cms): ")

		return float(dis)

if __name__ == "__main__":

	bot = MoveByHand()

	bot.turn(15)

	print bot.move(15)