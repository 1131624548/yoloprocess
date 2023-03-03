import cv2
import numpy as np

import cv2

def cann(path):
    # imread()两个参数：
    # 1、图片路径。
    # 2、读取图片的形式（1：默认值，加载彩色图片。 0：加载灰度图片。 -1：加载原图片）
    img = cv2.imread(path)
    cv2.imshow('img', img)

    ret, thresh1 = cv2.threshold(img, 80, 255, cv2.THRESH_BINARY)    # 阈值分割，黑白二值
    ret, thresh2 = cv2.threshold(thresh1, 80, 255, cv2.THRESH_BINARY_INV)    # （黑白二值反转）

    cv2.imshow('img1', thresh1)
    cv2.imshow('img2', thresh2)

    # Canny算子是双阈值，所以需要指定两个阈值，阈值越小，边缘越丰富。
    img3 = cv2.Canny(img, 70, 255)
    # 对img3图像进行反转
    img4 = cv2.bitwise_not(img3)
    cv2.imshow('img4', img4)

    cv2.waitKey()
    # 关闭窗口并取消分配任何相关的内存使用
    cv2.destroyAllWindows()



def CannyThreshold(lowThreshold):
    detected_edges = cv2.GaussianBlur(gray, (3, 3), 0)
    detected_edges = cv2.Canny(detected_edges,
                               lowThreshold,
                               lowThreshold * ratio,
                               apertureSize=kernel_size)
    dst = cv2.bitwise_and(img, img, mask=detected_edges)  # just add some colours to edges from original image.
    cv2.imshow('canny demo', dst)

if __name__=="__main__":
    path = r"E:\data\dataset\qiruidata\cam2\2022_4_9_11_8_35_dev2.bmp"
    # cann(path)
    lowThreshold = 0
    max_lowThreshold = 200
    ratio = 4
    kernel_size = 3

    img = cv2.imread(path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    cv2.namedWindow('canny demo')

    cv2.createTrackbar('Min threshold', 'canny demo', lowThreshold, max_lowThreshold, CannyThreshold)

    CannyThreshold(0)  # initialization
    if cv2.waitKey(0) == 27:
        cv2.destroyAllWindows()
