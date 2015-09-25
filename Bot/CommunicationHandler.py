#basic layout taken from stackoverflow.com:
#http://stackoverflow.com/questions/3643538/delegates-in-python
#by MattyW

class CommunicationHandler:
	
	def __init__(self,parent = None):
		self.parent = parent

	def displayMes(self,mes):
		
		Handler = 'displayMes_' + mes
		
		if hasattr(self,Handler):
			func = getattr(self,Handler)
			func()
		elif self.parent:
			self.parent.displayMes(mes)

	def drawOnMap(self,data):

		Handler = 'drawOnMap_' + data
		
		if hasattr(self,Handler):
			func = getattr(self,Handler)
			func()
		elif self.parent:
			self.parent.drawOnMap(data)

