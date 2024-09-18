import os
import pygame
import pygame as pg
import sys
import random
import pickle
import time
import pygame_gui
import random
from UI import UI
from circleMgr import CircleMgr
from circleMgr import Circle
from opCVMgr import openCV
from pygame.locals import *
from pygame_gui import UIManager, elements
import tkinter as tk
from tkinter import filedialog
import shutil

def load_music_files(folder_path):
    music_files = ""
    for filename in os.listdir(folder_path):
        if filename.endswith(".mp3"):
            music_files = (os.path.join(folder_path, filename))
    return music_files

def draw_text(text, font, color, surface, x, y):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect()
    text_rect.topleft = (x, y)
    surface.blit(text_obj, text_rect)

pygame.init()

# 定義顏色
white = (255, 255, 255)
black = (0, 0, 0)
red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)
# 設定鏡頭畫面透明度
screenAlpha = 128

# 字體
font = pygame.font.Font(None, 36)

# 設定遊戲狀態
MAIN_MENU = 0
GAME_PLAY = 1
GAME_CREATE = 2
GAME_OVER = 3

# 初始化狀態為主選單
state = MAIN_MENU

# 設定是否用滑鼠
useMouse = True

# 設定遊戲視窗
screenSize = [800, 600]
screen = pygame.display.set_mode(screenSize)
pygame.display.set_caption("Simple osu! Game")
#蓋在screen上的半透明視窗
mask = pygame.Surface(screenSize, pygame.SRCALPHA)
#蓋在mask上的半透明視窗
circleMask = pygame.Surface(screenSize, pygame.SRCALPHA)
resultMask = pygame.Surface(screenSize, pygame.SRCALPHA)

# 按鈕位置
start_button = pygame.Rect(300, 100, 200, 50)
exit_button = pygame.Rect(300, 200 , 200, 50)
replay_button = pygame.Rect(300, 100, 200, 50)
useMouse_botton = pygame.Rect(300, 300 , 200, 50)
NotuseMouse_botton = pygame.Rect(300, 400, 200, 50)
CreateMap_botton = pygame.Rect(300, 500, 200, 50)

#造假滑鼠事件
pg.init()

#--------------------------------------------------------
# 創建下拉選單的選項
def load_subfolders(folder_path):
    subfolders = [f for f in os.listdir(folder_path) if os.path.isdir(os.path.join(folder_path, f))]
    return subfolders

ui_manager = UIManager(screenSize)
base_folder_path = 'maps' #改成你的絕對路徑
initial_subfolders = load_subfolders(base_folder_path)
dropdown_options = initial_subfolders + ["add Map"]
dropdown_rect = pygame.Rect(10, 10, 150, 30)
dropdown = elements.UIDropDownMenu(dropdown_options, initial_subfolders[0], dropdown_rect, ui_manager)
selected_option = initial_subfolders[0]
#--------------------------------------------------------

#取得音樂百分比
def getPercent(startTime, nowTime):
    percent = (nowTime - startTime) / MusicTime
    return percent
#取得音樂時間
def getMusicTime(startTime, percent):
    Mtime = MusicTime * percent
    return Mtime

#是否遊戲中
isPlaying = False

# 設定計分
score = 0
font = pygame.font.Font(None, 36)

mosPos:list[list[float]] = [[0,0]]

volume = 0.25
# 定義音量拉條屬性
volume_slider_rect = pygame.Rect(600, 100, 20, 450)
volume_slider_handle_rect = pygame.Rect(volume_slider_rect.x, (volume_slider_rect.y + volume_slider_rect.height-20)-((volume_slider_rect.height-20)*volume), 20, 20)
volume_slider_dragging = False

