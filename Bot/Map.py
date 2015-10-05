import json
import math

MAXVIEW = 90

class Map:
    room = [[8]]
    pos = [0,0]
    
    #the first 4 points must be cardinal directions[up,right,down,left,...], the rest can be any
    def __init__(self, points):
        #points = [dist,angle]
        for i in points:
            if i[1]%90 == 0:
                if int(math.floor(i[0]))>MAXVIEW:
                    if i[1]==0:
                        for j in range(MAXVIEW):
                            self.room.insert(0,[0 for k in range(len(self.room[0]))])
                        self.pos[0] = self.pos[0]+MAXVIEW    
                    if i[1]==90:
                        for j in range(len(self.room)):
                            for k in range(MAXVIEW):
                                self.room[j].insert(len(self.room[j]),0)
                    if i[1]==180:
                        for j in range(MAXVIEW):
                            self.room.insert(len(self.room),[0 for k in range(len(self.room[0]))])
                    if i[1]==270:
                        for j in range(len(self.room)):
                            for k in range(MAXVIEW):
                                self.room[j].insert(0,0)
                        self.pos[1] = self.pos[1]+MAXVIEW
                            
                else:
                    if i[1]==0:
                        for j in range(int(math.floor(i[0]))):
                            self.room.insert(0,[0 for k in range(len(self.room[0]))])
                        self.room[self.pos[0]-int(math.floor(i[0]))-1][self.pos[1]] = 1
                        self.pos[0] = self.pos[0]+int(math.floor(i[0]))    
                    if i[1]==90:
                        for j in range(len(self.room)):
                            for k in range(int(i[0])):
                                self.room[j].insert(len(self.room[j]),0)
                        self.room[self.pos[0]][self.pos[1]+int(math.floor(i[0]))] = 1
                    if i[1]==180:
                        for j in range(int(math.floor(i[0]))):
                            self.room.insert(len(self.room),[0 for k in range(len(self.room[0]))])
                        self.room[self.pos[0]+int(math.floor(i[0]))][self.pos[1]] = 1

                    if i[1]==270:
                        for j in range(len(self.room)):
                            for k in range(int(i[0])):
                                self.room[j].insert(0,0)
                        self.pos[1] = self.pos[1]+int(math.floor(i[0]))    
                        self.room[self.pos[0]][self.pos[1]-int(math.floor(i[0]))] = 1
            else:
                self.room[self.pos[0]+int(math.floor(min(i[0],MAXVIEW)*-math.cos(i[1]*math.pi/180)))][self.pos[1]+int(math.floor(min(i[0],MAXVIEW)*math.sin(i[1]*math.pi/180)))] = 1
                #print self.pos[0]+int(math.floor(min(i[0],MAXVIEW)*math.sin(i[1]*math.pi/180)))
                #print self.pos[0]+int(math.floor(min(i[0],MAXVIEW)*-math.cos(i[1]*math.pi/180)))
    def showRoom(self):
        for i in self.room:
                print i
        print self.pos
    def getMap(self):
        return self.room
    def updatePos(self,newPos):
        self.room[self.pos[0]][self.pos[1]]=0
        self.pos = newPos
        self.room[self.pos[0]][self.pos[1]]=8
        return

    def updateMap(self,points):
        #wallDist = [up,right,down,left] 
        wallDist = list()
        wallDist.append(self.pos[0])
        wallDist.append(len(self.room[0])-self.pos[1]-1)
        wallDist.append(len(self.room)-self.pos[0]-1)
        wallDist.append(self.pos[1])
        
        over = 0
        for i in points:
            i[0]= min(i[0],MAXVIEW)
            #i[1]=i[1]/2
            if i[1]%90 == 0:
                #up
                if i[1]==0:
                    if i[0]>wallDist[0]:
                        over = int(i[0]-wallDist[0])
                        #print over    
                        for j in range(int(over)):
                            self.room.insert(0,[0 for k in range(len(self.room[0]))])
                        self.pos[0] = self.pos[0]+over    
                    if i[0]!=MAXVIEW:
                        self.room[self.pos[0]-int(math.floor(i[0]))][self.pos[1]] = points.index(i)+1
                #right            
                elif i[1]==90:
                    if int(math.floor(i[0]))>wallDist[1]:
                        over = int(i[0])-wallDist[1]
                        #print over    
                        for j in range(len(self.room)):
                            for k in range(int(i[0])):
                                self.room[j].insert(len(self.room[j]),0)
                        self.room[self.pos[0]][self.pos[1]+int(math.floor(i[0]))] = points.index(i)+1
                #down
                elif i[1]==180:
                    if i[0]>wallDist[2]:
                        over = int(i[0]-wallDist[2])
                        #print over    
                        for j in range(int(over)):
                            self.room.insert(len(self.room),[0 for k in range(len(self.room[0]))])
                    if i[0]!=MAXVIEW:
                        self.room[self.pos[0]+int(math.floor(i[0]))][self.pos[1]] = points.index(i)+1
                #left       
                elif i[1]==270:
                    if i[0]>wallDist[3]:
                        over = int(i[0]-wallDist[3])
                        #print over    
                        for j in range(int(over)):
                            for k in range(len(self.room)):
                                self.room[k].insert(0,0)
                        self.pos[1] = self.pos[1]+over    
                    if i[0]!=MAXVIEW:
                        self.room[self.pos[0]][self.pos[1]-int(math.floor(i[0]))] = points.index(i)+1
            else:
                if self.pos[0]+int(math.floor(min(i[0],MAXVIEW)*-math.cos(i[1]*math.pi/180.0)))>=len(self.room):
                    p =self.pos[0]+int(math.floor(min(i[0],MAXVIEW)*-math.cos(i[1]*math.pi/180.0))) - len(self.room)
                    for j in range (p+1):
                        self.room.insert(len(self.room),[0 for k in range(len(self.room[0]))])
                        
                elif self.pos[0]+int(math.floor(min(i[0],MAXVIEW)*-math.cos(i[1]*math.pi/180.0)))<=0:
                    p =abs(self.pos[0]+int(math.floor(min(i[0],MAXVIEW)*-math.cos(i[1]*math.pi/180.0))))
                    for j in range (p+1):
                        self.room.insert(0,[0 for k in range(len(self.room[0]))])
                    self.pos[0]=self.pos[0]+p+1
                    print "u"
                if self.pos[1]+int(math.floor(min(i[0],MAXVIEW)*math.sin(i[1]*math.pi/180.0))) >= len(self.room[0]):
                    p = self.pos[1]+int(math.floor(min(i[0],MAXVIEW)*math.sin(i[1]*math.pi/180.0))) - len(self.room[0])
                    for j in range(len(self.room)):
                        for q in range(p+1):
                            self.room[j].insert(len(self.room[j]),0)
                            
                elif self.pos[1]+int(math.floor(min(i[0],MAXVIEW)*math.sin(i[1]*math.pi/180.0))) <=0:
                    print "qq"
                    p = abs(self.pos[1]+int(math.floor(min(i[0],MAXVIEW)*math.sin(i[1]*math.pi/180.0))))
                    for j in range(len(self.room)):
                        for q in range(p+1):
                            self.room[j].insert(0,0)
                    self.pos[1] = self.pos[1]+p+1
                
                try:
                    self.room[self.pos[0]+int(math.floor(min(i[0],MAXVIEW)*-math.cos(i[1]*math.pi/180.0)))][self.pos[1]+int(math.floor(min(i[0],MAXVIEW)*math.sin(i[1]*math.pi/180.0)))] = points.index(i)+1
                except:
                    print i
                    pass
        for i in range(1,len(self.room)-1):
            for j in range(1,len(self.room[i])-1):
                if self.room[i][j]==0:
                    #looks to the left and right
                    if (([self.room[i+k][j-1] for k in [-1,0,1]].count(1)>0 and [self.room[i+k][j-1] for k in [-1,0,1]].count(1)<2) or ([self.room[i+k][j-1] for k in [-1,0,1]].count(4)>0 and [self.room[i+k][j-1] for k in [-1,0,1]].count(4)<2)) and (([self.room[i+k][j+1] for k in [-1,0,1]].count(1)>0 and [self.room[i+k][j+1] for k in [-1,0,1]].count(1)<2) or ([self.room[i+k][j+1] for k in [-1,0,1]].count(4)>0 and [self.room[i+k][j+1] for k in [-1,0,1]].count(4)<2)): 
                        if ([self.room[i-1][j+k] for k in [-1,0,1]].count(1)>0) or ([self.room[i+1][j+k] for k in [-1,0,1]].count(1)>0) or ([self.room[i-1][j+k] for k in [-1,0,1]].count(4)>0) or ([self.room[i+1][j+k] for k in [-1,0,1]].count(4)>0):
                            continue
                        self.room[i][j]=1
                    elif (([self.room[i-1][j+k] for k in [-1,0,1]].count(1)>0 and [self.room[i-1][j+k] for k in [-1,0,1]].count(1)<2) or ([self.room[i-1][j+k] for k in [-1,0,1]].count(4)>0 and [self.room[i-1][j+k] for k in [-1,0,1]].count(4)<2)) and (([self.room[i+1][j+k] for k in [-1,0,1]].count(1)>0 and [self.room[i+1][j+k] for k in [-1,0,1]].count(1)<2) or ([self.room[i+1][j+k] for k in [-1,0,1]].count(4)>0 and [self.room[i+1][j+k] for k in [-1,0,1]].count(4)<2)): 
                        if ([self.room[i+k][j-1] for k in [-1,0,1]].count(1)>0 ) or ([self.room[i+k][j+1] for k in [-1,0,1]].count(1)>0) or ([self.room[i+k][j-1] for k in [-1,0,1]].count(4)>0) or ([self.room[i+k][j+1] for k in [-1,0,1]].count(4)>0):
                            continue
                        self.room[i][j]=1
                    if [self.room[i+k][j+l] for k in [-1,0,1] for l in [-1,0,1]].count(1)>0:
                        continue
                        #print [self.room[i+k][j+l] for k in [-1,0,1] for l in [-1,0,1]]
        for i in range(1,len(self.room)-1):
            for j in range(1,len(self.room[i])-1):
                if ([self.room[i+k][j-1] for k in [-1,0,1]].count(1)==3 and j>self.pos[1]) or ([self.room[i+k][j+1] for k in [-1,0,1]].count(1)==3 and j<self.pos[1]) or ([self.room[i-1][j+k] for k in [-1,0,1]].count(1)==3 and i>self.pos[0]) or ([self.room[i+1][j+k] for k in [-1,0,1]].count(1)==3 and i< self.pos[0]) :
                    self.room[i][j]=9
        
        return
    def nextRoute(self):
        return
    def isMapped(self):
        return False
   
