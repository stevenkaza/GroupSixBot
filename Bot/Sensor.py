from discovery_bot import Ultrasound

class Sensor:
        def __init__(self):
                self.us = Ultrasound()

        def removeOutLayers(self, listS):

                low = 100
                high = 0

                for i in listS:
                        if i < low:
                                low = i
                        elif i > high:
                                high = i

                listS.remove(low)
                listS.remove(high)

                return listS

        def getDistance(self):

                listSense = []

                for i in range(10):
                        listSense.append(self.us.read_normalized())

                listSense = self.removeOutLayers(listSense)

                return float(sum(listSense))/float(len(listSense))

if __name__ == "__main__":

        s = Sensor()
        raw_input("Start")
        print s.getDistance()


