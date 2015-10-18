
		points = list()
		for i in range(360/self.turnAngle):
            # lets keep track of the points that we get
			if self.botAngle ==0:
				points.insert(0,[self.sensor.getDistance(),self.botAngle])
                distnace from0Degrees = self.sensor.getDistance
			elif self.botAngle == 90:
				points.insert(1,[self.sensor.getDistance(),self.botAngle])
			elif self.botAngle == 180:
				points.insert(2,[self.sensor.getDistance(),self.botAngle])
			elif self.botAngle == 270:
				points.insert(3,[self.sensor.getDistance(),self.botAngle])
			else:
				points.append([self.sensor.getDistance(),self.botAngle])
			self.movement.turn(self.turnAngle)
			self.botAngle = self.botAngle+self.turnAngle
			if self.botAngle >= 360:
				self.botAngle = self.botAngle-360
				break
			#if self.botAngle == 0:
			#	break
			time.sleep(1)
		return points