'''
m = Map([[4.2,0],[2.3,90],[5,180],[9,270]])
m.showRoom()

m.updatePos([6,2])
m.showRoom()

m.updateMap([[3.2,0],[4.5,90],[8,180],[6,270]])
m.showRoom()
'''

m = Map([[0,0],[0,90],[0,180],[0,270]])
#m.updateMap([[55.8,0],[35.6,90],[30.3,180],[51.6,270],[34.1,15],[33.8,30],[99.0,45],[10.0,60],[34.2,75],[35.7,105],[33.4,120],[44.0,135],[35.8,150],[31.8,165],[27.2,195],[27.2,210],[27.2,235],[27.5,240],[27.6,255],[58.1,285],[57.0,300],[54.1,315],[54.2,330],[55.7,345]])
#m.showRoom()
m.updateMap([[16.07951521873474, 0], [16.980090737342834, 90], [20.722948014736176, 180], [9.3706876039505, 270], [16.975490748882294, 15], [18.200621008872986, 30], [25.088337063789368, 45], [26.162689924240112, 60], [18.659086525440216, 75], [13.581210374832153, 105], [13.874076306819916, 120], [18.997952342033386, 135], [33.314138650894165, 150], [33.13780575990677, 165], [14.601385593414307, 195], [18.2936429977417, 210], [20.154593884944916, 225], [28.51226180791855, 240], [15.240272879600525, 255], [9.069643914699554, 285], [9.460131824016571, 300], [11.372193694114685, 315], [16.81806892156601, 330], [18.438798189163208, 345]])

