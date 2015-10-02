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
                            for k in range(i[0]):
                                self.room[j].insert(len(self.room[j]),0)
                        self.room[self.pos[0]][self.pos[1]+int(math.floor(i[0]))] = 1
                    if i[1]==180:
                        for j in range(int(math.floor(i[0]))):
                            self.room.insert(len(self.room),[0 for k in range(len(self.room[0]))])
                        self.room[self.pos[0]+int(math.floor(i[0]))][self.pos[1]] = 1

                    if i[1]==270:
                        for j in range(len(self.room)):
                            for k in range(i[0]):
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
        return room
    def updatePos(self,newPos):
        self.room[self.pos[0]][self.pos[1]]=0
        self.pos = newPos
        self.room[self.pos[0]][self.pos[1]]='8'
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
            if i[1]%90 == 0:
                #up
                if i[1]==0:
                    if i[0]>wallDist[0]:
                        over = i[0]-wallDist[0]
                        print over    
                        for j in range(over):
                            self.room.insert(0,[0 for k in range(len(self.room[0]))])
                        self.pos[0] = self.pos[0]+over    
                    if i[0]!=MAXVIEW:
                        self.room[self.pos[0]-i[0]][self.pos[1]] = 1
                #right            
                elif i[1]==90:
                    if i[0]>wallDist[1]:
                        over = i[0]-wallDist[1]
                        print over    
                        for j in range(over):
                            self.room[j].insert(len(self.room[j]),0)
                    if i[0]!=MAXVIEW:
                        self.room[self.pos[0]][self.pos[1]+int(math.floor(i[0]))] = 1
                #down
                elif i[1]==180:
                    if i[0]>wallDist[2]:
                        over = i[0]-wallDist[2]
                        print over    
                        for j in range(over):
                            self.room.insert(len(self.room),[0 for k in range(len(self.room[0]))])
                    if i[0]!=MAXVIEW:
                        self.room[self.pos[0]+int(math.floor(i[0]))][self.pos[1]] = 1
                #left       
                elif i[1]==270:
                    if i[0]>wallDist[3]:
                        over = i[0]-wallDist[3]
                        print over    
                        for j in range(over):
                            for k in range(len(self.room)):
                                self.room[k].insert(0,0)
                        self.pos[1] = self.pos[1]+over    
                    if i[0]!=MAXVIEW:
                        self.room[self.pos[0]][self.pos[1]-i[0]] = 1
            else:
                self.room[self.pos[0]+int(math.floor(min(i[0],MAXVIEW)*-math.cos(i[1]*math.pi/180)))][self.pos[1]+int(math.floor(min(i[0],MAXVIEW)*math.sin(i[1]*math.pi/180)))] = 1
                
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
                        print [self.room[i+k][j+l] for k in [-1,0,1] for l in [-1,0,1]]
        for i in range(1,len(self.room)-1):
            for j in range(1,len(self.room[i])-1):
                if ([self.room[i+k][j-1] for k in [-1,0,1]].count(1)==3 and j>self.pos[1]) or ([self.room[i+k][j+1] for k in [-1,0,1]].count(1)==3 and j<self.pos[1]) or ([self.room[i-1][j+k] for k in [-1,0,1]].count(1)==3 and i>self.pos[0]) or ([self.room[i+1][j+k] for k in [-1,0,1]].count(1)==3 and i< self.pos[0]) :
                    self.room[i][j]=9
        return
    def nextRoute(self):
        return
    def isMapped(self):
        return False
    




	