#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：颜色识别 
@File    ：霍夫变换检测圆trackbar调参.py
@IDE     ：PyCharm 
@Author  ：咋
@Date    ：2023/3/3 9:52 
"""
import cv2
import numpy as np
cv2.namedWindow("window",cv2.WINDOW_NORMAL)
cv2.resizeWindow("window",(640,480))
def decodeDisplay(video,param2,minRadius,maxRadius):
    gay_img = cv2.cvtColor(video, cv2.COLOR_BGRA2GRAY)
    img = cv2.medianBlur(gay_img, 7)  # 进行中值模糊，去噪点
    cimg = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
    circles = cv2.HoughCircles(img, cv2.HOUGH_GRADIENT, 1, 50, param1=100, param2=param2, minRadius=minRadius, maxRadius=maxRadius)
    if circles is not None:
        circles = np.uint16(np.around(circles))
        print(circles)
        for i in circles[0, :]:  # 遍历矩阵每一行的数据
            cv2.circle(video, (i[0], i[1]), i[2], (0, 255, 0), 2)
            cv2.circle(video, (i[0], i[1]), 2, (0, 0, 255), 3)
        return video
    else:
        return video
        # 如果识别不出，显示圆心不存在
        # print('x: None y: None')
        # cv2.imshow('frame', video)
image = cv2.imread("1.jpg")
def callback(value):
    print(value)

# 创建Trackbar控件
cv2.createTrackbar("param2","window",80,150,callback)
cv2.createTrackbar("minRadius","window",400,1000,callback)
cv2.createTrackbar("maxRadius","window",600,2000,callback)
while True:
    # 获取Trackbar控件的值
    param2 = cv2.getTrackbarPos("param2","window")
    minRadius = cv2.getTrackbarPos("minRadius","window")
    maxRadius = cv2.getTrackbarPos("maxRadius","window")
    # 用获取的值来生成图片
    image = decodeDisplay(image, param2, minRadius, maxRadius)
    # 显示图片
    cv2.imshow("window",image)
    if cv2.waitKey(1) == ord("q"):
        break
