'''
time        打擊時間
radius      半徑
duration    持續時間
x           位置
y           位置
color       顏色
'''
class Circle:
    def __init__(self, time, radius, duration, x, y, color):
        self.time = time
        self.radius = radius
        self.duration = duration
        self.x = x
        self.y = y
        self.color = color

class CircleMgr:
    def __init__(self, startTime, circle):
        self.ui = None
        self.StartTime = startTime
        self.circleList: list[Circle] = circle
        self.circleFlag: list[bool] = []
        for i in range(self.circleList.__len__()):
            self.circleFlag.append(False)
    def setUI(self, ui):
        self.ui = ui
    
    def Scoring(self, nowTime, mosPos) -> int:
        for i in range(self.circleList.__len__()):
            if self.circleFlag[i] == True:
                continue
            if nowTime - self.StartTime >= self.circleList[i].time:
                self.circleFlag[i] = True
                for m in mosPos:
                    print(m)
                    distance = ((m[0] - self.circleList[i].x) ** 2 + (m[1] - self.circleList[i].y) ** 2) ** 0.5
                    if distance <= self.circleList[i].radius:
                        self.ui.setIsScore(i, True)
                        return 1
            else:
                break
        return 0
    def add(self, c):
        self.circleList.append(c)
        self.circleList = sorted(self.circleList,key=lambda a:a.time)
        self.ui.ChangeCircle(self.circleList)
    def remove(self, numberList):
        for i in numberList:
            self.circleList.pop(i)
        self.circleList = sorted(self.circleList,key=lambda a:a.time)
        self.ui.ChangeCircle(self.circleList)