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
    image_path = r"E:\data\dataset\qiruidata\cam6\2022_4_9_11_5_40_dev6.bmp"
    # image_path = r"E:\xunfei\LVVDB11B1MD324953\right.jpg"
    server = shapeDetect(image_path)
    server.canny_circle()
    # server.rectangleDetect()
    # server.easy_circle()