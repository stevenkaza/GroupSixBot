from Move import *
from Com import *

class AI:

	def __init__(self):
		"""
			This function has two objects right now
			move will control the movement of the pibot
			com controls the communication.
			Basically the AI gets information from the sensors (Maybe thats a class aswell?)
			does its AI stuff, calls move to move the bot and calls com to update the laptop
		"""
		self.move = Move()
		self.com = Com()

	def sense(self):

		"""
			This function is a temp function it just takes in input from the user
			The user can send a message to the laptop or update the map (the map right now is
			just a X Y coordination)
			This entire function will be replaced its just for testing
		"""

		print "Location: " + str(self.move.location)

		command = raw_input("mes or data?: ")

		if command == "mes":
			mes = raw_input("Whats your message: ")
			if mes == "exit":
				self.com.sendMessage(mes)
				self.com.end()
				return mes
			else:
				self.com.sendMessage(mes)
		else:
			
			while 1:
				data = raw_input("Enter x,y: ")
				inp = data.split(",")

				if len(inp) != 2:
					print "Invalid input"
				else:
					self.move.move(int(inp[0]),int(inp[1]))
					self.com.updateMap("draw")
					break


		return command


if __name__ == "__main__":

	a = AI()

	print "Starting AI"

	while 1:
		c = a.sense()
		if c == "exit":
			break