while True:
    rainbow = (random.randrange(0, 255), random.randrange(0, 255), random.randrange(0, 255))
    rainbow_1 = (random.randrange(0, 100), random.randrange(0, 100), random.randrange(0, 100))
    rainbow_2 = (random.randrange(150, 255), random.randrange(150, 255), random.randrange(150, 255))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            try:
                opCV.exit()
            except:
                pass
            pygame.quit()
            sys.exit()
        ui_manager.process_events(event)
        # 更新 Pygame GUI 管理器
        
        if state == MAIN_MENU:
            # 處理音量拉條事件
            if event.type == pygame.MOUSEBUTTONDOWN:
                if volume_slider_handle_rect.collidepoint(event.pos):
                    volume_slider_dragging = True
            elif event.type == pygame.MOUSEBUTTONUP:
                if volume_slider_dragging == True:
                    volume_slider_dragging = False
            elif event.type == pygame.MOUSEMOTION:
                if volume_slider_dragging:
                    # 確保拉條不會超出範圍
                    volume_slider_handle_rect.y = min(max(event.pos[1] - volume_slider_handle_rect.height/2, volume_slider_rect.y), volume_slider_rect.y + volume_slider_rect.height - volume_slider_handle_rect.height)
                    # 計算音量百分比
                    volume_percentage = (volume_slider_handle_rect.y - volume_slider_rect.y) / (volume_slider_rect.height - volume_slider_handle_rect.height)
                    volume = round(1 - volume_percentage, 2)
                    # 設置音量
                    if(volume > 1):
                        volume = 1
                    
#--------------------------------------------------------
            ui_manager.update(0.016) 

            if event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_DROP_DOWN_MENU_CHANGED:
                    if event.ui_element == dropdown:
                        selected_option = event.text
                        if selected_option == "add Map":
                            file_path = filedialog.askopenfilename()   # 選擇檔案後回傳檔案路徑與名稱
                            print(file_path)
                            fileName = file_path.split("/")
                            fileName = fileName[fileName.__len__()-1]
                            fileName = fileName.split(".")
                            print(fileName)
                            if (fileName[1] == "mp3"):
                                path = base_folder_path +'/'+ fileName[0]
                                if not os.path.isdir(path):
                                    os.mkdir(path)
                                print(file_path, path +'/'+ fileName[0] +'.'+ fileName[1])
                                shutil.copyfile(file_path, path +'/'+ fileName[0] +'.'+ fileName[1])
                                selected_option = fileName[0]
                                #造假滑鼠點擊事件
                                mouse_event = pg.event.Event(pg.MOUSEBUTTONDOWN, {'pos': (400, 525), 'button': 1})
                                pg.event.post(mouse_event)
                            else:
                                print("can only use mp3!!")
                            pass
                        mapPath = f'maps/{selected_option}'  # 將選擇的值加到路徑中
#--------------------------------------------------------
                        
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.collidepoint(event.pos):
                    state = GAME_PLAY
                    # 設定是否用滑鼠
                    #useMouse = True
                    #設定攝影機
                    opCV = openCV(screenSize, screen)
                    if useMouse == True:
                        opCV.exit()
#--------------------------------------------------------                        
                    #地圖路徑
                    mapPath = f'maps/{selected_option}'
