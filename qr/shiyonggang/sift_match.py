import cv2
from matplotlib import pyplot as plt
import numpy as np
def bfMatch(imgpath1,imgpath2):
    img1 = cv2.imread(imgpath1, cv2.IMREAD_GRAYSCALE)
    img2 = cv2.imread(imgpath2, cv2.IMREAD_GRAYSCALE)
    orb = cv2.ORB_create()
    kp1, des1 = orb.detectAndCompute(img1, None)
    kp2, des2 = orb.detectAndCompute(img2, None)
    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
    matches = bf.match(des1, des2)
    matches = sorted(matches, key=lambda x: x.distance)
    img3 = cv2.drawMatches(img1, kp1, img2, kp2, matches[:80], img2, flags=2)

    plt.imshow(img3)
    plt.show()

def knnMatch(imgpath1,imgpath2):
    # coding:utf-8

    import cv2

    # 按照灰度图像读入两张图片
    img1 = cv2.imread(imgpath1, cv2.IMREAD_GRAYSCALE)
    img2 = cv2.imread(imgpath2, cv2.IMREAD_GRAYSCALE)

    # 获取特征提取器对象
    orb = cv2.ORB_create()
    # 检测关键点和特征描述
    keypoint1, desc1 = orb.detectAndCompute(img1, None)
    keypoint2, desc2 = orb.detectAndCompute(img2, None)
    """
    keypoint 是关键点的列表
    desc 检测到的特征的局部图的列表
    """
    # 获得knn检测器
    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
    matches = bf.knnMatch(desc1, desc2, k=1)
    """
    knn 匹配可以返回k个最佳的匹配项
    bf返回所有的匹配项
    """
    # 画出匹配结果
    img3 = cv2.drawMatchesKnn(img1, keypoint1, img2, keypoint2, matches, img2, flags=2)
    plt.imshow(img3), plt.title('Test3'),
    plt.axis('off')
    plt.show()

def convert_keypoint2dict(keypoint):
    points = []
    for p in keypoint:
        pdict = {"pt": p.pt,
                 "size": p.size,
                 "angle": p.angle,
                 "res": p.response,
                 "octave": p.octave,
                 "class_id": p.class_id
                 }
        points.append(pdict)
    return points

def convert_dict2keypoint(points):
    keypoints = []
    for p in points:
        kp = cv2.KeyPoint(x=p["pt"][0], y=p["pt"][1], _size=p["size"], _angle=p["angle"],
                          _response=p["res"], _octave=p["octave"], _class_id=p["class_id"])
        keypoints.append(kp)
    return keypoints




def crop_img(img):
    # img = cv2.imread(imgpath)
    print(img.shape)
    cropped = img[1500:2000, 560:3800]  # 裁剪坐标为[y0:y1, x0:x1]
    plt.imshow(cropped), plt.title('canny'),
    plt.axis('off')
    plt.show()
    return cropped

def FlannMatch(imgpath1,imgpath2):
    """
    FLANN是类似最近邻的快速匹配库
        它会根据数据本身选择最合适的算法来处理数据
        比其他搜索算法快10倍
    """
    start = time.time()
    # 按照灰度图片读入
    img1 = cv2.imread(imgpath1, cv2.IMREAD_GRAYSCALE)
    # img1 = cv2.imread(imgpath1)
    # img_1 = crop_img(img1)
    img2 = cv2.imread(imgpath2, cv2.IMREAD_GRAYSCALE)
    # img2 = cv2.imread(imgpath2)
    # 创建sift检测器
    sift = cv2.xfeatures2d.SIFT_create(nfeatures=None)
    # 查找监测点和匹配符
    kp1, des1 = sift.detectAndCompute(img1, None)
    # print("--points:{}--  des:{}--".format(kp1,des1))
    kp2, des2 = sift.detectAndCompute(img2, None)
    """
    keypoint是检测到的特征点的列表
    descriptor是检测到特征的局部图像的列表
    """
    # 获取flann匹配器
    FLANN_INDEX_KDTREE = 1
    indexParams = dict(algorithm=FLANN_INDEX_KDTREE, trees=10)
    searchParams = dict(checks=50)
    flann = cv2.FlannBasedMatcher(indexParams, searchParams)
    # 进行匹配
    matches = flann.knnMatch(des1, des2, k=2)
    good = []
    for i, (m, n) in enumerate(matches):
        if m.distance < 0.75*n.distance:
            good.append(m)
    print(len(good))
    # print("========")
    if len(good) >= 10:
        src_pts = np.float32([kp1[m.queryIdx].pt for m in good])
        dst_pts = np.float32([kp2[m.trainIdx].pt for m in good]).reshape(-1,2,1)
        # print("src_pts",src_pts)
        # print("dst_pts",dst_pts)
        _, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 1)
        # 用于绘图的mask
        matchesMask = mask.ravel().tolist()

        dst_pts = dst_pts.tolist()
        print("----",dst_pts)
        x1 = int(max(dst_pts, key=lambda x: x[0][0])[0][0])
        y1 = int(max(dst_pts, key=lambda y: y[1][0])[1][0])
        x0 = int(min(dst_pts, key=lambda x: x[0][0])[0][0])
        y0 = int(min(dst_pts, key=lambda y: y[1][0])[1][0])
        pt_size = [y0, y1, x0, x1]
        # mask可以去掉不可靠的点
        print("pt_size", pt_size)
    else:
        matchesMask = None
    # print(src_pts)
    # print("-------------------")
    # print(dst_pts)

    # print("===================")
    drawPrams = dict(matchColor=(0, 255, 0),
                     singlePointColor=None,
                     matchesMask=matchesMask,
                     flags=2)
    # 匹配结果图片
    img3 = cv2.drawMatches(img1, kp1, img2, kp2, good, None, **drawPrams)
    plt.imshow(img3), plt.title('Test3'),
    plt.axis('off')
    plt.show()

if __name__=="__main__":
    img_1 =r"E:\workspace\data\tirecrop.jpg"
    img_2 =  r"E:\workspace\data\tyre\Image_20210916155400421.jpg" 
    #import time
    #start = time.time()
    knnMatch(img_1, img_2)
    # FlannMatch(img_1, img_2)
    #print(time.time()-start)