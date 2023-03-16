import numpy as np
import collections
import cv2

# 定义字典存放颜色分量上下限
# 例如：{颜色: [min分量, max分量]}
# {'red': [array([160, 43, 46]), array([179, 255, 255])]}

def getColorList():
    dict = collections.defaultdict(list)
    # 黑色
    lower_black = np.array([0, 0, 0])
    upper_black = np.array([180, 255, 46])
    color_list = []
    color_list.append(lower_black)
    color_list.append(upper_black)
    dict['black'] = color_list

    #灰色
    lower_gray = np.array([0, 0, 46])
    upper_gray = np.array([180, 43, 220])
    color_list = []
    color_list.append(lower_gray)
    color_list.append(upper_gray)
    dict['gray'] = color_list

    # 白色
    lower_white = np.array([0, 0, 221])
    upper_white = np.array([180, 30, 255])
    color_list = []
    color_list.append(lower_white)
    color_list.append(upper_white)
    dict['white'] = color_list

    # 红色
    lower_red = np.array([156, 43, 46])
    upper_red = np.array([180, 255, 255])
    color_list = []
    color_list.append(lower_red)
    color_list.append(upper_red)
    dict['red'] = color_list

    # 红色2
    lower_red = np.array([0, 43, 46])
    upper_red = np.array([10, 255, 255])
    color_list = []
    color_list.append(lower_red)
    color_list.append(upper_red)
    dict['red2'] = color_list

    # 橙色
    lower_orange = np.array([11, 43, 46])
    upper_orange = np.array([25, 255, 255])
    color_list = []
    color_list.append(lower_orange)
    color_list.append(upper_orange)
    dict['orange'] = color_list

    # 黄色
    lower_yellow = np.array([26, 43, 46])
    upper_yellow = np.array([34, 255, 255])
    color_list = []
    color_list.append(lower_yellow)
    color_list.append(upper_yellow)
    dict['yellow'] = color_list

    # 绿色
    lower_green = np.array([35, 43, 46])
    upper_green = np.array([77, 255, 255])
    color_list = []
    color_list.append(lower_green)
    color_list.append(upper_green)
    dict['green'] = color_list

    # 青色
    lower_cyan = np.array([78, 43, 46])
    upper_cyan = np.array([99, 255, 255])
    color_list = []
    color_list.append(lower_cyan)
    color_list.append(upper_cyan)
    dict['cyan'] = color_list

    # 蓝色
    lower_blue = np.array([100, 43, 46])
    upper_blue = np.array([124, 255, 255])
    color_list = []
    color_list.append(lower_blue)
    color_list.append(upper_blue)
    dict['blue'] = color_list

    # 紫色
    lower_purple = np.array([125, 43, 46])
    upper_purple = np.array([155, 255, 255])
    color_list = []
    color_list.append(lower_purple)
    color_list.append(upper_purple)
    dict['purple'] = color_list
    return dict

# 处理图片
def get_color(filename):
    if isinstance(filename,str):
        frame = cv2.imread(filename)
    else:
        frame = filename
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    maxsum = -100
    color = None
    color_dict = getColorList()
    for d in color_dict:
        mask = cv2.inRange(hsv, color_dict[d][0], color_dict[d][1]) # hsv指的是原图；第二个参数指的是图像中低于这个参数的值，图像值变为0；第三个参数指的是图像中低于这个参数的值，图像值变为0；而在第二个第三个参数之间的值变成255
        # cv2.imwrite(d + '.jpg', mask)
        binary = cv2.threshold(mask, 127, 255, cv2.THRESH_BINARY)[1]
        binary = cv2.dilate(binary, None, iterations=2) #膨胀处理
        img, cnts, hiera = cv2.findContours(binary.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) #  cv2.RETR_EXTERNAL 只寻找最高层级的轮廓  cv.CHAIN_APPROX_SIMPLE 两个端点
        # cv2.drawContours(img, cnts, -1, (0, 0, 255), 3) # 绘制所有图像
        # cv2.imshow("img", mask)
        # cv2.waitKey(0)
        sum = 0
        for c in cnts:
            sum += cv2.contourArea(c)
        if sum > maxsum:

            maxsum = sum
            color = d
    return color




if __name__ == '__main__':
    # filename = r'C:\Users\Dell\Desktop\car_error_img\11jpg.png'
    filename = r'E:\data\car_hub\zhuangshi\1.jpg'
    color = get_color(filename)
    print("----颜色-----",color)