import json
import math

MAXVIEW = 90

DIST0  =0
DIST90 =0
DIST180=0
DIST270=0

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
        self.room[self.pos[0]][self.pos[1]]=0
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
                        self.room[self.pos[0]-int(math.floor(i[0]))][self.pos[1]] = 1
                #right            
                elif i[1]==90:
                    if int(math.floor(i[0]))>wallDist[1]:
                        over = int(i[0])-wallDist[1]
                        #print over    
                        for j in range(len(self.room)):
                            for k in range(int(i[0])):
                                self.room[j].insert(len(self.room[j]),0)
                    if i[0]!=MAXVIEW:
                        self.room[self.pos[0]][self.pos[1]+int(math.floor(i[0]))] = 1
                #down
                elif i[1]==180:
                    if i[0]>wallDist[2]:
                        over = int(i[0]-wallDist[2])
                        #print over    
                        for j in range(int(over)):
                            self.room.insert(len(self.room),[0 for k in range(len(self.room[0]))])
                    if i[0]!=MAXVIEW:
                        self.room[self.pos[0]+int(math.floor(i[0]))][self.pos[1]] = 1
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
                        self.room[self.pos[0]][self.pos[1]-int(math.floor(i[0]))] = 1
            else:
                if self.pos[0]+int(math.floor(min(i[0],MAXVIEW)*-math.cos(i[1]*math.pi/180.0)))>=len(self.room):
                    p =self.pos[0]+int(math.floor(min(i[0],MAXVIEW)*-math.cos(i[1]*math.pi/180.0))) - len(self.room)
                    for j in range (p+1):
                        self.room.insert(len(self.room),[0 for k in range(len(self.room[0]))])
                        
                elif self.pos[0]+int(math.floor(min(i[0],MAXVIEW)*-math.cos(i[1]*math.pi/180.0)))<=0:
                    p =abs(self.pos[0]+int(math.floor(min(i[0],MAXVIEW)*-math.cos(i[1]*math.pi/180.0))))
                    for j in range (p+1):
                        self.room.insert(0,[0 for k in range(len(self.room[0]))])
                    self.pos[0]=self.pos[0]+p
                if self.pos[1]+int(math.floor(min(i[0],MAXVIEW)*math.sin(i[1]*math.pi/180.0))) >= len(self.room[0]):
                    p = self.pos[1]+int(math.floor(min(i[0],MAXVIEW)*math.sin(i[1]*math.pi/180.0))) - len(self.room[0])
                    for j in range(len(self.room)):
                        for q in range(p+1):
                            self.room[j].insert(len(self.room[j]),0)
                            
                elif self.pos[1]+int(math.floor(min(i[0],MAXVIEW)*math.sin(i[1]*math.pi/180.0))) <=0:
                    p = abs(self.pos[1]+int(math.floor(min(i[0],MAXVIEW)*math.sin(i[1]*math.pi/180.0))))
                    for j in range(len(self.room)):
                        for q in range(p+1):
                            self.room[j].insert(0,0)
                    self.pos[1] = self.pos[1]+p+1
                
                try:
                    self.room[self.pos[0]+int(math.floor(min(i[0],MAXVIEW)*-math.cos(i[1]*math.pi/180.0)))][self.pos[1]+int(math.floor(min(i[0],MAXVIEW)*math.sin(i[1]*math.pi/180.0)))] = 1
                except:
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
        self.room[self.pos[0]][self.pos[1]] = 8
        return self.pos
	
    def nextRoute(self):
        return
    def isMapped(self):
        return False
	
    def fillMap90(self):
        fillR =-1
        fillL =-1
        fillU =-1
        fillD =-1
        print self.pos
        for i in range(len(self.room)):
            if self.room[i][self.pos[1]] == 1:
                if i>self.pos[0] and fillD==-1:
                    fillD=i
                elif i<self.pos[0] and fillU==-1:
                    fillU=i
        for i in range(len(self.room[self.pos[0]])):
            if self.room[self.pos[0]][i]==1:
                if i>self.pos[1] and fillR==-1:
                    fillR=i
                elif i<self.pos[1] and fillL==-1:
                    fillL=i
        if fillR!=-1:
            for i in range(len(self.room)):
                self.room[i][fillR] =1
        if fillL!=-1:
            for i in range(len(self.room)):
                self.room[i][fillL]=1
        if fillU!=-1:
            for i in range(len(self.room[0])):
                self.room[fillU][i]=1
        if fillD!=-1:
            for i in range(len(self.room[0])):
                self.room[fillD][i]=1
        return

    def makeBox(self):
        length = int(len(self.room))
        width = int(len(self.room[0]))

        room = []

        for i in range(length):
            line = []
            for j in range(width):
                if (i == 0 or j == 0) or (i == length - 1) or (j == width - 1):
                    line.append(1)
                else:
                    line.append(0)

            room.append(line)

        room[int(self.top)][int(self.left)] = 8

        return room


    def nextRoute90(self):
        moveR=True
        moveL=True
        moveU=True
        moveD=True
        p = list()
        for i in range(len(self.room)):
            if self.room[i].count(1)==0:
                continue
            for j in range(len(self.room[i])):
                if self.room[i][j]==1:
                    p.append([i,j])
        for i in p:
            if i[0]>self.pos[0] and i[1]==self.pos[1]:
                moveD=False
            if i[0]<self.pos[0] and i[1]==self.pos[1]:
                moveU=False
            if i[1]>self.pos[1] and i[0]==self.pos[0]:
                moveR=False
            if i[1]<self.pos[1] and i[0]==self.pos[0]:
                moveL=False
        if moveD:
            return "D"
        if moveL:
            return "L"
        if moveR:
            return "R"
        if moveU: 
            return "U"
        return

