import cv2
import cvzone
from cvzone.HandTrackingModule import HandDetector
import pygame

class openCV:
    screen: pygame.Surface
    def __init__(self, screenSize, screen):
        self.screenSize = screenSize
        self.screen = screen
        # 初始化 HandDetector
        self.detector = HandDetector(
            staticMode = False,
            maxHands = 2,
            modelComplexity = 1,
            detectionCon = 0.5,
            minTrackCon = 0.3
        )
        # 選擇第一個攝像頭（如果有多個攝像頭，可以調整引數）
        try:
            self.cap = cv2.VideoCapture(0)
        except:
            pass

    def updata(self) -> list[list[float]] | bool:
        # 讀取一個視訊幀
        ret, self.frame = self.cap.read()
        
        # 將畫面水平翻轉
        self.frame = cv2.rotate(self.frame, cv2.ROTATE_90_COUNTERCLOCKWISE)
        
        # 找出手部
        hands, self.frame = self.detector.findHands(self.frame,False)

        # 繪製手部關鍵點和連線
        if hands:
            '''
        # 取得第一隻手的資訊
            hand = hands[0]
        
        # 取得手部所有關鍵點的座標
            hand_landmarks = hand['lmList']
        
        # 打印或使用手的座標
            #print("Hand Landmarks:", hand_landmarks)
        
        # 例如，取得食指指尖的座標
            index_finger_tip = hand_landmarks[8]  # 8 是食指指尖的索引
            print("Index Finger Tip Coordinates (x, y):", (index_finger_tip[1], index_finger_tip[0]))
            '''
        #校正座標點
            width = self.cap.get(cv2.CAP_PROP_FRAME_WIDTH)
            height = self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT)

            scaleX = self.screenSize[0] / width
            scaleY = self.screenSize[1] / height

        #取得座標
            pos = []
            for h in hands:
                mosX = 0
                mosY = 0
                # 取得手部所有關鍵點的座標
                hand_landmarks = h['lmList']
                for a in hand_landmarks:
                    mosX += a[1] * scaleX
                    mosY += a[0] * scaleY
                mosX /= hand_landmarks.__len__()
                mosY /= hand_landmarks.__len__()
                pos.append([round(mosX), round(mosY)])
                #print("hand(x,y): ", pos)
            return pos
        return False


    def show(self):
        # 將 OpenCV 的影像轉換成 Pygame 的 Surface
        self.frame = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
        self.frame = pygame.surfarray.make_surface(self.frame)
        self.frame = pygame.transform.scale(self.frame, self.screenSize)
        self.screen.blit(self.frame, (0, 0))
    
    def exit(self):
        # 釋放攝像頭並關閉視窗
        try:
            self.cap.release()
        finally:
            cv2.destroyAllWindows()