m.showRoom()

'''
o=0
for i in [[16.07951521873474, 0], [16.980090737342834, 90], [20.722948014736176, 180], [9.3706876039505, 270], [16.975490748882294, 15], [18.200621008872986, 30], [25.088337063789368, 45], [26.162689924240112, 60], [18.659086525440216, 75], [13.581210374832153, 105], [13.874076306819916, 120], [18.997952342033386, 135], [33.314138650894165, 150], [33.13780575990677, 165], [14.601385593414307, 195], [18.2936429977417, 210], [20.154593884944916, 225], [28.51226180791855, 240], [15.240272879600525, 255], [9.069643914699554, 285], [9.460131824016571, 300], [11.372193694114685, 315], [16.81806892156601, 330], [18.438798189163208, 345]]:
	print o 
	print "-cos(y)",int(math.floor(min(i[0],MAXVIEW)*-math.cos(i[1]*math.pi/180.0)))
	print "sin (x)",int(math.floor(min(i[0],MAXVIEW)*math.sin(i[1]*math.pi/180.0)))
	print
	o=o+1
'''

'''
[34.1,15],[33.8,30],[34.0,45],[34.0,60],[34.2,75],[35.6,90],[40.7,105],[43.4,120],[44.0,135],[43.8,150],[31.8,165],[30.3,180],[27.2,195],[27.2,210],[27.2,235],[27.5,240],[27.6,255],[51.6,270],[58.1,285],[57.0,300],[54.1,315],[54.2,330],[55.7,345],[55.8,0]
'''
#self.room[self.pos[0]+int(math.floor(min(i[0],MAXVIEW)*-math.cos(i[1]*math.pi/180.0)))][self.pos[1]+int(math.floor(min(i[0],MAXVIEW)*math.sin(i[1]*math.pi/180.0)))] = points.index(i)
         