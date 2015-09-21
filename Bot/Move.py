class Move:

	def __init__(self, start = (0,0)):
		self.location = start
		self.x = start[0]
		self.y = start[1]

	def move(self, x ,y):
		self.y += y
		self.x += x

		self.location = (self.x,self.y)