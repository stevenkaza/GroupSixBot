import json

class Map:

	def __init__(self, points = (0,0,100,100)):
		self.points = points

	def to_JSON(self):

		return json.dumps(self,default=lambda o: o.__tuple__)