#--------------------------------------------------------                    
                    #圈圈陣列
                    circle:list[Circle]
                    #讀檔
                    with open(mapPath + '/circle.pickle', 'rb') as f:
                        circle = pickle.load(f)
                    #音樂設定
                    mapMusic = load_music_files(mapPath)
                    pygame.mixer.music.load(mapMusic)
                    pygame.mixer.music.set_volume(volume)
                    # 載入音樂文件以利之後獲取長度
                    MusicTime = pygame.mixer.Sound(mapMusic).get_length()
                    # 遊戲開始時播放音樂
                    pygame.mixer.music.play()
                    #歸零分數
                    score = 0
                    #設定遊戲開始時間
                    startTime = time.time()
                    #設定目前時間
                    nowTime = startTime
                    #初始化各系統
                    circleMgr = CircleMgr(startTime, circle)
                    ui = UI(screen, circleMask, resultMask, startTime, circleMgr)
                    circleMgr.setUI(ui)
                    
                    isPlaying = True
                elif CreateMap_botton.collidepoint(event.pos):
                    state = GAME_CREATE
                    #設定攝影機
                    opCV = openCV(screenSize, screen)
                    if useMouse == True:
                        opCV.exit()
                    #地圖路徑
                    mapPath = f'maps/{selected_option}'
                    #圈圈陣列
                    circle:list[Circle] = []
                    #讀檔
                    if os.path.exists(mapPath + '/circle.pickle'):
                        with open(mapPath + '/circle.pickle', 'rb') as f:
                            circle = pickle.load(f)
                        f.close()
                    else:
                        with open(mapPath + '/circle.pickle', 'wb') as f:
                            pickle.dump([], f)
                        circle = []
                        f.close()
                    #音樂設定
                    mapMusic = load_music_files(mapPath)
                    pygame.mixer.music.load(mapMusic)
                    pygame.mixer.music.set_volume(volume)
                    # 載入音樂文件以利之後獲取長度
                    Music = pygame.mixer.Sound(mapMusic)
                    MusicTime = Music.get_length()
                    pygame.mixer.music.play()
                    pygame.mixer.music.pause()
                    #音樂進度條
                    musicPercent:float = 0
                    #是否播放
                    CisPlaying = False
                    #是否隱藏介面
                    isHide = False
                    
                    # 初始化 GUI 管理器
                    ui_manager = UIManager((screenSize[0],screenSize[1]))
                    # 創建按鈕
                    pause_button = elements.UIButton(relative_rect=pygame.Rect((140, 10), (100, 50)),
                                                    text='pause', manager=ui_manager)
                    back_button = elements.UIButton(relative_rect=pygame.Rect((250, 30), (50, 30)),
                                                    text='<<', manager=ui_manager)
                    forward_button = elements.UIButton(relative_rect=pygame.Rect((350, 30), (50, 30)),
                                                    text='>>', manager=ui_manager)
                    save_button = elements.UIButton(relative_rect=pygame.Rect((400, 30), (100, 30)),
                                                    text='save', manager=ui_manager)
                    hideBar_button = elements.UIButton(relative_rect=pygame.Rect((500, 30), (100, 30)),
                                                    text='hide bar', manager=ui_manager)
                    search_button = elements.UIButton(relative_rect=pygame.Rect((700, 60), (80, 30)),
                                                    text='search', manager=ui_manager)
                    delete_button = elements.UIButton(relative_rect=pygame.Rect((700, 90), (80, 30)),
                                                    text='delete', manager=ui_manager)
                    close_button = elements.UIButton(relative_rect=pygame.Rect((screenSize[0]-100, screenSize[1]-30), (80, 30)),
                                                    text='close', manager=ui_manager)
                    # 定義時間拉條屬性
                    time_slider_rect = pygame.Rect(250, 10, 450, 20)
                    slider_handle_rect = pygame.Rect(time_slider_rect.x, time_slider_rect.y, 20, 20)
                    slider_dragging = False
                    # 創建輸入框
                    time_entry = elements.UITextEntryLine(relative_rect=pygame.Rect((300, 30), (50, 30)),
                                                manager=ui_manager)
                    time_entry.set_text("0.1")

                    circle_entry = elements.UITextEntryLine(relative_rect=pygame.Rect((600, 60), (100, 30)),
                                                manager=ui_manager)
                    radius_entry = elements.UITextEntryLine(relative_rect=pygame.Rect((700, 150), (80, 30)),
                                                manager=ui_manager)
                    radius_entry.set_text("30")
                    duration_entry = elements.UITextEntryLine(relative_rect=pygame.Rect((700, 210), (80, 30)),
                                                manager=ui_manager)
                    duration_entry.set_text("1")
                    r_entry = elements.UITextEntryLine(relative_rect=pygame.Rect((720, 270), (60, 30)),
                                                manager=ui_manager)
                    r_entry.set_text("255")
                    g_entry = elements.UITextEntryLine(relative_rect=pygame.Rect((720, 300), (60, 30)),
                                                manager=ui_manager)
                    g_entry.set_text("0")
                    b_entry = elements.UITextEntryLine(relative_rect=pygame.Rect((720, 330), (60, 30)),
                                                manager=ui_manager)
                    b_entry.set_text("0")
                    
                    startTime = 0
                    nowTime = startTime
                    
                    #圓圈設定
                    mtime = None
                    mradius = 30
                    mduration = 1
                    mx = None
                    my = None
                    mcolor = red

                    circleMgr = CircleMgr(startTime, circle)
                    ui = UI(screen, circleMask, resultMask, startTime, circleMgr)
                    circleMgr.setUI(ui)

                    selectCircle = []

                    clock = pygame.time.Clock()
                
                elif exit_button.collidepoint(event.pos):
                    try:
                        opCV.exit()
                    except:
                        pass
                    pygame.quit()
                    sys.exit()
                elif useMouse_botton.collidepoint(event.pos):
                    useMouse = True
                elif NotuseMouse_botton.collidepoint(event.pos):
                    useMouse = False
                    

        if useMouse:
            if event.type == pygame.MOUSEMOTION:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                mosPos = [[mouse_x, mouse_y]]

    
    if state == MAIN_MENU:
        # 清空畫面
        screen.fill(black)
        mask.fill((0,0,0,screenAlpha))
        circleMask.fill((0,0,0,0))
        resultMask.fill((0,0,0,0))

        if useMouse :
            draw_text(f"Mode : \nuse Mouse", font, rainbow_2, screen, 80, 300)
        else :
            draw_text(f"Mode : \nuse Hand", font, rainbow_2, screen, 80, 300)
        pygame.draw.rect(screen, white, start_button)
        draw_text("game start", font, black, screen, start_button.x + 50, start_button.y + 15)

        pygame.draw.rect(screen, white, exit_button)
        draw_text("over", font, black, screen, exit_button.x + 80, exit_button.y + 15)
        #新增滑鼠切換按鈕
        pygame.draw.rect(screen, white, useMouse_botton)
        draw_text("use Mouse", font, black, screen, useMouse_botton.x + 30, useMouse_botton.y + 15)

        pygame.draw.rect(screen, white, NotuseMouse_botton)
        draw_text("use Hand", font, black, screen, NotuseMouse_botton.x + 30, NotuseMouse_botton.y + 15)

        pygame.draw.rect(screen, white, CreateMap_botton)
        draw_text("create Map", font, black, screen, CreateMap_botton.x + 30, CreateMap_botton.y + 15)

        #音量拉條隨進度移動
        volume_slider_handle_rect.x = volume_slider_rect.x + (volume * (volume_slider_rect.width - volume_slider_handle_rect.width))
        # 繪製音量拉條
        pygame.draw.rect(screen, rainbow_2, volume_slider_rect)
        pygame.draw.rect(screen, rainbow_1, volume_slider_handle_rect)
        # 顯示標籤
        volume_text = font.render(f"volume:{format(volume,'.0%')}", True, rainbow_2)
        screen.blit(volume_text, (550, 50))
        font = pygame.font.Font(None, 80)
        title_text = font.render(f"Fake\nOSU!!", True, rainbow)
        screen.blit(title_text, (80, 120))
        font = pygame.font.Font(None, 36)

        ui_manager.draw_ui(screen)


    elif state == GAME_PLAY:

        if useMouse == False:
            HandPos = opCV.updata()
            if(HandPos != False):
                mosPos = HandPos

        nowTime = time.time()
        
        #判斷命中
        score += circleMgr.Scoring(nowTime, mosPos)

        # 清空畫面
        screen.fill(white)
        mask.fill((0,0,0,screenAlpha))
        circleMask.fill((0,0,0,0))
        resultMask.fill((0,0,0,0))

        if useMouse == False:
            opCV.show()
        # 畫圓圈
        ui.draw(nowTime, mosPos)

        # 顯示分數
        score_text = font.render(f"Score: {score}", True, black)
        screen.blit(score_text, (10, 10))
        # 顯示滑鼠位置
        # mosPos_text = font.render(f"mosPos: {mosPos}", True, black)
        # screen.blit(mosPos_text, (10, 30))
        # 顯示進度條
        percent_text = font.render(f"{format(getPercent(startTime, nowTime)*100,'.1f')}%", True, black)
        screen.blit(percent_text, (screenSize[0] - 70, 10))

        #繪製半透明視窗
        screen.blit(mask, (0,0))
        screen.blit(circleMask, (0,0))
        screen.blit(resultMask, (0,0))

        if(getPercent(startTime, nowTime)>=1):
            isPlaying = False
            state = GAME_OVER
        '''
        if score == 2:
            isPlaying = False
            state = GAME_OVER
        '''

    elif state == GAME_CREATE:
        #計算時間
        dt = clock.tick(60)
        if pygame.mixer.music.get_busy():
            nowTime += dt/1000
        musicPercent = getPercent(0, nowTime)
        #處理輸入顏色
        r = r_entry.get_text()
        g = g_entry.get_text()
        b = b_entry.get_text()
        if r.isdigit():
            r = int(r)
            if not (r>=0 and r<=255):
                r_entry.set_text("0")
                r = 0
        else:
            r_entry.set_text("0")
            r = 0
        if g.isdigit():
            g = int(g)
            if not (g>=0 and g<=255):
                g_entry.set_text("0")
                g = 0
        else:
            g_entry.set_text("0")
            g = 0
        if b.isdigit():
            b = int(b)
            if not (b>=0 and b<=255):
                b_entry.set_text("0")
                b = 0
        else:
            b_entry.set_text("0")
            b = 0
        mcolor = (r, g, b)
        if radius_entry.get_text() == "":
            radius_entry.set_text("0")
        if duration_entry.get_text() == "":
            duration_entry.set_text("0")
        if time_entry.get_text() == "":
            time_entry.set_text("0")
        #處理選擇圈圈事件
        if selectCircle and selectCircle[0]:
            #處理輸入半徑和持續時間
            mradius = float(radius_entry.get_text())
            mduration = float(duration_entry.get_text())
            i = circleMgr.circleList[selectCircle[0]]
            i.radius = mradius
            i.duration = mduration
            i.color = mcolor
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                try:
                    opCV.exit()
                except:
                    pass
                pygame.quit()
                sys.exit()
            if useMouse:
                if event.type == pygame.MOUSEMOTION:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    mosPos = [[mouse_x, mouse_y]]

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if isHide:
                        isHide = False
                elif event.button == 3:
                    print(nowTime)
                    mcolor = (float(r_entry.get_text()), float(g_entry.get_text()), float(b_entry.get_text()))
                    mradius = float(radius_entry.get_text())
                    mduration = float(duration_entry.get_text())
                    c = Circle(nowTime, mradius, mduration, mosPos[0][0], mosPos[0][1], mcolor)
                    circleMgr.add(c)
            
            # 更新 UI 管理器
            time_delta = pygame.time.Clock().tick(60) / 1000.0
            if not isHide:
                ui_manager.process_events(event)
                ui_manager.update(time_delta)

            if not isHide:   
                # 處理按鈕事件
                if pause_button.check_pressed():
                    if nowTime<MusicTime:
                        CisPlaying = not CisPlaying
                elif back_button.check_pressed():
                    try:
                        nowTime -= float(time_entry.get_text())
                        if nowTime <= 0:
                            nowTime = 0
                        pygame.mixer.music.set_pos(nowTime)
                    except:
                        pass
                elif forward_button.check_pressed():
                    try:
                        nowTime += float(time_entry.get_text())
                        if nowTime >= Music.get_length():
                            nowTime = Music.get_length()
                            CisPlaying = False
                            pygame.mixer.music.set_pos(nowTime)
                            pygame.mixer.music.pause()
                        else:
                            pygame.mixer.music.set_pos(nowTime)
                    except:
                        pass
                elif save_button.check_pressed():
                    with open(mapPath + '/circle.pickle', 'wb') as f:
                        pickle.dump(circleMgr.circleList, f)
                    f.close()
                elif hideBar_button.check_pressed():
                    try:
                        isHide = True
                        pass
                    except:
                        pass
                elif search_button.check_pressed():
                    selectCircle = []
                    s = circle_entry.get_text().split('~')
                    begin = s[0]
                    end = s[s.__len__()-1]
                    if begin.isdigit() and end.isdigit():
                        b = int(begin)
                        e = int(end)
                        if b > circleMgr.circleList.__len__() -1:
                            b = circleMgr.circleList.__len__() -1
                        if e > circleMgr.circleList.__len__() -1:
                            e = circleMgr.circleList.__len__() -1
                        if b > e :
                            a = b
                            b = e
                            e = a
                        nowTime = circleMgr.circleList[b].time
                        for i in range(b,e+1):
                            selectCircle.append(i)
                            print(i)
                    if s[0] == "":
                        circle_entry.set_text("")
                        selectCircle = []
                    if selectCircle and selectCircle[0]:
                        i = circleMgr.circleList[selectCircle[0]]
                        mradius = i.radius
                        radius_entry.set_text(str(mradius))
                        mduration = i.duration
                        duration_entry.set_text(str(mduration))
                        mcolor = (int(i.color[0]),int(i.color[1]),int(i.color[2]))
                        print(mcolor)
                        r_entry.set_text(str(mcolor[0]))
                        g_entry.set_text(str(mcolor[1]))
                        b_entry.set_text(str(mcolor[2]))
                elif delete_button.check_pressed():
                    selectCircle.reverse()
                    circleMgr.remove(selectCircle)
                    selectCircle = []
                    circle_entry.set_text("")
                elif close_button.check_pressed():
                    state = MAIN_MENU

                # 處理時間拉條事件
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if slider_handle_rect.collidepoint(event.pos):
                        slider_dragging = True
                        pygame.mixer.music.pause()
                elif event.type == pygame.MOUSEBUTTONUP:
                    if slider_dragging == True:
                        slider_dragging = False
                        pygame.mixer.music.unpause()
                elif event.type == pygame.MOUSEMOTION:
                    if slider_dragging:
                        # 確保拉條不會超出範圍
                        slider_handle_rect.x = min(max(event.pos[0] - slider_handle_rect.width/2, time_slider_rect.x), time_slider_rect.x + time_slider_rect.width - slider_handle_rect.width)
                        # 計算時間百分比
                        time_percentage = (slider_handle_rect.x - time_slider_rect.x) / (time_slider_rect.width - slider_handle_rect.width)
                        musicPercent = time_percentage
                        nowTime = getMusicTime(0, musicPercent)
                        # 設置音樂時間
                        if(musicPercent < 1):
                            if pygame.mixer.music.get_busy():
                                pygame.mixer.music.set_pos(musicPercent * Music.get_length())
                            else:
                                pygame.mixer.music.play()
                                pygame.mixer.music.pause()
                                pygame.mixer.music.set_pos(musicPercent * Music.get_length())
                        else:
                            pygame.mixer.music.pause()
                            CisPlaying = False
                            pygame.mixer.music.set_pos(Music.get_length())
        if useMouse == False:
            HandPos = opCV.updata()
            if(HandPos != False):
                mosPos = HandPos
        
        if(CisPlaying and not slider_dragging):
            pygame.mixer.music.unpause()
        else:
            pygame.mixer.music.pause()

        # 清空畫面
        screen.fill(white)
        mask.fill((0,0,0,screenAlpha))
        circleMask.fill((0,0,0,0))
        resultMask.fill((0,0,0,0))
        
        if useMouse == False:
            opCV.show()

        # 畫圓圈
        ui.draw(nowTime, None, False, font)

        #時間拉條隨進度移動
        slider_handle_rect.x = time_slider_rect.x + (musicPercent * (time_slider_rect.width - slider_handle_rect.width))

        # 顯示滑鼠位置
        mosPos_text = font.render(f"mosPos: \n{mosPos}", True, black)
        resultMask.blit(mosPos_text, (10, 10))
        # 顯示進度
        percent_text = font.render(f"{format(getPercent(startTime, nowTime)*100,'.1f')}%\ns:{format(nowTime, '.2f')}", True, black)
        resultMask.blit(percent_text, (screenSize[0] - 95, 10))
        # 顯示標籤
        radius_text = font.render(f"radius", True, black)
        resultMask.blit(radius_text, (700, 120))
        duration_text = font.render(f"duration", True, black)
        resultMask.blit(duration_text, (700, 180))
        R_text = font.render(f"R", True, black)
        resultMask.blit(R_text, (700, 270))
        g_text = font.render(f"G", True, black)
        resultMask.blit(g_text, (700, 300))
        b_text = font.render(f"B", True, black)
        resultMask.blit(b_text, (700, 330))
        #顯示顏色
        pygame.draw.rect(resultMask, mcolor, (700, 240, 80, 30))
        # 顯示目前選擇
        if selectCircle.__len__() >= 2:
            select_text = font.render(f"{selectCircle[0]}~{selectCircle[selectCircle.__len__()-1]}", True, black)
        elif selectCircle.__len__() >= 1:
            select_text = font.render(f"{selectCircle[0]}", True, black)
        else:
            select_text = font.render(f"", True, black)
        resultMask.blit(select_text, (600, 30))
        # 繪製按鈕、下拉選單和拉條
        if not isHide:
            ui_manager.draw_ui(resultMask)
        # 繪製時間拉條
        pygame.draw.rect(resultMask, (255, 255, 255), time_slider_rect)
        pygame.draw.rect(resultMask, (0, 0, 255), slider_handle_rect)

        #繪製半透明視窗
        screen.blit(mask, (0,0))
        screen.blit(circleMask, (0,0))
        if(not isHide):
            screen.blit(resultMask, (0,0))

        if state != GAME_CREATE:
            # 設定是否用滑鼠
            useMouse = True
            # 遊戲結束暫停音樂
            pygame.mixer.music.pause()
            #設定攝影機
            try:
                opCV.exit()
            except:
                pass
            opCV = None
            #圈圈陣列
            circle:list[Circle] = None
            #音樂設定
            mapMusic = None
            #初始化各系統
            circleMgr = None
            ui = None

            ui_manager = UIManager(screenSize)
            base_folder_path = 'maps' #改成你的絕對路徑
            initial_subfolders = load_subfolders(base_folder_path)
            dropdown_options = initial_subfolders + ["add Map"]
            dropdown_rect = pygame.Rect(10, 10, 150, 30)
            dropdown = elements.UIDropDownMenu(dropdown_options, initial_subfolders[0], dropdown_rect, ui_manager)
            selected_option = initial_subfolders[0]
            
            isPlaying = False
        
    elif state == GAME_OVER:
        # 設定是否用滑鼠
        useMouse = True
        # 遊戲結束暫停音樂
        pygame.mixer.music.pause()
        #設定攝影機
        try:
            opCV.exit()
        except:
            pass
        opCV = None
        #圈圈陣列
        circle:list[Circle] = None
        #音樂設定
        mapMusic = None
        #初始化各系統
        circleMgr = None
        ui = None
        
        isPlaying = False
        # 清空畫面
        screen.fill(black)
        mask.fill((0,0,0,screenAlpha))
        circleMask.fill((0,0,0,0))
        resultMask.fill((0,0,0,0))
        font = pygame.font.Font(None, 80)
        draw_text("game over", font, rainbow_2, screen, 250, 400)
        draw_text(f'your score = {score}', font, rainbow_2, screen, 250, 450)

        font = pygame.font.Font(None, 36)
        pygame.draw.rect(screen, white, start_button)
        draw_text("replay", font, black, screen, start_button.x + 50, start_button.y + 15)

        pygame.draw.rect(screen, white, exit_button)
        draw_text("quit", font, black, screen, exit_button.x + 80, exit_button.y + 15)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                try:
                    opCV.exit()
                except:
                    pass
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if replay_button.collidepoint(event.pos):
                    state = MAIN_MENU  
                elif exit_button.collidepoint(event.pos):
                    try:
                        opCV.exit()
                    except:
                        pass
                    pygame.quit()
                    sys.exit()
    # 更新畫面
    pygame.display.flip()