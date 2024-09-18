import time
import pygame
from circleMgr import CircleMgr, Circle

# 定義顏色
white = (255, 255, 255)
black = (0, 0, 0)
red = (255,0,0)
green = (0,255,0)

#結果持續時間
scoreTime = 0.5

class UI:
    circleList: list[Circle]
    Screen: pygame.Surface
    StartTime: float

    def __init__(self, screen, circleMask, resultMask, startTime, circleMgr):
        self.Screen = screen
        self.circleMask = circleMask
        self.resultMask = resultMask
        self.StartTime = startTime
        self.circleMgr: CircleMgr = circleMgr
        self.circleList: list[Circle] = self.circleMgr.circleList
        self.isScoreList: list[bool] = []
        for i in range(self.circleList.__len__()):
            self.isScoreList.append(False)

    def ChangeCircle(self, circleList):
        self.circleList = circleList

    def draw(self, nowTime, mosPos = None, useResult = True, showNum = None):
        #畫圓圈
        for i in range (self.circleList.__len__()):
            
            circle =self.circleList[i]
            timeLeft = circle.duration + (nowTime-0.01 - self.StartTime - circle.time)
            if(timeLeft < 0 or timeLeft >= circle.duration):
                continue
            alpha = timeLeft*700
            if alpha > 255:
                alpha = 255
            a = circle.radius + ((circle.duration - timeLeft) * circle.radius * 4)
            r,g,b = circle.color
            color = (r,g,b,alpha)
            pygame.draw.circle(self.circleMask, color, (circle.x, circle.y), a, 2)
            pygame.draw.circle(self.circleMask, color, (circle.x, circle.y), circle.radius)
            if showNum:
                Num_text = showNum.render(f"{i}", True, black)
                self.circleMask.blit(Num_text, (circle.x - (circle.radius/2), circle.y - (circle.radius/2)))
                pass
        #畫結果
        if useResult:
            for i in range (self.circleList.__len__()):
                circle =self.circleList[i]
                timeLeft = scoreTime + (circle.time - (nowTime - self.StartTime))
                if(timeLeft < 0 or timeLeft > scoreTime):
                    continue
                alpha = 255 * (timeLeft/scoreTime)
                if self.isScoreList[i] == True:
                    r,g,b = green
                    color = (r,g,b,alpha)
                    pygame.draw.circle(self.resultMask, color, (circle.x, circle.y), 10, 3)
                else:
                    r,g,b = red
                    color = (r,g,b,alpha)
                    pygame.draw.line(self.resultMask, color, (circle.x-10, circle.y-10), (circle.x+10, circle.y+10), 3)
                    pygame.draw.line(self.resultMask, color, (circle.x-10, circle.y+10), (circle.x+10, circle.y-10), 3)
        #畫滑鼠位置
        if(mosPos != None):
            for m in mosPos:
                pygame.draw.circle(self.resultMask, white, (m[0], m[1]), 10)

    def setIsScore(self, i, isScore:bool):
        self.isScoreList[i] = isScore