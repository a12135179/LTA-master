import cv2
import numpy as np
"""
這個文件的功能為在輸出結果當中印出除了虛線跟實線車道線之外，
提示箭頭跟文字都是在這裡做處理，只要修改這個文件
就可以加上新的功能

物件：
class DrivingAssistant
屬性：
self.road_image 已經印有車道線的道路照片，
self.h_sample   tusimple的H_sample
self.coords     該照片的預測出來的線條
方法：
CenterArrowedLine()：印出行駛中車道線的中心箭頭
KeepCenter():偵測車子是否在道路中心，並印出提示文字跟箭頭，和標示車子的中央。
"""
class DrivingAssistant:
    def __init__(self,road_image,coords):
        self.road_image = road_image
        self.h_sample = [160, 170, 180, 190, 200, 210, 220, 230, 240, 250, 260, 270, 280, 290, 300, 310, 320, 330, 340, 350, 360, 370, 380, 390, 400, 410, 420, 430, 440, 450, 460, 470, 480, 490, 500, 510, 520, 530, 540, 550, 560, 570, 580, 590, 600, 610, 620, 630, 640, 650, 660, 670, 680, 690, 700, 710]
        self.coords = coords
    #def BirdEyeView(self)
    def CenterArrowedLine(self,left,right): #輸出車道中間的方向箭頭
        #h_sample = [160, 170, 180, 190, 200, 210, 220, 230, 240, 250, 260, 270, 280, 290, 300, 310, 320, 330, 340, 350, 360, 370, 380, 390, 400, 410, 420, 430, 440, 450, 460, 470, 480, 490, 500, 510, 520, 530, 540, 550, 560, 570, 580, 590, 600, 610, 620, 630, 640, 650, 660, 670, 680, 690, 700, 710]
   
        y_sample = [i for i in range(56)]
        arr_start = 0
        arr_end = 0
        for i in y_sample:
            if left[1][i][0] >0 and right[1][i][0] >0 :
                arr_start = i
                break
            
        #print("arr_start",arr_start)
        y_sample = [i for i in range(55,-1,-1)]
        #print(y_sample)
        for i in y_sample:
            if left[1][i][0] >0 and right[1][i][0] >0 :
                arr_end = i
                break
        if self.h_sample[arr_end]>650:
            arr_end = self.h_sample.index(650)
        if self.h_sample[arr_start]<200:
            arr_start = self.h_sample.index(250)

        arr_line = [x for x in range(arr_start,arr_end)] 
        arr_len = len(arr_line)   
        #print("arr_end",arr_end)
        arr_start_x = (right[1][arr_start][0]+left[1][arr_start][0])/2
        arr_end_x = (right[1][arr_end][0]+left[1][arr_end][0])/2
        #arr_start_x是
        #x_last = 0
        #y_last = 0
        #for i in range(1,arr_len,10):
        #    y1 = int(self.h_sample[arr_line[i-1]])
        #    y2 = int(self.h_sample[arr_line[i]])
        #    x1 = int((right[1][i-1][0] + left[1][i-1][0])/2)
        #    x2 = int((right[1][i][0] + left[1][i][0])/2)
        #    x_last = x1
        #    y_last = y1
        #    cv2.line(self.road_image,(x1,y1),(x2,y2),(255,255,255),3)
        cv2.arrowedLine(self.road_image,(int(arr_end_x),self.h_sample[int(arr_end)]),(int(arr_start_x),self.h_sample[int(arr_start)]),(255,255,255),3)
        #車道中間點
        #箭頭尾端
        arr_end_coor = (int(arr_end_x),self.h_sample[arr_end])
        cv2.circle(self.road_image,arr_end_coor,4,(255,0,0),-2)
        return arr_end_coor
    def KeepCenter(self,left,right,arr_end_coor):

        """
        Arguments:
        ----------
        left:行駛中的車道中，左邊的車道線
        right:行駛車道中的右邊車道線
        arr_end_coor: 箭頭的末端
        Return:
        ----------
        self.road_image:image that is added CenterPoint and KeepCenter Message
        """
        
       
        car_center_coor = int(1280/2-1)
        #標示車子的中央
        cv2.circle(self.road_image, (car_center_coor,720-10), 5, (0,0,255), -2)
        cv2.line(self.road_image,(car_center_coor,710),(car_center_coor,650),(255,0,255),3)
        cv2.line(self.road_image,(car_center_coor,710),arr_end_coor,(0,0,255),2)

        #如果沒有偵測到左右車道線的話，退出
        if right[0] == -1 or left[0]==-1:  
            return self.road_image
        
        #車道正中央的x座標
        lane_center = arr_end_coor[0]
        
        
        if lane_center - car_center_coor > 10: #如果車子太偏左
            flag = 'KeepRight'
        elif lane_center - car_center_coor < -10: #如果車子太偏右
            flag = 'KeepLeft'
        else:
            flag = 'In the center'

        #flag 是 KeepCenter Message

        #印出靠左、靠右的提示文字跟提示箭頭
        if flag is 'KeepRight':
            #印出右箭頭
            cv2.arrowedLine(self.road_image,(10,30),(70,30),(255,255,255),3,tipLength=0.5)
        elif flag is 'KeepLeft':
            #印出左箭頭
            cv2.arrowedLine(self.road_image,(70,30),(10,30),(255,255,255),3,tipLength=0.5)
        else:
            #印出圈圈
            self.road_image = cv2.circle(self.road_image, (40,30), 25, (255,255,255), 2)
        #印出文字與文字後的黑框框
        textOrg = (int(car_center_coor-100),50)
        Size, baseline= cv2.getTextSize(flag, cv2.FONT_HERSHEY_SIMPLEX, 1,1)
        cv2.rectangle(self.road_image,textOrg,(textOrg[0] + Size[0],textOrg[1] -Size[1]), (0,0,0),Size[1])
        cv2.putText(self.road_image, flag, textOrg, cv2.FONT_HERSHEY_SIMPLEX, 1,(255,255,255),1, cv2.LINE_AA)
        #cv2.imshow('self.road_image',self.road_image)
        #cv2.waitKey(1)
        
        return self.road_image     