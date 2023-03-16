import cv2

# 读取待检测图像
img = cv2.imread(r"E:\workspace\data\tyre\Image_20210916155400421.jpg", 0)
# 读取模板图像
temple = cv2.imread(r"E:\workspace\data\tirecrop.jpg", 0)

# 显示灰度处理后的待检测图像
# cv2.namedWindow('sample', 0)
# cv2.resizeWindow('sample', 600, 600)
# cv2.imshow('sample', img)

# 显示灰度处理后的模板图像
cv2.namedWindow('target', 0)
cv2.resizeWindow('target', 60, 60)
cv2.imshow('target', temple)

# 获取模板图像的高和宽
th, tw = temple.shape[:2]
print(th, tw)

# 使用标准相关系数匹配,1表示完美匹配,-1表示糟糕的匹配,0表示没有任何相关性
result = cv2.matchTemplate(img, temple, cv2.TM_CCOEFF_NORMED)

# result为匹配结果矩阵
# print(result)


# TM_CCOEFF_NORMED方法处理后的结果图像
cv2.namedWindow('match_r', 0)
cv2.resizeWindow('match_r', 600, 600)
# 显示窗口
cv2.imshow('match_r', result)

# 使用函数minMaxLoc,确定匹配结果矩阵的最大值和最小值(val)，以及它们的位置(loc)
min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

# 此处选取最大值的位置,为图像的左上角
tl = max_loc
# 获取图像的右下角
br = (tl[0]+tw, tl[1]+th)
# 绘制矩形框
cv2.rectangle(img, tl, br, (255, 255, 0), 2)

# 设置显示窗口
cv2.namedWindow('match', 0) 
cv2.resizeWindow('match', 600, 600)
# 显示窗口
cv2.imshow('match', img)

# 结束
cv2.waitKey(0)
cv2.destroyAllWindows()
