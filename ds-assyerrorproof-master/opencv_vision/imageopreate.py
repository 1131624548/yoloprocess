import cv2
from matplotlib import pyplot as plt
from PIL import Image
import numpy as np
import os


def compute(path):
    # img = Convert(path)
    per_image_Rmean = []
    per_image_Gmean = []


    per_image_Bmean = []
    img = cv2.imread(path, 1)
    per_image_Bmean.append(np.mean(img[:,:,0]))
    per_image_Gmean.append(np.mean(img[:,:,1]))
    per_image_Rmean.append(np.mean(img[:,:,2]))
    R_mean = np.mean(per_image_Rmean)
    G_mean = np.mean(per_image_Gmean)
    B_mean = np.mean(per_image_Bmean)
    return R_mean, G_mean, B_mean

def erzhi(path):
    # 1.47 固定阈值二值变换
    img = cv2.imread(path)  # 读取彩色图像(BGR)
    imgGray = cv2.imread(path, flags=0)  # flags=0 读取为灰度图像
    # imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # 颜色转换：BGR(OpenCV) -> Gray

    # cv2.threshold(src, thresh, maxval, type[, dst]) → retval, dst
    ret1, img1 = cv2.threshold(imgGray, 70, 255, cv2.THRESH_BINARY)  # 转换为二值图像, thresh=63
    ret2, img2 = cv2.threshold(imgGray, 127, 255, cv2.THRESH_BINARY)  # 转换为二值图像, thresh=127
    ret3, img3 = cv2.threshold(imgGray, 191, 255, cv2.THRESH_BINARY)  # 转换为二值图像, thresh=191
    ret4, img4 = cv2.threshold(imgGray, 127, 255, cv2.THRESH_BINARY_INV)  # 逆二值图像，BINARY_INV
    ret5, img5 = cv2.threshold(imgGray, 127, 255, cv2.THRESH_TRUNC)  # TRUNC 阈值处理，THRESH_TRUNC
    ret6, img6 = cv2.threshold(imgGray, 127, 255, cv2.THRESH_TOZERO)  # TOZERO 阈值处理，THRESH_TOZERO
    ret7, img7 = cv2.threshold(imgGray, 127, 255, cv2.THRESH_TOZERO_INV)
    # imgGray[np.where((imgGray==[255,255,255]).all(axis=2))] = [0,0,0]
    ret8, img8 = cv2.threshold(img5, 70, 255, cv2.THRESH_BINARY)  # TRUNC 阈值处理，THRESH_TRUNC
    plt.figure(figsize=(9, 8))
    titleList = ["1. BINARY(thresh=63)", "2. BINARY(thresh=127)", "3. BINARY(thresh=191)", "4. THRESH_BINARY_INV", "5. THRESH_TRUNC", "6. THRESH_TOZERO","7.THRESH_TOZERO_INV","2. BINARY(thresh=200)"]
    imageList = [img1, img2, img3, img4, img5, img6,img7,img8]
    for i in range(8):
        plt.subplot(3, 3, i+1), plt.title(titleList[i]), plt.axis('off')
        plt.imshow(imageList[i], 'gray')  # 灰度图像 ndim=2
    plt.show()


def Convert(path):
    """
    将图像中白色像素转变为黑色像素
    """
    src = cv2.imread(path)
    height, width = src.shape[0:2]
    grayImg = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)

    cv2.imshow("gray1", grayImg)
    # 100 ---> 255 - 100 = 155
    for row in range(height):
        for col in range(width):
            value = grayImg[row, col]
            grayImg[row, col] = 255 - value

    # cv2.imshow("gray2", grayImg)
    # cv2.imshow("src", src)
    # cv2.waitKey()
    return grayImg


def heibai(path):

    img = cv2.imread(path)  # 读取图片
    print(img.shape)
    w, h = img.shape[:2]  # 获取长宽
    print(w, h)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # 变为灰度图
    ret, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)  ## 阈值分割得到二值化图片
    # cv2.namedWindow('binary', cv2.WINDOW_AUTOSIZE)
    # cv2.imshow('binary', binary)
    # cv2.waitKey(0)

    # binary = binary > 2  # 得到图片通道的逻辑值

    '''
    [[False False False ... False False False]
     [False False False ... False False False]
     [False False False ... False False False]
     ...
     [False False False ... False False False]
     [False False False ... False False False]
     [False False False ... False False False]]
    '''
    # 创建全为0的背景图
    img[np.where((img == [255, 255, 255]).all(axis=2))] = [0, 0, 0];
    # fg_image = np.zeros(img.shape[:-1], dtype=np.uint8)
    # 创建全为255的背景图
    # fg_image2 = np.ones(img.shape[:-1], dtype=np.uint8) * 255

    # FG_img = np.where(binary, fg_image,fg_image2)  # 参数1为Ture返回参数2，否则参数3
    # print(FG_img)
    cv2.namedWindow('FG_img', cv2.WINDOW_AUTOSIZE)
    cv2.imshow('FG_img', img)
    cv2.waitKey(0)




if __name__ == "__main__":
    path = r"E:\data\dataset\qiruidata\cam2\2022_4_9_11_8_35_dev2.bmp"
    # Convert(path)
    erzhi(path)
    # 像素方法
    # 隐私玻璃 25.635854341736696 25.53096238495398 27.428371348539414，39.59288220551378 41.13609022556391 41.15563909774436
    # 非隐私玻璃 40.372859488623035 39.68062397372742 38.697982641332395，60.80448437321558 67.2569188016293 70.06737980128669
    # a,b,c = compute(path)

    # print(a,b,c)
pass
