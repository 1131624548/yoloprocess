# Descripttion:CropYoloTarget
# version: 1.0 
# Author: xiaoxuesheng
# Date: 2023-05-04 10:53:53
# LastEditors:  *****
# LastEditTime: *****
# import time
# print(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))
# -*- coding: utf-8 -*-


#Acording YOLO label txt  crop Detection 
import os # 多种操作系统接口

import cv2 # opencv 
from tqdm import tqdm # tqdm 库 
 
image_input = r'E:\workspace\datasets\20230428\images/'# image
txt_input = r'E:\workspace\datasets\20230428\labels/'# txt
path_output = r"E:\workspace\20230504"    # 裁剪出来的小图保存的根目录
class_names_path = r'E:\workspace\datasets\classes.txt' # 标签
 
img_total = [] 
txt_total = []
 
def read_class_name(path):        #读取path下的类别数
    f = open(path,'r')
    classes_name = []
    for i in f.readlines():
        classes_name.append(i.strip())
    return classes_name
classes_name = read_class_name(class_names_path)
 
file_image = os.listdir(image_input)
for filename in file_image:#jpg文件名列表
     first,last = os.path.splitext(filename) # 	分割路径中的文件名与拓展名
     img_total.append(first)
 
file_txt = os.listdir(txt_input)
for filename in file_txt:# txt文件名列表
     first,last = os.path.splitext(filename) # 	分割路径中的文件名与拓展名
     txt_total.append(first)
 
for img_ in tqdm(img_total):
    if img_ in txt_total:
        filename_img = img_+".jpg"
        path1 = os.path.join(image_input,filename_img)
        img = cv2.imread(path1)
        filename_txt = img_+'.txt'     #预测出来的txt文件没有后缀名，有则加 {+".txt"}
        h = img.shape[0]
        w = img.shape[1]
        n = 1
        with open(os.path.join(txt_input,filename_txt),"r+",encoding="utf-8",errors="ignore") as f:
            for line in f:
                aa = line.split(" ")
                # if not int(aa[0]) == 0: continue     #判断需要裁剪的类别:0--vehicle
                x_center = w * float(aa[1])       # aa[1]左上点的x坐标
                y_center = h * float(aa[2])       # aa[2]左上点的y坐标
                width = int(w*float(aa[3]))       # aa[3]图片width
                height = int(h*float(aa[4]))      # aa[4]图片height
                lefttopx = int(x_center-width/2.0)
                lefttopy = int(y_center-height/2.0)
                roi = img[lefttopy+1:lefttopy+height+3,lefttopx+1:lefttopx+width+1] # [左上y:右下y,左上x:右下x]
                                                                          # (y1:y2,x1:x2)需要调参，否则裁剪出来的小图可能不太好
                if roi.size == 0: continue
                filename_last = img_+"_"+str(n)+".jpg"      # 裁剪出来的小图文件名
                x = int(aa[0])
                path2 = os.path.join(path_output,classes_name[x])           # 需要在path_output路径下创建一个cut_txt文件夹
                if not os.path.exists(path2):
                    os.mkdir(path2)
                # print('path2:', path2)                    # 裁剪小图的保存位置
                cv2.imwrite(os.path.join(path2,filename_last),roi)
                n = n+1
    else:
         continue
