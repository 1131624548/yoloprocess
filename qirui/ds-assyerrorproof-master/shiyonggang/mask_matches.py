# -*- coding:utf-8 -*-
import cv2
import numpy as np
from matplotlib import pyplot as plt

img = cv2.imread(r"E:\workspace\data\tyre\Image_20210916155400421.jpg",0)
img2 = img.copy()
template = cv2.imread( r"E:\workspace\data\tirecrop.jpg",0)
w,h = template.shape[::-1]

# 6 个匹配效果对比算法
methods = ['cv2.TM_CCOEFF', 'cv2.TM_CCOEFF_NORMED', 'cv2.TM_CCORR',
           'cv2.TM_CCORR_NORMED', 'cv2.TM_SQDIFF', 'cv2.TM_SQDIFF_NORMED'] 
# CV_TM_CCOEFF 相关系数匹配法：利用模板与图像间的相关系数匹配，1表示完美的匹配，-1表示最差的匹配。
# CV_TM_CCOEFF_NORMED归一化相关系数匹配法。
# CV_TM_CCORR    相关匹配法：利用模板与图像间的乘法进行匹配，数值越大表示匹配程度较高，越小表示匹配效果差。
# CV_TM_CCORR_NORMED 归一化相关匹配法。
# CV_TM_SQDIFF 平方差匹配法：利用模板与图像之间的平方差进行匹配，最好的匹配是0，匹配越差，匹配的值越大。
# CV_TM_SQDIFF_NORMED 归一化平方差匹配法。


for meth in methods:
    img = img2.copy()

    method = eval(meth) # 去掉引号

    res = cv2.matchTemplate(img,template,method)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

    if method in [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]:
        top_left = min_loc
    else:
        top_left = max_loc
    bottom_right = (top_left[0] + w, top_left[1] + h)

    cv2.rectangle(img,top_left, bottom_right, 255, 2)

   #  print(meth)
    plt.subplot(221), plt.imshow(img2,cmap= "gray")
    plt.title('Original Image'), plt.xticks([]),plt.yticks([])
    plt.subplot(222), plt.imshow(template,cmap= "gray")
    plt.title('template Image'),plt.xticks([]),plt.yticks([])
    plt.subplot(223), plt.imshow(res,cmap= "gray")
    plt.title('Matching Result'), plt.xticks([]),plt.yticks([])
    plt.subplot(224), plt.imshow(img,cmap= "gray")
    plt.title('Detected Point'),plt.xticks([]),plt.yticks([])
    plt.show()
