#coding:utf8
import datetime
import cv2
from opencv_vision.color_recongnzie import get_color

starttime = datetime.datetime.now()

def canny_circle(imgpath):
    [x, y] = [0, 0]
    r = 0
    # 载入并显示图片
    img = cv2.imread(imgpath)
    # 降噪（模糊处理用来减少瑕疵点）
    result = cv2.blur(img, (5, 5))
    # 灰度化,就是去色（类似老式照片）
    gray = cv2.cvtColor(result, cv2.COLOR_BGR2GRAY)
    # 霍夫变换圆检测
    circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1, 500, param1=80, param2=30, minRadius=150, maxRadius=250)
    # 输出返回值，方便查看类型
    print(circles)
    # 输出检测到圆的个数
    print('-------------圆个数-----------------', len(circles[0]))
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
        print(x, y, r)
        # circle_img = cv2.circle(img, (x, y), r, (0, 0, 255), 5, 8, 0)
    # 显示新图像
    # cv2.imshow('5', circle_img)
    crop_img = get_square(img, r, [x, y])
    color = get_color(crop_img)
    cv2.imshow('5', crop_img)
    # 按任意键退出
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    return color

"""
# 图像处理，获取图片最大内接圆，其他区域置为透明
def img_deal(input_img):
    # cv2.IMREAD_COLOR，读取BGR通道数值，即彩色通道，该参数为函数默认值
    # cv2.IMREAD_UNCHANGED，读取透明（alpha）通道数值
    # cv2.IMREAD_ANYDEPTH，读取灰色图，返回矩阵是两维的
    img = cv2.imread(input_img, cv2.IMREAD_UNCHANGED)
    rows, cols, channel = img.shape
    # cols = 188
    # rows = 191
    # 创建一张4通道的新图片，包含透明通道，初始化是透明的
    img_new = np.zeros((rows,cols,4),np.uint8)
    img_new[:,:,0:3] = img[:,:,0:3]
    #190.5
    #194.5
    # 创建一张单通道的图片，设置最大内接圆为不透明，注意圆心的坐标设置，cols是x坐标，rows是y坐标
    img_circle = np.zeros((rows,cols,1),np.uint8)
    img_circle[:,:,:] = 0  # 设置为全透明

    img_circle = cv2.circle(img_circle,(225,224), 161 ,(255),-1) # 设置最大内接圆为不透明
    # 图片融合
    img_new[:,:,3] = img_circle[:,:,0]

    # 保存图片
    savepath = input_img.split(".")[0]+"_1.png"
    # img_pil = Image.fromarray(cv2.cvtColor(img_new, cv2.COLOR_BGRA2RGBA))
    # img_rgb = img_pil.convert("RGB")
    # img_rgb.save(savepath)
    cv2.imwrite(savepath, img_new)
    # cv2.imencode('.jpg', img)[1].tofile('./9.jpg')  # 保存到另外的位置


    # 显示图片，调用matplotlib.pyplot展示
    # plt.subplot(121), plt.imshow(img_convert(img), cmap='gray'), plt.title('IMG')
    # plt.subplot(122), plt.imshow(img_convert(img_rgb), cmap='gray'), plt.title('IMG_NEW')
    # plt.subplot(123), plt.imshow(img_convert(img_new), cmap='gray'), plt.title('IMG_NEW')
    plt.show()
    return savepath
"""

#获取圆内切正方形
def get_square(input_img,r,center):
    """

    :param input_img:图像
    :param r: 圆半径
    :param center: 圆心
    :return: 正方形 [y0,y1,x0,x1]
    """
    #圆内接正方形，边长为2*math.sqrt(2)*r math.sqrt(2)近似等于0.7
    ratio = 0.8
    x,y = center[0], center[1]
    distence = ratio*r
    #x
    x0 = int(x-distence)
    x1 = int(x+distence)
    #y
    y0 = int(y-distence)
    y1 = int(y+distence)
    cropped = input_img[y0:y1, x0:x1]
    return cropped

"""
# cv2与matplotlib的图像转换，cv2是bgr格式，matplotlib是rgb格式
def img_convert(cv2_img):
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
"""

# 主函数
if __name__ == "__main__":

    path = r"C:\Users\Dell\Desktop\car_error_img\2.png"
    color = canny_circle(path)
    print(color)
    # circle(path)
