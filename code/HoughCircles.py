'''
Descripttion:霍夫变换
version: 1.0
Author: xiaoxuesheng
Date: 2023-02-28 14:51:15
LastEditors:  *****
LastEditTime: *****
'''
# encoding:utf-8
import cv2
import numpy as np
import matplotlib.pyplot as plt
import os


# # 图片的路径
# bmp_dir = r'E:\workspace\qr\tyre'
# jpg_dir = r'E:\workspace\qr\tyre1'

# filelists = os.listdir(bmp_dir)

# for i,file in enumerate(filelists):
#     # 读图，-1为不改变图片格式，0为灰度图  
#     img = cv2.imread(os.path.join(bmp_dir,file),-1)
#     newName = file.replace('.bmp','.jpg')
#     cv2.imwrite(os.path.join(jpg_dir,newName),img)
#     print('第%d张图：%s'%(i+1,newName))

img = cv2.imread(r'E:\workspace\qr\tyre1\Image_20210916155400421.jpg')


#读取原始图片
# src = cv2.imread(r'E:\workspace\qr\tyre1\Image_20210916155400421.jpg')
# #图像灰度化处理
# grayImage = cv2.cvtColor(src,cv2.COLOR_BGR2GRAY)
# #显示图像
# cv2.imshow("src", src)
# cv2.imshow("result", grayImage)
# #等待显示
# cv2.waitKey(0)
# cv2.destroyAllWindows()

#获取图像高度和宽度
height = img.shape[0]
width = img.shape[1]
#创建一幅图像
grayimg = np.zeros((height, width, 3), np.uint8)

#图像平均灰度处理方法
for i in range(height):
 for j in range(width):
 #灰度值为RGB三个分量的平均值
        gray = (int(img[i,j][0]) + int(img[i,j][1]) + int(img[i,j][2])) / 3
 grayimg[i,j] = np.uint8(gray)
#显示图像
cv2.imshow("src", img)
cv2.imshow("gray", grayimg)
#等待显示
cv2.waitKey(0)
cv2.destroyAllWindows()



# cv2.imshow('img',img)
# cv2.waitKey(0)

# img = cv2.medianBlur(img,5)
# gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # 灰度图像
# plt.subplot(121), plt.imshow(gray, cmap='gray')
# plt.title('img'), plt.xticks([]), plt.yticks([])
# circle1 = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1, 100, param1=50, param2=50, minRadius=500, maxRadius=800)  #把半径范围缩小点，检测内圆，瞳孔
# print(circle1)
# circles = circle1[0, :, :]  # 提取为二维
# circles = np.uint16(np.around(circles))  # 四舍五入，取整
# for i in circles[:]:
#     cv2.circle(img, (i[0], i[1]), i[2], (255, 0, 0), 5)  # 画圆
#     cv2.circle(img, (i[0], i[1]), 2, (255, 0, 0), 10)  # 画圆心

# plt.subplot(122), plt.imshow(img)
# plt.title('circle'), plt.xticks([]), plt.yticks([])
# plt.show()


