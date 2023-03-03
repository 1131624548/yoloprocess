'''
Descripttion:霍夫变换
version: 1.0
Author: xiaoxuesheng
Date: 2023-02-28 14:51:15
LastEditors:  *****
LastEditTime: *****
'''

# -*- coding: utf-8 -*-
import cv2
import numpy as np
import matplotlib.pyplot as plt

class shapeDetect():
    def __init__(self,imagepath):
        self.imgpath = imagepath

    def canny(self):
        # 载入并显示图片
        img = cv2.imread(self.imgpath)
        # cv2.imshow('1', img)
        # 降噪（模糊处理用来减少瑕疵点）
        result = cv2.blur(img, (5, 5))
        # cv2.imshow('2', result)
        # 灰度化,就是去色（类似老式照片）
        gray = cv2.cvtColor(result, cv2.COLOR_BGR2GRAY)
        # cv2.imshow('3', gray)
        # param1的具体实现，用于边缘检测
        canny = cv2.Canny(gray, 40, 80)
        plt.imshow(canny), plt.title('canny'),
        plt.axis('off')
        plt.show()
        # cv2.imshow('4', canny)
        # 按任意键退出
        # cv2.waitKey(0)

    def canny_circle(self):
        # 载入并显示图片
        img = cv2.imread(self.imgpath)
        # cv2.imshow('1', img)
        # 降噪（模糊处理用来减少瑕疵点）
        result = cv2.blur(img, (5, 5))
        # cv2.imshow('2', result)
        # 灰度化,就是去色（类似老式照片）
        gray = cv2.cvtColor(result, cv2.COLOR_BGR2GRAY)
        # cv2.imshow('3', gray)
        # param1的具体实现，用于边缘检测
        canny = cv2.Canny(img, 40, 80)
        # cv2.imshow('4', canny)
        # 霍夫变换圆检测
        # circles_1 = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1, 500, param1=80, param2=30, minRadius=180, maxRadius=250)
        circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1, 500, param1=80, param2=30, minRadius=240, maxRadius=410)
        # 输出返回值，方便查看类型
        # circles = [circles_1, circles_2]
        print(circles)

        # 输出检测到圆的个数
        print('-------------圆个数-----------------', len(circles[0]))

        print('-------------画圆-----------------')
        # 根据检测到圆的信息，画出每一个圆
        for circle in circles[0]:
            # 圆的基本信息
            print('-------------半径-----------------', circle[2])
            # 坐标行列(就是圆心)
            x = int(circle[0])
            y = int(circle[1])
            # 半径
            r = int(circle[2])
            # 在原图用指定颜色圈出圆，参数设定为int所以圈画存在误差
            print(x,y,r)
            img = cv2.circle(img, (x, y), r, (0, 0, 255), 5, 8, 0)
        # 显示新图像
        cv2.imshow('5', img)

        # 按任意键退出
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def easy_circle(self):
        # -*- coding: utf-8 -*-
        """
        Created on Tue Sep 26 23:15:39 2017
        @author: tina
        """
        img = cv2.imread(self.imgpath)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # plt.subplot(121), plt.imshow(gray, 'gray')
        # plt.xticks([]), plt.yticks([])

        circles1 = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1,600, param1=100, param2=30, minRadius=200, maxRadius=280)
        # circles1 = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1, 600, param1=50, param2=20, minRadius=155, maxRadius=280)
        circles = circles1[0, :, :]
        circles = np.uint16(np.around(circles))
        for i in circles[0]:
            cv2.circle(img, (i[0], i[1]), i[2], (255, 0, 0), 5)
            # cv2.circle(img, (i[0], i[1]), 2, (255, 0, 255), 10)
            # cv2.rectangle(img, (i[0] - i[2], i[1] + i[2]), (i[0] + i[2], i[1] - i[2]), (255, 255, 0), 5)
        print("圆心坐标", i[0], i[1])
        plt.subplot(122), plt.imshow(img)
        plt.xticks([]), plt.yticks([])
        plt.show()

    # 图像处理，获取图片最大内接圆，其他区域置为透明
    def img_deal(self,input_img):
        # cv2.IMREAD_COLOR，读取BGR通道数值，即彩色通道，该参数为函数默认值
        # cv2.IMREAD_UNCHANGED，读取透明（alpha）通道数值
        # cv2.IMREAD_ANYDEPTH，读取灰色图，返回矩阵是两维的
        img = cv2.imread(input_img, cv2.IMREAD_UNCHANGED)
        rows, cols, channel = img.shape
        # cols = 188
        # rows = 191
        # 创建一张4通道的新图片，包含透明通道，初始化是透明的
        img_new = np.zeros((rows, cols, 4), np.uint8)
        img_new[:, :, 0:3] = img[:, :, 0:3]

        # 190.5
        # 194.5
        # 创建一张单通道的图片，设置最大内接圆为不透明，注意圆心的坐标设置，cols是x坐标，rows是y坐标
        img_circle = np.zeros((rows, cols, 1), np.uint8)
        img_circle[:, :, :] = 0  # 设置为全透明
        img_circle = cv2.circle(img_circle, (177, 183), 180, (255), -1)  # 设置最大内接圆为不透明
        # 图片融合
        img_new[:, :, 3] = img_circle[:, :, 0]
        # 保存图片
        cv2.imwrite(input_img + ".png", img_new)
        # cv2.imencode('.jpg', img)[1].tofile('./9.jpg')  # 保存到另外的位置

        # 显示图片，调用opencv展示
        # cv2.imshow("img_new", img_new)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()

        # 显示图片，调用matplotlib.pyplot展示
        plt.subplot(121), plt.imshow(self.img_convert(img), cmap='gray'), plt.title('IMG')
        plt.subplot(122), plt.imshow(self.img_convert(img_new), cmap='gray'), plt.title('IMG_NEW')
        plt.show()

    # cv2与matplotlib的图像转换，cv2是bgr格式，matplotlib是rgb格式
    def img_convert(self, cv2_img):
        # 灰度图片直接返回
        if len(cv2_img.shape) == 2:
            return cv2_img
        # 3通道的BGR图片
        elif len(cv2_img.shape) == 3 and cv2_img.shape[2] == 3:
            b, g, r = cv2.split(cv2_img)
            return cv2.merge((r, g, b))
        # 4通道的BGR图片
        elif len(cv2_img.shape) == 3 and cv2_img.shape[2] == 4:
            b, g, r, a = cv2.split(cv2_img)
            return cv2.merge((r, g, b, a))
        # 未知图片格式
        else:
            return cv2_img

    def rectangleDetect(self,**kwargs):
        cropped_zst, cropped_hsj, cropped_dh = None, None, None
        #img_list = [装饰条, 后视镜, 门把手]
        #crop_list [y0,y1,x0,x1]
        #装饰条
        zst = kwargs.get("zst", None)
        img = cv2.imread(self.imgpath)
        if zst:
            crop_list = [1500,2000, 560,3800]
            cropped_zst = img[crop_list[0]:crop_list[1], crop_list[2]:crop_list[3]]
        #后视镜
        hsj = kwargs.get("hsj",None)
        if hsj:
            crop_list = [1500,2000, 560,3800]
            cropped_hsj = img[crop_list[0]:crop_list[1], crop_list[2]:crop_list[3]]
        #门把手
        dh = kwargs.get("dh",None)
        if dh:
            crop_list = [1500,2000, 560,3800]
            cropped_dh = img[crop_list[0]:crop_list[1], crop_list[2]:crop_list[3]]
        img_list = [cropped_zst, cropped_hsj, cropped_dh]
        print(img.shape)
        cropped = img[1500:2000, 560:3800]  # 裁剪坐标为[y0:y1, x0:x1]
        plt.imshow(cropped), plt.title('cropped'),
        # result = cv2.blur(img, (5, 5))
        # cv2.imshow('2', result)
        # 灰度化,就是去色（类似老式照片）
        # gray = cv2.cvtColor(cropped, cv2.COLOR_BGR2GRAY)
        # cv2.imshow('3', gray)
        # param1的具体实现，用于边缘检测
        # canny = cv2.Canny(gray, 40, 80)
        # plt.imshow(canny), plt.title('canny'),
        plt.axis('off')
        plt.show()
        # cv2.imwrite(r"E:\data\car_hub\zhuangshi/1.jpg", cropped)
        return img_list