'''
m=Map([[10,0],[100,90],[10,180],[20,270]])
m.fillMap90()
m.showRoom()
nr = m.nextRoute90()
'''
'''
m.updatePos([m.pos[0],m.pos[1]+MAXVIEW-20])
m.updateMap([[10,0],[30,90],[10,180],[70,270]])
m.fillMap90()
m.showRoom()

print m.nextRoute90()
'''      
'''
m = Map([[4.2,0],[2.3,90],[5,180],[9,270]])
m.showRoom()

m.updatePos([6,2])
m.showRoom()

m.updateMap([[3.2,0],[4.5,90],[8,180],[6,270]])
m.showRoom()
'''

'''
m = Map([[0,0],[0,90],[0,180],[0,270]])
#m.updateMap([[55.8,0],[35.6,90],[30.3,180],[51.6,270],[34.1,15],[33.8,30],[99.0,45],[10.0,60],[34.2,75],[35.7,105],[33.4,120],[44.0,135],[35.8,150],[31.8,165],[27.2,195],[27.2,210],[27.2,235],[27.5,240],[27.6,255],[58.1,285],[57.0,300],[54.1,315],[54.2,330],[55.7,345]])
#m.showRoom()
m.updateMap([[16.07951521873474, 0], [16.980090737342834, 90], [20.722948014736176, 180], [9.3706876039505, 270], [16.975490748882294, 15], [18.200621008872986, 30], [25.088337063789368, 45], [26.162689924240112, 60], [18.659086525440216, 75], [13.581210374832153, 105], [13.874076306819916, 120], [18.997952342033386, 135], [33.314138650894165, 150], [33.13780575990677, 165], [14.601385593414307, 195], [18.2936429977417, 210], [20.154593884944916, 225], [28.51226180791855, 240], [15.240272879600525, 255], [9.069643914699554, 285], [9.460131824016571, 300], [11.372193694114685, 315], [16.81806892156601, 330], [18.438798189163208, 345]])


m.showRoom()


o=0
left = []
right = []
u = [[16.07951521873474, 0],[16.975490748882294, 15], [18.200621008872986, 30], [25.088337063789368, 45], [26.162689924240112, 60], [18.659086525440216, 75],[16.980090737342834, 90], [13.581210374832153, 105], [13.874076306819916, 120], [18.997952342033386, 135], [33.314138650894165, 150], [33.13780575990677, 165],[20.722948014736176, 180], [14.601385593414307, 195], [18.2936429977417, 210], [20.154593884944916, 225], [28.51226180791855, 240], [15.240272879600525, 255],  [9.3706876039505, 270], [9.069643914699554, 285], [9.460131824016571, 300], [11.372193694114685, 315], [16.81806892156601, 330], [18.438798189163208, 345]]
for i in range(len(u)):
	try:
		br = abs(u[i][0])-abs(u[i+1][0])
	except:
		br = None
	try:
		bl = abs(u[i][0])-abs(u[i-1][0])
	except:
		bl = None
	right.append(br)
	left.append(bl)
print left,right

b=list()
print len(left)
for i in range(len(left)):
	try:
		b.append( abs(abs(left[i])-abs(right[i])))
	except:
		b.append(None)
	if b[i]>8:
		print i
print b

'''
'''
	print o 
	print "-cos(y)",int(math.floor(min(i[0],MAXVIEW)*-math.cos(i[1]*math.pi/180.0)))
	print "sin (x)",int(math.floor(min(i[0],MAXVIEW)*math.sin(i[1]*math.pi/180.0)))
	print
	o=o+1
'''

'''
[34.1,15],[33.8,30],[34.0,45],[34.0,60],[34.2,75],[35.6,90],[40.7,105],[43.4,120],[44.0,135],[43.8,150],[31.8,165],[30.3,180],[27.2,195],[27.2,210],[27.2,235],[27.5,240],[27.6,255],[51.6,270],[58.1,285],[57.0,300],[54.1,315],[54.2,330],[55.7,345],[55.8,0]
[[20.47097086906433, 0],  [24.92324858903885, 180], [15.941515564918518, 270], [20.10194957256317, 15], [22.920720279216766, 30], [26.504622399806976, 45], [26.160645484924316, 60], [17.270401120185852, 75],[16.096892952919006, 90], [16.770024597644806, 105], [22.344699501991272, 120], [31.41229897737503, 135], [30.852633714675903, 150], [25.90509057044983, 165], [25.064314901828766, 195], [25.796224176883698, 210], [28.912460803985596, 225], [28.7862166762352, 240], [17.024557292461395, 255], [14.91878479719162, 285], [16.405092179775238, 300], [20.744414627552032, 315], [26.654888689517975, 330], [25.965401530265808, 345]]

'''
#self.room[self.pos[0]+int(math.floor(min(i[0],MAXVIEW)*-math.cos(i[1]*math.pi/180.0)))][self.pos[1]+int(math.floor(min(i[0],MAXVIEW)*math.sin(i[1]*math.pi/180.0)))] = points.index(i)
         


