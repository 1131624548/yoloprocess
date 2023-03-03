'''
Descripttion:霍夫变换
version: 1.0
Author: xiaoxuesheng
Date: 2023-03-03 17:44:15
LastEditors:  *****
LastEditTime: *****
'''

# encoding:utf-8

import os 
import cv2 as cv
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
tirepath = r"E:\workspace\qr\tyre"
save_dir =r"E:\workspace\corptire" # 图片和标签在同一个文件夹中
if not os.path.exists(save_dir):
    os.makedirs(save_dir)

j=0
for file in os.listdir(tirepath):
       filename = os.path.join(tirepath,file)
       
       #这里将bmp图事先转为jpg，如不满足需求，需在此提前读取bmp的位图数据，在进行后期运算
       src = cv.imread(filename)
       img = src.copy()
       im = Image.open(filename)

       #将原图转为灰度图
       img_gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
       # 进行中值滤波，经过多次尝试，滤波核大小设置为5效果较好
       dst_img = cv.medianBlur(img_gray,5)
       # 霍夫圆检测在调用时，同心圆的圆心距离设置在200，边缘检测算子90，累加器85效果较好，但在选择性调整圆半径设定时，参数设置与预期不符这里使用默认值
       circle = cv.HoughCircles(dst_img, cv.HOUGH_GRADIENT, 1, 100,param1=100, param2=90, minRadius=0, maxRadius=0)
       print(circle)
       try:
       # 将检测结果绘制在图像上
              for i in circle[0, :]: # 遍历矩阵的每一行的数据
                     cv.circle(img, (int(i[0]), int(i[1])), int(i[2]), (0, 255, 0),3,-1) # 绘制圆形  
                     cv.circle(img, (int(i[0]), int(i[1])), 10, (255, 0, 255), -1)  # 绘制圆心
                     
                     #左上
                     left = int(i[0]) - int(i[2])
                     upper = int(i[0]) + int(i[2])
                     right = int(i[1]) - int(i[2])
                     lower = int(i[1]) + int(i[2])
                     im = im.crop((left,upper,right,lower)) # 对图片进行切割 im.crop(top_x, top_y, bottom_x, bottom_y) 表示为坐标是 (left, upper, right, lower)
                     im.save( os.path.join(save_dir,file))
                     #im.show()
                     #print((left,upper,right,lower))
       except:
              j=j+1 
              print('有%d张图没有被检测到'%(j))
       #显示图像
       fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(10, 8), dpi=100)
       axes[0].imshow(src[:, :, ::-1])
       axes[0].set_title("原图")
       axes[1].imshow(img[:, :, ::-1])
       axes[1].set_title("霍夫圆检测后的图像")
       plt.show()

# import cv2
# import numpy as np
# def decodeDisplay(video):
#     gay_img = cv2.cvtColor(video, cv2.COLOR_BGRA2GRAY)
#     img = cv2.medianBlur(gay_img, 7)  # 进行中值模糊，去噪点
#     cimg = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
#     circles = cv2.HoughCircles(img, cv2.HOUGH_GRADIENT, 1, 50, param1=100, param2=80, minRadius=400, maxRadius=600)
#     if circles is not None:
#         circles = np.uint16(np.around(circles))
#         print(circles)
#         for i in circles[0, :]:  # 遍历矩阵每一行的数据
#             cv2.circle(video, (i[0], i[1]), i[2], (0, 255, 0), 2)
#             cv2.circle(video, (i[0], i[1]), 2, (0, 0, 255), 3)
#         cv2.imshow("image",video)
#         cv2.waitKey(0)
#     else:
#         return video
#         # 如果识别不出，显示圆心不存在
#         # print('x: None y: None')
#         # cv2.imshow('frame', video)
# image = cv2.imread(r"E:\workspace\qr\tyre1\Image_20210916155400421.jpg")
# decodeDisplay(image)



# import cv2
# import numpy as np
# import matplotlib.pyplot as plt
# import os

# # #opencv模板匹配----单目标匹配
# # import cv2
# # #读取目标图片
# # target = cv2.imread(r'E:\workspace\qr\tyre1\Image_20210916155400421.jpg')
# # #读取模板图片
# # template = cv2.imread(r'E:\workspace\qr\temptire.png')
# # #获得模板图片的高宽尺寸
# # theight, twidth = template.shape[:2]
# # #执行模板匹配，采用的匹配方式cv2.TM_SQDIFF_NORMED
# # result = cv2.matchTemplate(target,template,cv2.TM_SQDIFF_NORMED)
# # #归一化处理
# # cv2.normalize( result, result, 0, 1, cv2.NORM_MINMAX, -1 )
# # #寻找矩阵（一维数组当做向量，用Mat定义）中的最大值和最小值的匹配结果及其位置
# # min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
# # #匹配值转换为字符串
# # #对于cv2.TM_SQDIFF及cv2.TM_SQDIFF_NORMED方法min_val越趋近与0匹配度越好，匹配位置取min_loc
# # #对于其他方法max_val越趋近于1匹配度越好，匹配位置取max_loc
# # strmin_val = str(min_val)
# # #绘制矩形边框，将匹配区域标注出来
# # #min_loc：矩形定点
# # #(min_loc[0]+twidth,min_loc[1]+theight)：矩形的宽高
# # #(0,0,225)：矩形的边框颜色；2：矩形边框宽度
# # cv2.rectangle(target,min_loc,(min_loc[0]+twidth,min_loc[1]+theight),(0,0,225),2)
# # #显示结果,并将匹配值显示在标题栏上
# # cv2.imshow("MatchResult----MatchingValue="+strmin_val,target)
# # cv2.waitKey()
# # cv2.destroyAllWindows()




# # import cv2
# # import numpy as np
# # img_rgb = cv2.imread(r'E:\workspace\qr\tyre1\Image_20210916155400421.jpg')
# # img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
# # template = cv2.imread(r'E:\workspace\qr\temptire.png', 0)
# # h, w = template.shape[:2]
 
# # res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
# # threshold = 0.3
# # # 取匹配程度大于%80的坐标
# # loc = np.where(res >= threshold)
# # #np.where返回的坐标值(x,y)是(h,w)，注意h,w的顺序
# # for pt in zip(*loc[::-1]):  
# #     bottom_right = (pt[0] + w, pt[1] + h)
# #     cv2.rectangle(img_rgb, pt, bottom_right, (0, 0, 255), 2)
# # cv2.imwrite("img.jpg",img_rgb)
# # cv2.imshow('img', img_rgb)
# # cv2.waitKey(0)







# # # 图片的路径
# # bmp_dir = r'E:\workspace\qr\tyre'
# # jpg_dir = r'E:\workspace\qr\tyre1'

# # filelists = os.listdir(bmp_dir)

# # for i,file in enumerate(filelists):
# #     # 读图，-1为不改变图片格式，0为灰度图  
# #     img = cv2.imread(os.path.join(bmp_dir,file),-1)
# #     newName = file.replace('.bmp','.jpg')
# #     cv2.imwrite(os.path.join(jpg_dir,newName),img)
# #     print('第%d张图：%s'%(i+1,newName))