if __name__=="__main__":
    image_path = r"E:\workspace\qr\qrlt\Image_20210916155402941.bmp"
    # image_path = r"E:\xunfei\LVVDB11B1MD324953\right.jpg"
    server = shapeDetect(image_path)
    server.canny_circle()
    # server.rectangleDetect()
    # server.easy_circle()



# # encoding:utf-8

# import os 
# import cv2 as cv
# import matplotlib.pyplot as plt
# import numpy as np
# from PIL import Image
# tirepath = r"E:\workspace\qr\tyre"
# save_dir =r"E:\workspace\corptire" # 图片和标签在同一个文件夹中
# if not os.path.exists(save_dir):
#     os.makedirs(save_dir)




# j=0
# for file in os.listdir(tirepath):
#        filename = os.path.join(tirepath,file)
       
#        #这里将bmp图事先转为jpg，如不满足需求，需在此提前读取bmp的位图数据，在进行后期运算
#        src = cv.imread(filename)
#        img = src.copy()
#        im = Image.open(filename)

#        #将原图转为灰度图
#        img_gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
#        # 进行中值滤波，经过多次尝试，滤波核大小设置为5效果较好
#        dst_img = cv.medianBlur(img_gray,5)
#        # 霍夫圆检测在调用时，同心圆的圆心距离设置在200，边缘检测算子90，累加器85效果较好，但在选择性调整圆半径设定时，参数设置与预期不符这里使用默认值
#        circle = cv.HoughCircles(dst_img, cv.HOUGH_GRADIENT, 1, 100,param1=100, param2=90, minRadius=0, maxRadius=0)
#        print(circle)
#        try:
#        # 将检测结果绘制在图像上
#               for i in circle[0, :]: # 遍历矩阵的每一行的数据
#                      cv.circle(img, (int(i[0]), int(i[1])), int(i[2]), (0, 255, 0),3,-1) # 绘制圆形  
#                      cv.circle(img, (int(i[0]), int(i[1])), 10, (255, 0, 255), -1)  # 绘制圆心
                     
#                      #左上
#                      left = int(i[0]) - int(i[2])
#                      upper = int(i[0]) + int(i[2])
#                      right = int(i[1]) - int(i[2])
#                      lower = int(i[1]) + int(i[2])
#                      im = im.crop((left,upper,right,lower)) # 对图片进行切割 im.crop(top_x, top_y, bottom_x, bottom_y) 表示为坐标是 (left, upper, right, lower)
#                      im.save( os.path.join(save_dir,file))
#                      #im.show()
#                      #print((left,upper,right,lower))
#        except:
#               j=j+1 
#               print('有%d张图没有被检测到'%(j))
       # #显示图像
       # fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(10, 8), dpi=100)
       # axes[0].imshow(src[:, :, ::-1])
       # axes[0].set_title("原图")
       # axes[1].imshow(img[:, :, ::-1])
       # axes[1].set_title("霍夫圆检测后的图像")
       # plt.show()

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

# src = cv2.imread(r'E:\workspace\qr\tyre1\Image_20210916155400421.jpg')


# img =src.copy



# # cv2.imshow('img',img)
# # cv2.waitKey(0)

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


