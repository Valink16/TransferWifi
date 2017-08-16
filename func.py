import pygame
from sys import setrecursionlimit
from pygame.locals import *
from time import sleep
from threading import Thread
setrecursionlimit(10000)

class fillThread(Thread):
    def __init__(self,x,y,obj,o,n,map,c,addrPos):
        Thread.__init__(self)
        self.x=x
        self.y=y
        self.obj=obj
        self.o=o
        self.n=n
        self.map=map
        self.c=c
        self.addrPos=addrPos
        self.running=True
    def run(self):
        if(self.running):
            if(floodfill(self.x,self.y,self.obj,self.o,self.n,self.map,self.c+1,self.addrPos)):
                self.running=False

def loadMap(fileName):
    map=[]
    try:
        with open(fileName,"r") as file:
            for line in file:
                map.append([])
                for case in line:
                    if(not(case=="\n")):
                        map[len(map)-1].append(mapCase(case,10000))
    except FileNotFoundError:
        for i in range(20):
            map.append([])
            for a in range(20):
                map[len(map)-1].append(mapCase(" ",0))


    return map

def drawMap(screen,map,sprDict):
    for x,line in enumerate(map):
        for y,c in enumerate(line):
            if(not(c.spr==" ")):
                screen.blit(sprDict[c.spr],(x*25,y*25))
                #index=str(x)+" : "+str(y)
                #indexTxt=sprDict["font"].render(index,1,(0,0,0))
                #screen.blit(indexTxt,(x*25+20,y*25))
                #sprTxt=sprDict["font"].render(str(c.spr),1,(0,0,0))
                #screen.blit(sprTxt,(x*25,y*25+10))
                if(not(c.spr=="w")):
                    countSurface=sprDict["font"].render(str(c.count),1,(0,0,0))
                    screen.blit(countSurface,(x*25,y*25))


def floodfill(x,y,obj,o,n,map,c,addrPos):
    if(map[x][y].spr==obj):
        print("OBJ")
        map[x][y].changeSpr("f")
        addrPos[0]=x
        addrPos[1]=y
        return True

    elif(map[x][y].spr==o):
        map[x][y].spr=n
        map[x][y].count=c
        f1=fillThread(x-1,y,obj,o,n,map,c,addrPos)
        f2=fillThread(x+1,y,obj,o,n,map,c,addrPos)
        f3=fillThread(x,y-1,obj,o,n,map,c,addrPos)
        f4=fillThread(x,y+1,obj,o,n,map,c,addrPos)
        f1.start()
        f2.start()
        f3.start()
        f4.start()

        if(not(f1.running and f2.running and f3.running and f4.running)):
            f1.running=False
            f2.running=False
            f3.running=False
            f4.running=False
            return True


def wayback(x,y,map):
    map[x][y].changeSpr("o")
    aTab=[]
    aTab.append((x,y-1))
    aTab.append((x,y+1))
    aTab.append((x-1,y))
    aTab.append((x+1,y))

    smallest=100000
    posS=[]
    for pos in aTab:
        if(map[pos[0]][pos[1]].count<smallest):
            smallest=map[pos[0]][pos[1]].count
            posS=(pos[0],pos[1])

    return posS


class mapCase():
    def __init__(self,spr,count):
        self.spr=spr
        self.count=count

    def changeSpr(self,nSpr):
        self.spr=nSpr
