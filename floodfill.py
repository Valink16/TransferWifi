import pygame
from pygame.locals import *
from func import *

pygame.display.init()
pygame.font.init()
font=pygame.font.SysFont("arial",10)
screen=pygame.display.set_mode((500,500))

clock=pygame.time.Clock()
pygame.key.set_repeat(50,20)
map=loadMap("map")
bgColor=(255,255,255)
wallSpr=pygame.image.load("assets/wall.png").convert()
fillSpr=pygame.image.load("assets/fill.png").convert()
objSpr=pygame.image.load("assets/obj.png").convert()
wallSpr=pygame.transform.scale(wallSpr,(25,25))
objSpr=pygame.transform.scale(objSpr,(25,25))
fillSpr=pygame.transform.scale(fillSpr,(25,25))
sprDict={"w":wallSpr, "f":fillSpr, "font": font, "o": objSpr}
mainLoop=True
nSpr="w"
while(mainLoop):
    events=pygame.event.get()
    for event in events:
        if(event.type==QUIT):
            mapS=""
            for l in map:
                line=""
                for c in l:
                    if(c.spr=="f"):
                        c.changeSpr(" ")
                    line+=c.spr
                mapS+=line+"\n"
            with open("map","w") as file:
                file.write(mapS)
            mainLoop=False

        if(event.type==KEYDOWN):
            if(event.key==K_q):
                x,y=pygame.mouse.get_pos()
                tabPosObj=[0,0]
                filler=fillThread(x//25,y//25,"o"," ","f",map,0,tabPosObj)
                filler.start()
                print(tabPosObj)
                sPos=wayback(tabPosObj[0],tabPosObj[1],map)
                print(map[sPos[0]][sPos[1]].spr)
                print(map[sPos[0]][sPos[1]].count)
                map[sPos[0]][sPos[1]].changeSpr("o")
            if(event.key==K_r):
                map=loadMap("save")
        if(event.type==MOUSEBUTTONDOWN):
            x,y=event.pos
            b=event.button

            if(b==1):
                nSpr="w"
            elif(b==2):
                nSpr="o"
            elif(b==3):
                nSpr=" "
    pressed=pygame.key.get_pressed()
    if(pressed[K_a]):
        x,y=pygame.mouse.get_pos()
        print("Changing at {},{}".format(x//25,y//25))
        map[x//25][y//25].changeSpr(nSpr)
    clock.tick(60)

    #Drawing
    screen.fill(bgColor)
    drawMap(screen,map,sprDict)
    pygame.display.flip()
    fps=clock.get_fps()
    pygame.display.set_caption("FPS: {}".format(fps))
