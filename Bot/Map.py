import json

class Map:

	def __init__(self, points = (0,0,100,100)):
		if type(points) == tuple:
			self.points = points
		else:
			self.points = tuple(points["points"])


if __name__ == "__main__":

	m = Map((0,0,55,55))
	print m

	jd = json.dumps(vars(m))

	c = json.loads(jd)

	nm = Map(c)

	print nm.points