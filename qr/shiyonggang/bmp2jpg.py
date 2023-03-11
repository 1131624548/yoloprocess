'''
Descripttion:bmp2jpg in one file
version: 1.0
Author: xiaoxuesheng
Date: 2023-03-06 13:41:15
LastEditors:  *****
LastEditTime: *****
'''
# -*- coding: utf-8 -*-

import os 
import cv2 

# 图片的路径
bmp_dir = r'E:\workspace\qr\tyre'
jpg_dir = r'E:\workspace\qr\tyre1'
if not os.path.exists(jpg_dir):
    os.makedirs(jpg_dir)

filelists = os.listdir(bmp_dir)

for i,file in enumerate(filelists):
    # 读图，-1为不改变图片格式，0为灰度图  
    img = cv2.imread(os.path.join(bmp_dir,file),-1)
    newName = file.replace('.bmp','.jpg')
    cv2.imwrite(os.path.join(jpg_dir,newName),img)
    print('第%d张图：%s'%(i+1,newName))
 